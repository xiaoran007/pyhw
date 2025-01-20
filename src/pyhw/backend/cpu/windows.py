import re
import os
import subprocess
from .cpuInfo import CPUInfo


class CPUDetectWindows:
    def __init__(self):
        self.__cpuInfo = CPUInfo()

    def getCPUInfo(self):
        self.__getCPUInfo()
        if self.__cpuInfo.model == "":
            self.__cpuInfo.model = "Unknown"
        if self.__cpuInfo.model != "":
            self.__cpuInfo.cpu = self.__cpuInfo.model
            if self.__cpuInfo.cores != "":
                self.__cpuInfo.cpu += f" ({self.__cpuInfo.cores})"
            if self.__cpuInfo.frequency != "":
                self.__cpuInfo.cpu += f" @ {self.__cpuInfo.frequency}"
        return self.__cpuInfo

    def __getCPUInfo(self):
        try:
            result = subprocess.run(
                ["powershell", "-Command",
                 "Get-CimInstance -ClassName Win32_Processor | Select-Object -Property Name,NumberOfCores,MaxClockSpeed"],
                capture_output=True, text=True, check=True
            )
            output = result.stdout.strip().split("\n")
            if len(output) > 2:
                cpu_info = output[2].split()
                self.__cpuInfo.model = " ".join(cpu_info[:-2])
                self.__cpuInfo.cores = cpu_info[-2]
                self.__cpuInfo.frequency = f"{int(cpu_info[-1]) / 1000} GHz"
        except subprocess.CalledProcessError:
            pass

