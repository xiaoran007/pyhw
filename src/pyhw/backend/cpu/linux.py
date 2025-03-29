import re
import os
from .cpuInfo import CPUInfo


class CPUDetectLinux:
    def __init__(self):
        self.__cpuInfo = CPUInfo()

    def getCPUInfo(self):
        self.__getCPUInfo()
        self.__modelClean()
        self.__handleSBC()
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
                        self.__cpuInfo.frequency = f"{round(float(line.split(':')[1].strip()) / 1000, 2)} Ghz"  # Ghz
                        break

    def __modelClean(self):
        self.__cpuInfo.model = self.__cpuInfo.model.replace("(R)", "")
        self.__cpuInfo.model = self.__cpuInfo.model.replace("(TM)", "")

    def __handleSBC(self):
        # some values should be double-checked
        # Info source: https://github.com/raspberrypi/firmware/tree/master/boot
        if os.path.exists("/sys/firmware/devicetree/base/compatible"):
            try:
                with open("/sys/firmware/devicetree/base/compatible", "r") as f:
                    compatible = f.read().strip()
            except FileNotFoundError:
                compatible = ""
            if "raspberrypi" in compatible:
                model = compatible.split(",")[-1]
                if model.startswith("bcm"):
                    self.__cpuInfo.model = model.upper()
            elif "orangepi" in compatible:
                if "allwinner" in compatible:
                    model = compatible.split(",")[-1]
                    if model.startswith("sun"):
                        self.__cpuInfo.model = f"Allwinner {model.split('-')[-1].upper()} ({model})"
            elif "cvitek" in compatible:
                model = compatible.split(",")[-1]
                self.__cpuInfo.model = f"Cvitek {model}"
        else:
            pass
