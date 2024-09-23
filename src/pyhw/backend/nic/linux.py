import subprocess
from .nicInfo import NICInfo
from ...pyhwUtil import getArch
from ...pyhwException import BackendException
import pypci


class NICDetectLinux:
    def __init__(self):
        self.__nicInfo = NICInfo()

    def getNICInfo(self):
        self.__getNICInfo()
        self.__sortNICList()
        return self.__nicInfo

    def __getNICInfo(self):
        nic_devices = pypci.PCI().FindAllNIC()
        if len(nic_devices) == 0:
            self.__handleNonePciDevices()
        else:
            for device in nic_devices:
                if device.subsystem_device_name != "":
                    device_name = f"{device.vendor_name} {device.device_name} ({device.subsystem_device_name})"
                else:
                    device_name = f"{device.vendor_name} {device.device_name}"
                self.__nicInfo.nics.append(self.__nicNameClean(device_name))
                self.__nicInfo.number += 1

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
