from .linux import CPUDetectLinux
from ...pyhwException import OSUnsupportedException


class CPUDetect:
    def __init__(self, os):
        self.OS = os

    def getCPUInfo(self):
        if self.OS == "linux":
            return CPUDetectLinux().getCPUInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
