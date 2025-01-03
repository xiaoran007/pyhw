from .unix import KernelDetectUnix
from ...pyhwException import OSUnsupportedException


class KernelDetect:
    def __init__(self, os):
        self.OS = os

    def getKernelInfo(self):
        if self.OS in ["linux", "macos", "freebsd"]:
            return KernelDetectUnix().getKernelInfo()
        elif self.OS == "windows":
            raise OSUnsupportedException("Unsupported operating system")
        else:
            raise OSUnsupportedException("Unsupported operating system")
