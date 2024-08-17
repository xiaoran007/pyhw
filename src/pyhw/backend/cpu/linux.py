from dataclasses import dataclass
import re
import os


@dataclass
class CPUInfoLinux:
    cpu = ""
    model = ""
    cores = ""
    frequency = ""


class CPUDetectLinux:
    def __init__(self):
        self.__cpuInfo = CPUInfoLinux()

    def getCPUInfo(self):
        self.__getCPUInfo()
        if self.__cpuInfo.model != "":
            self.__cpuInfo.cpu = self.__cpuInfo.model
            if self.__cpuInfo.cores != "":
                self.__cpuInfo.cpu += f" ({self.__cpuInfo.cores})"
            if self.__cpuInfo.frequency != "":
                self.__cpuInfo.cpu += f" @ {self.__cpuInfo.frequency}"
        return self.__cpuInfo

    def __getCPUInfo(self):
        try:
            with open("/proc/cpuinfo", "r") as f:
                cpu_info = f.read()
        except FileNotFoundError:
            return
        for line in cpu_info.split("\n"):
            if (line.startswith("model name") or line.startswith("Hardware") or line.startswith("Processor") or
                    line.startswith("cpu model") or line.startswith("chip type") or line.startswith("cpu type")):
                model = line.split(":")[1].strip()
                if "@" in model:
                    self.__cpuInfo.model = model.split("@")[0].strip()
                    self.__cpuInfo.frequency = model.split("@")[1].strip()
                else:
                    self.__cpuInfo.model = model
                break
        self.__cpuInfo.cores = len(re.findall(r"processor", cpu_info))
        if self.__cpuInfo.frequency == "":
            if os.path.exists("/sys/devices/system/cpu/cpu0/cpufreq"):
                try:
                    with open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq", "r") as f:
                        self.__cpuInfo.frequency = f"{int(f.read()) / 1000 / 1000} Ghz"  # Ghz
                except FileNotFoundError:
                    pass
            else:
                for line in cpu_info.split("\n"):
                    if line.startswith("cpu MHz") or line.startswith("clock"):
                        self.__cpuInfo.frequency = float(line.split(":")[1].strip()) / 1000  # Ghz
                        break
