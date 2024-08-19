from .linux import HostDetectLinux
from .macos import HostDetectMacOS
from .windows import HostDetectWindows
from ...pyhwException import OSUnsupportedException


class HostDetect:
    def __init__(self, os):
        self.OS = os

    def getHostInfo(self):
        if self.OS == "linux":
            return HostDetectLinux().getHostInfo()
        elif self.OS == "macos":
            return HostDetectMacOS().getHostInfo()
        elif self.OS == "windows":
            pass
        else:
            raise OSUnsupportedException("Unsupported operating system")
