from .gpuInfo import GPUInfo
from ...pyhwUtil import getArch
import json
import subprocess
import ctypes
from pathlib import Path


class GPUDetectMacOS:
    def __init__(self):
        self.__gpuInfo = GPUInfo()
        self.__arch = getArch()

    def getGPUInfo(self):
        if self.__arch == "aarch64":
            self.__getGPUAppleSilicon()
        else:   # Does not consider powerPC based Macs.
            self.__getGPUIntel()
        return self.__gpuInfo

    def __getGPUAppleSilicon(self):
        gpus = list()
        try:
            gpu_info_dict = json.loads(subprocess.check_output(["system_profiler", "SPDisplaysDataType", "-json"]))
            if 'SPDisplaysDataType' in gpu_info_dict:
                gpus = gpu_info_dict['SPDisplaysDataType']
                self.__gpuInfo.number = len(gpus)
            else:
                pass
        except Exception:
            return

        for gpu in gpus:
            self.__gpuInfo.gpus.append(f'{gpu.get("sppci_model")} ({gpu.get("sppci_cores")} Cores) [SOC Integrated]')

    def __getGPUIntel(self):
        if self.__getGPUIOKit():
            pass
        else:  # fallback to the default implementation
            gpus = list()
            try:
                gpu_info_dict = json.loads(subprocess.check_output(["system_profiler", "SPDisplaysDataType", "-json"]))
                if 'SPDisplaysDataType' in gpu_info_dict:
                    gpus = gpu_info_dict['SPDisplaysDataType']
                    self.__gpuInfo.number = len(gpus)
                else:
                    pass
            except Exception:
                return

            for gpu in gpus:
                if self.__handleVendor(gpu.get("spdisplays_vendor")) == "Intel":    # Integrated GPU
                    self.__gpuInfo.gpus.append(f'{gpu.get("sppci_model")} [CPU Integrated]')
                elif self.__handleVendor(gpu.get("spdisplays_vendor")) == "AMD":    # dGPU
                    self.__gpuInfo.gpus.append(f'{gpu.get("sppci_model")} {gpu.get("spdisplays_vram")} [Discrete]')
                elif self.__handleVendor(gpu.get("spdisplays_vendor")) == "Nvidia":    # Since current macOS does not support NVIDIA GPUs, this condition is not applicable
                    pass

    def __getGPUIOKit(self):
        try:
            package_root = Path(__file__).resolve().parent.parent.parent
            lib = ctypes.CDLL(f"{package_root}/library/lib/iokitGPULib.dylib")
            lib.getGPUInfo.restype = ctypes.c_char_p
            gpu_info = lib.getGPUInfo()
            gpus = gpu_info.decode('utf-8').split("; ")
            # if the first element is "Error", it means that the library failed to get the GPU info
            # Fall back to the default implementation
            if gpus[0] == "Error":
                return False
            self.__gpuInfo.number = len(gpus)
            for gpu in gpus:
                info_list = gpu.split(", ")
                model = info_list[0]
                vendor_id = info_list[1]
                vram = round(int(info_list[2]) / 1024, None)
                if self.__handleVendorID(vendor_id) == "Intel":    # Integrated GPU
                    self.__gpuInfo.gpus.append(f'{model} [CPU Integrated]')
                elif self.__handleVendorID(vendor_id) == "AMD":    # dGPU
                    self.__gpuInfo.gpus.append(f'{model} {vram} GB [Discrete]')
            return True
        except Exception as e:
            # print(f"An error occurred while getting GPU info using IOKit: {e}")
            return False

    @staticmethod
    def __handleVendor(vendor):
        if vendor == "sppci_vendor_Apple":
            return "Apple"
        elif vendor == "sppci_vendor_intel":
            return "Intel"
        elif vendor == "sppci_vendor_amd":
            return "AMD"
        else:
            return vendor

    @staticmethod
    def __handleVendorID(vendor_id):
        if vendor_id == "0x8086":
            return "Intel"
        elif vendor_id == "0x1002":
            return "AMD"
        else:
            return vendor_id

