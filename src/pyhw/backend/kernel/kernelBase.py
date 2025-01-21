from ...pyhwException import OSUnsupportedException


class KernelDetect:
    def __init__(self, os):
        self.OS = os

    def getKernelInfo(self):
        if self.OS in ["linux", "macos", "freebsd"]:
            from .unix import KernelDetectUnix
            return KernelDetectUnix().getKernelInfo()
        elif self.OS == "windows":
            from .windows import KernelDetectWindows
            return KernelDetectWindows().getKernelInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
