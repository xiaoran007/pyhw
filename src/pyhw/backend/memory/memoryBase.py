from ...pyhwException import OSUnsupportedException


class MemoryDetect:
    def __init__(self, os):
        self.OS = os

    def getMemoryInfo(self):
        if self.OS == "linux":
            from .linux import MemoryDetectLinux
            return MemoryDetectLinux().getMemoryInfo()
        elif self.OS == "macos":
            from .macos import MemoryDetectMacOS
            return MemoryDetectMacOS().getMemoryInfo()
        elif self.OS == "freebsd":
            from .bsd import MemoryDetectBSD
            return MemoryDetectBSD().getMemoryInfo()
        elif self.OS == "windows":
            from .windows import MemoryDetectWindows
            return MemoryDetectWindows().getMemoryInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
