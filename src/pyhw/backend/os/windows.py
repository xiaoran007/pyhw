from .osInfo import OSInfo
import platform
import winreg


class OSDetectWindows:
    def __init__(self):
        self._osInfo = OSInfo()

    def getOSInfo(self):
        system = platform.system()
        release = platform.release()
        edition = platform.win32_edition()
        machine = platform.machine()
        display = self.__get_windows_version()
        if display != "":
            self._osInfo.prettyName = f"{system} {release} {display} ({edition}) {machine}"
        else:
            self._osInfo.prettyName = f"{system} {release} ({edition}) {machine}"
        if release == "10":
            self._osInfo.id = "windows_10"
        elif release == "11":
            self._osInfo.id = "windows_11"
        else:
            self._osInfo.id = "windows_old"
        return self._osInfo

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
