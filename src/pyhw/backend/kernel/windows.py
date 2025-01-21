"""
    In dev.
"""
from .kernelInfo import KernelInfo
from ...pyhwException import BackendException
import platform
import winreg


class KernelDetectWindows:
    def __init__(self):
        self.__kernelInfo = KernelInfo()

    def getKernelInfo(self):
        version = platform.version()
        machine = platform.machine()
        display = self.__get_windows_version()
        if display != "":
            self.__kernelInfo.kernel = f"{version} ({display}) {machine}"
        else:
            self.__kernelInfo.kernel = f"{version} {machine}"
        return self.__kernelInfo

    @staticmethod
    def __get_windows_version():
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
            winreg.CloseKey(key)
            return str(display_version)
        except:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
                release_id, _ = winreg.QueryValueEx(key, "ReleaseId")
                winreg.CloseKey(key)
                return str(release_id)
            except:
                return ""
