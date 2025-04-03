from .npuInfo import NPUInfo
from ...pyhwUtil import getArch, getOS
from ..cpu import CPUDetect


class NPUDetectMacOS:
    def __init__(self):
        self.__npuInfo = NPUInfo()
        self.__arch = getArch()

    def getNPUInfo(self):
        self.__npuInfo.npus.append(self.__getNPUbyModelName())
        self.__npuInfo.number += 1
        # if self.__arch == "aarch64":
        #     self.__getNPUAppleSilicon()
        # else:   # Does not consider powerPC based Macs.
        #     self.__getNPUIntel()
        return self.__npuInfo

    def __getNPUAppleSilicon(self):
        # Place holder
        self.__npuInfo.npus.append("Apple Neural Engine [SOC Integrated]")
        self.__npuInfo.number += 1

    def __getNPUIntel(self):
        # Place holder
        self.__npuInfo.npus.append("Not Found")
        self.__npuInfo.number += 1

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
    def __getNPUbyModelName():
        # Placeholder
        # see https://apple.fandom.com/wiki/Neural_Engine for more details.
        model_name = CPUDetect(os=getOS()).getCPUInfo().model
        npu = {
            "Apple M1": "Apple Neural Engine 16 Cores (5nm) [SOC Integrated]",
            "Apple M1 Pro": "Apple Neural Engine 16 Cores (5nm) [SOC Integrated]",
            "Apple M1 Max": "Apple Neural Engine 16 Cores (5nm) [SOC Integrated]",
            "Apple M1 Ultra": "Apple Neural Engine 32 Cores (5nm) [SOC Integrated]",
            "Apple M2": "Apple Neural Engine 16 Cores (5nm) [SOC Integrated]",
            "Apple M2 Pro": "Apple Neural Engine 16 Cores (5nm) [SOC Integrated]",
            "Apple M2 Max": "Apple Neural Engine 16 Cores (5nm) [SOC Integrated]",
            "Apple M2 Ultra": "Apple Neural Engine 32 Cores (5nm) [SOC Integrated]",
            "Apple M3": "Apple Neural Engine 16 Cores (3nm) [SOC Integrated]",
            "Apple M3 Pro": "Apple Neural Engine 16 Cores (3nm) [SOC Integrated]",
            "Apple M3 Max": "Apple Neural Engine 16 Cores (3nm) [SOC Integrated]",
            "Apple M3 Ultra": "Apple Neural Engine 32 Cores (3nm) [SOC Integrated]",
            "Apple M4": "Apple Neural Engine 16 Cores (3nm) [SOC Integrated]",
            "Apple M4 Pro": "Apple Neural Engine 16 Cores (3nm) [SOC Integrated]",
            "Apple M4 Max": "Apple Neural Engine 16 Cores (3nm) [SOC Integrated]"
        }
        return npu.get(model_name, "Not Found")
