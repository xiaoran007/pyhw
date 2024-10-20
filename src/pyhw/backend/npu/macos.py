from .npuInfo import NPUInfo
from ...pyhwUtil import getArch
import json
import subprocess


class NPUDetectMacOS:
    def __init__(self):
        self.__npuInfo = NPUInfo()
        self.__arch = getArch()

    def getNPUInfo(self):
        if self.__arch == "aarch64":
            self.__getNPUAppleSilicon()
        else:   # Does not consider powerPC based Macs.
            self.__getNPUIntel()
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

