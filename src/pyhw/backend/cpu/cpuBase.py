from .linux import CPUDetectLinux
from .macos import CPUDetectMacOS
from ...pyhwException import OSUnsupportedException


class CPUDetect:
    def __init__(self, os):
        self.OS = os

    def getCPUInfo(self):
        if self.OS == "linux":
            return CPUDetectLinux().getCPUInfo()
        elif self.OS == "macos":
            return CPUDetectMacOS().getCPUInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
