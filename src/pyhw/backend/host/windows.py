from ...pyhwUtil import getArch
from ...pyhwException import BackendException
from .hostInfo import HostInfo
import winreg


class HostDetectWindows:
    def __init__(self):
        self._hostInfo = HostInfo()
        self._arch = getArch()

    def getHostInfo(self):
        self._getModel()
        return self._hostInfo

    def _getModel(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS")
            manufacturer, _ = winreg.QueryValueEx(key, "SystemManufacturer")
            name, _ = winreg.QueryValueEx(key, "SystemProductName")
            version, _ = winreg.QueryValueEx(key, "SystemVersion")
            winreg.CloseKey(key)
        except FileNotFoundError:
            raise BackendException("Unable to retrieve system information.")
        self._hostInfo.name = name
        self._hostInfo.version = version
        self._hostInfo.vendor = manufacturer
        self.__handleVM()
        self._hostInfo.model = self._hostInfo.name + " " + self._hostInfo.version

    def __handleVM(self):
        if self._hostInfo.name.startswith("VMware"):
            self._hostInfo.version = ""
