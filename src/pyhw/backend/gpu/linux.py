from .gpuInfo import GPUInfo
from ..cpu import CPUDetect
from ...pyhwUtil import getArch
from ...pyhwUtil import PCIManager
from pathlib import Path
import ctypes


class GPUDetectLinux:
    def __init__(self):
        self.__gpuInfo = GPUInfo()
        self.__arch = self.__setArch()

    def getGPUInfo(self):
        self.__getGPUInfo()
        self.__sortGPUList()
        return self.__gpuInfo

    def __getGPUInfo(self):
        gpu_devices = PCIManager.get_instance().FindAllVGA()
        if len(gpu_devices) == 0:
            self.__handleNonePciDevices()
        else:
            core_map = dict()
            for device in gpu_devices:
                record_cores = core_map.get(device.device_id, 0)
                if record_cores != 0:
                    pass
                else:
                    cores = self.__getGPUInfoNvidia(device)
                    core_map[device.device_id] = cores
            for device in gpu_devices:
                core = core_map.get(device.device_id, 0)
                if core == 0:
                    core_print = ""
                else:
                    core_print = f"({core} Cores)"
                if device.subsystem_device_name != "":
                    device_name = f"{device.vendor_name} {device.device_name} [{device.subsystem_device_name}] {core_print}"
                else:
                    device_name = f"{device.vendor_name} {device.device_name} {core_print}"

                if not device_name.strip():
                    device_name = f"{device.class_name}"

                self.__gpuInfo.gpus.append(self.__gpuNameClean(device_name))
                self.__gpuInfo.number += 1

    def __getGPUInfoNvidia(self, device):
        try:
            package_root = Path(__file__).resolve().parent.parent.parent
            lib = ctypes.CDLL(f"{package_root}/library/lib/nvmlGPULib_{self.__arch}.so")
            lib.GetGPUCoreCountByPciBusId.argtypes = [ctypes.c_char_p]
            lib.GetGPUCoreCountByPciBusId.restype = ctypes.c_uint
            cores = lib.GetGPUCoreCountByPciBusId(f'00000000:{device.bus}'.encode())
            return cores
        except Exception as e:
            # print(f"An error occurred while getting GPU info using nvml: {e}")
            return 0

    def __handleNonePciDevices(self):
        # if detector can't find any VGA/Display/3D GPUs, assume the host is a sbc device, this function is a placeholder for a more advanced method.
        if getArch() in ["aarch64", "arm32", "riscv64"]:
            self.__gpuInfo.number = 1
            self.__gpuInfo.gpus.append(f"{CPUDetect(os='linux').getCPUInfo().model} [SOC Integrated]")
        else:
            self.__gpuInfo.number = 1
            self.__gpuInfo.gpus.append("Not found")

    @staticmethod
    def __gpuNameClean(gpu_name: str):
        gpu_name_clean = gpu_name.replace("Corporation ", "")
        return gpu_name_clean

    @staticmethod
    def __setArch():
        arch = getArch()
        if arch == "aarch64":
            return "arm64"
        elif arch == "x86_64":
            return "amd64"

    def __sortGPUList(self):
        self.__gpuInfo.gpus.sort()
