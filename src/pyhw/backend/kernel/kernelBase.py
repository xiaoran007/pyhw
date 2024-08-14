from .linux import KernelDetectLinux
from ...pyhwException import OSUnsupportedException


class KernelDetect:
    def __init__(self, os):
        self.OS = os

    def getKernelInfo(self):
        if self.OS == "linux":
            return KernelDetectLinux().getKernelInfo()
        elif self.OS == "macos":
            pass
        elif self.OS == "windows":
            pass
        else:
            raise OSUnsupportedException("Unsupported operating system")
