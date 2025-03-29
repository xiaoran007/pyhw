import subprocess
from .cpuInfo import CPUInfo
import json


class CPUDetectWindows:
    def __init__(self):
        self.__cpuInfo = CPUInfo()

    def getCPUInfo(self):
        self.__getCPUInfo()
        self.__modelClean()
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
        COMMAND = "Get-CimInstance -ClassName Win32_Processor | Select-Object Name,NumberOfLogicalProcessors,MaxClockSpeed | ConvertTo-JSON"

        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", COMMAND], capture_output=True, text=True)
        except subprocess.SubprocessError:
            exit(-1)

        res = json.loads(result.stdout)
        name = res["Name"]
        cores = res["NumberOfLogicalProcessors"]
        frequency = round(int(res["MaxClockSpeed"]) / 1000.0, 2)  # GHz
        if "@" in name:
            self.__cpuInfo.model = name.split("@")[0].strip()
        else:
            self.__cpuInfo.model = name
        self.__cpuInfo.cores = str(cores)
        self.__cpuInfo.frequency = f"{frequency:.2f} GHz"

    def __modelClean(self):
        self.__cpuInfo.model = self.__cpuInfo.model.replace("(R)", "")
        self.__cpuInfo.model = self.__cpuInfo.model.replace("(TM)", "")
        self.__cpuInfo.model = self.__cpuInfo.model.replace("CPU ", "")
