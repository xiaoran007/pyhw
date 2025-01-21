from ...pyhwException import OSUnsupportedException


class HostDetect:
    def __init__(self, os):
        self.OS = os

    def getHostInfo(self):
        if self.OS == "linux":
            from .linux import HostDetectLinux
            return HostDetectLinux().getHostInfo()
        elif self.OS == "macos":
            from .macos import HostDetectMacOS
            return HostDetectMacOS().getHostInfo()
        elif self.OS == "freebsd":
            from .bsd import HostDetectBSD
            return HostDetectBSD().getHostInfo()
        elif self.OS == "windows":
            from .windows import HostDetectWindows
            return HostDetectWindows().getHostInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
