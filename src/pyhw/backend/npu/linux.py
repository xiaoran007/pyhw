import subprocess
from .npuInfo import NPUInfo
from ..cpu import CPUDetect
from ...pyhwUtil import getArch
import pypci


class NPUDetectLinux:
    def __init__(self):
        self.__npuInfo = NPUInfo()

    def getNPUInfo(self):
        self.__getNPUInfo()
        self.__sortNPUList()
        return self.__npuInfo

    def __getNPUInfo(self):
        npu_devices = pypci.PCI().FindAllNPU()
        if len(npu_devices) == 0:
            self.__handleNonePciDevices()
        else:
            for device in npu_devices:
                if device.subsystem_device_name != "":
                    device_name = f"{device.vendor_name} {device.device_name} ({device.subsystem_device_name})"
                else:
                    device_name = f"{device.vendor_name} {device.device_name}"
                self.__npuInfo.npus.append(self.__npuNameClean(device_name))
                self.__npuInfo.number += 1

    def __handleNonePciDevices(self):
        # Place Holder for unknown NPU
        self.__npuInfo.number = 1
        self.__npuInfo.npus.append("Not found")

    @staticmethod
    def __npuNameClean(npu_name: str):
        npu_name_clean = npu_name.replace("Corporation ", "")
        return npu_name_clean

    def __sortNPUList(self):
        self.__npuInfo.npus.sort()

