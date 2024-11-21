from .cpuInfo import CPUInfo
from ...pyhwUtil import sysctlGetString, sysctlGetInt, getArch


class CPUDetectBSD:
    def __init__(self):
        self.__cpuInfo = CPUInfo()

    def getCPUInfo(self):
        self.__cpuInfo.cpu = sysctlGetString("hw.model")
        return self.__cpuInfo

