import subprocess
from .gpuInfo import GPUInfo
from ..cpu import CPUDetect
from ...pyhwUtil import getArch


class GPUDetectLinux:
    def __init__(self):
        self.__gpuInfo = GPUInfo()

    def getGPUInfo(self):
        self.__getGPUInfo()
        self.__sortGPUList()
        return self.__gpuInfo

    def __getGPUInfo(self):
        try:
            pci_info = subprocess.run(["bash", "-c", "lspci"], capture_output=True, text=True).stdout.strip()
        except subprocess.SubprocessError:
            return
        if len(pci_info) == 0:  # no pcie devices found
            self.__handleNonePciDevices()
        for line in pci_info.split("\n"):
            if "VGA" in line or "Display" in line or "3D " in line:
                gpu = line.split(": ")[1]
                self.__gpuInfo.gpus.append(self.__gpuNameClean(gpu))
                self.__gpuInfo.number += 1
        if self.__gpuInfo.number == 0:
            self.__handleNonePciDevices()  # fallback to a sbc device detection method

    def __handleNonePciDevices(self):
        # if detector can't find any VGA/Display/3D GPUs, assume the host is a sbc device, this function is a placeholder for a more advanced method.
        if getArch() == "aarch64" or getArch() == "arm32":
            self.__gpuInfo.number = 1
            self.__gpuInfo.gpus.append(f"{CPUDetect(os='linux').getCPUInfo().model} [SOC Integrated]")
        else:
            self.__gpuInfo.number = 1
            self.__gpuInfo.gpus.append("Not found")

    @staticmethod
    def __gpuNameClean(gpu_name: str):
        gpu_name_clean = gpu_name.replace("Corporation", "")
        return gpu_name_clean

    def __sortGPUList(self):
        self.__gpuInfo.gpus.sort()

