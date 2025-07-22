import subprocess
from .nicInfo import NICInfo
from ...pyhwUtil import PCIManager
import os


class NICDetectLinux:
    def __init__(self):
        self._nicInfo = NICInfo()

    def getNICInfo(self):
        self._getNICInfo()
        self._sortNICList()
        return self._nicInfo

    def _getNICInfo(self):
        nic_devices = PCIManager.get_instance().FindAllNIC()
        if len(nic_devices) == 0:
            self.__handleNonePciDevices()
        else:
            for device in nic_devices:
                if device.subsystem_device_name != "":
                    device_name = f"{device.vendor_name} {device.device_name} ({device.subsystem_device_name})"
                else:
                    device_name = f"{device.vendor_name} {device.device_name}"
                self._nicInfo.nics.append(self._nicNameClean(device_name))
                self._nicInfo.number += 1

    def __handleNonePciDevices(self):
        # need to update
        interfaces = list()
        for i in os.listdir('/sys/class/net/'):
            if i == "lo":
                continue
            interfaces.append(i)
        if len(interfaces) > 0:
            for interface in interfaces:
                try:
                    if_ip = subprocess.run(["bash", "-c", f"ip -4 addr show {interface} | grep inet | awk '{{print $2}}'"], capture_output=True, text=True).stdout.strip().split("/")[0]
                    if if_ip == "":
                        continue
                    self._nicInfo.nics.append(f"{interface} @ {if_ip}")
                    self._nicInfo.number += 1
                except:
                    pass
        else:
            pass
        if self._nicInfo.number == 0:
            self._nicInfo.nics.append("Not found")
            self._nicInfo.number = 1

    @staticmethod
    def _nicNameClean(nic_name: str):
        nic_name_clean = nic_name.replace("Corporation ", "")
        return nic_name_clean

    def _sortNICList(self):
        return self._nicInfo.nics.sort()
