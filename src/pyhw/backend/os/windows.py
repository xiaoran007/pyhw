from .osInfo import OSInfo
import platform


class OSDetectWindows:
    def __init__(self):
        self._osInfo = OSInfo()

    def getOSInfo(self):
        system = platform.system()
        release = platform.release()
        edition = platform.win32_edition()
        machine = platform.machine()
        self._osInfo.prettyName = f"{system} {release} ({edition}) {machine}"
        if release == "10":
            self._osInfo.id = "windows_10"
        elif release == "11":
            self._osInfo.id = "windows_11"
        else:
            self._osInfo.id = "windows_old"
        return self._osInfo

