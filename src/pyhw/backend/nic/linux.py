import subprocess
from .nicInfo import NICInfo
from ...pyhwUtil import getArch
from ...pyhwException import BackendException


class NICDetectLinux:
    def __init__(self):
        self.__nicInfo = NICInfo()

    def getNICInfo(self):
        self.__getNICInfo()
        self.__sortNICList()
        return self.__nicInfo

    def __getNICInfo(self):
        try:
            pci_info = subprocess.run(["bash", "-c", "lspci"], capture_output=True, text=True).stdout.strip()
        except subprocess.SubprocessError:
            return
        if len(pci_info) == 0:  # no pcie devices found
            self.__handleNonePciDevices()
            return
        for line in pci_info.split("\n"):
            if "Ethernet controller" in line or "Network controller" in line:
                nic = line.split(": ")[1]
                self.__nicInfo.nics.append(self.__nicNameClean(nic))
                self.__nicInfo.number += 1
        if self.__nicInfo.number == 0:
            self.__handleNonePciDevices()  # fallback to usb detection method

    def __handleNonePciDevices(self):
        # placeholder for a more advanced method.
        self.__nicInfo.nics.append("Not found")
        self.__nicInfo.number = 1

    @staticmethod
    def __nicNameClean(nic_name: str):
        nic_name_clean = nic_name.replace("Corporation ", "")
        return nic_name_clean

    def __sortNICList(self):
        return self.__nicInfo.nics.sort()