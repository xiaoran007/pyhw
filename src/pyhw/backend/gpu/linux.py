import subprocess
from .gpuInfo import GPUInfo
from ..cpu import CPUDetect
from ...pyhwUtil import getArch
import pypci


class GPUDetectLinux:
    def __init__(self):
        self.__gpuInfo = GPUInfo()

    def getGPUInfo(self):
        self.__getGPUInfo()
        self.__sortGPUList()
        return self.__gpuInfo

    def __getGPUInfo(self):
        gpu_devices = pypci.PCI().FindAllVGA()
        if len(gpu_devices) == 0:
            self.__handleNonePciDevices()
        else:
            for device in gpu_devices:
                if device.subsystem_device_name != "":
                    device_name = f"{device.vendor_name} {device.device_name} ({device.subsystem_device_name})"
                else:
                    device_name = f"{device.vendor_name} {device.device_name}"
                self.__gpuInfo.gpus.append(self.__gpuNameClean(device_name))
                self.__gpuInfo.number += 1

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

    def __sortGPUList(self):
        self.__gpuInfo.gpus.sort()

