from .npuInfo import NPUInfo
from ...pyhwUtil import PCIManager


class NPUDetectWindows:
    def __init__(self):
        self._npuInfo = NPUInfo()

    def getNPUInfo(self):
        self._getNPUInfo()
        self._sortNPUList()
        return self._npuInfo

    def _getNPUInfo(self):
        npu_devices = PCIManager.get_instance().FindAllNPU()
        if len(npu_devices) == 0:
            self._handleNonePciDevices()
        else:
            for device in npu_devices:
                if device.subsystem_device_name != "":
                    device_name = f"{device.vendor_name} {device.device_name} ({device.subsystem_device_name})"
                else:
                    device_name = f"{device.vendor_name} {device.device_name}"
                self._npuInfo.npus.append(self._npuNameClean(device_name))
                self._npuInfo.number += 1

    def _handleNonePciDevices(self):
        # Place Holder for unknown NPU
        self._npuInfo.number = 1
        self._npuInfo.npus.append("Not found")

    @staticmethod
    def _npuNameClean(npu_name: str):
        npu_name_clean = npu_name.replace("Corporation ", "")
        return npu_name_clean

    def _sortNPUList(self):
        self._npuInfo.npus.sort()
