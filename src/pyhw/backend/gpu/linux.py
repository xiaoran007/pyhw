import subprocess
from dataclasses import dataclass


@dataclass
class GPUInfoLinux:
    number = 0
    gpus = []


class GPUDetectLinux:
    def __init__(self):
        self.__gpuInfo = GPUInfoLinux()

    def getGPUInfo(self):
        self.__getGPUInfo()
        return self.__gpuInfo

    def __getGPUInfo(self):
        try:
            pci_info = subprocess.run(["bash", "-c", "lspci"], capture_output=True, text=True).stdout.strip()
        except subprocess.SubprocessError:
            return
        for line in pci_info.split("\n"):
            if "VGA" in line or "Display" in line or "3D" in line:
                gpu = line.split(": ")[1]
                self.__gpuInfo.gpus.append(gpu)
                self.__gpuInfo.number += 1
