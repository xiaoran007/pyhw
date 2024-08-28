from .gpuInfo import GPUInfo
from ...pyhwUtil import getArch
import json
import subprocess


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
            self.__gpuInfo.gpus.append(f'{gpu.get("sppci_model")} ({gpu.get("sppci_cores")} cores) [SOC Integrated]')

    def __getGPUIntel(self):
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
