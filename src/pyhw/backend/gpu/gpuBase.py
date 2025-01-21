from .linux import GPUDetectLinux
from .macos import GPUDetectMacOS
from .bsd import GPUDetectBSD
from .windows import GPUDetectWindows


class GPUDetect:
    def __init__(self, os):
        self.OS = os

    def getGPUInfo(self):
        if self.OS == "linux":
            return GPUDetectLinux().getGPUInfo()
        elif self.OS == "macos":
            return GPUDetectMacOS().getGPUInfo()
        elif self.OS == "freebsd":
            return GPUDetectBSD().getGPUInfo()
        elif self.OS == "windows":
            return GPUDetectWindows().getGPUInfo()
        else:
            raise NotImplementedError("Unsupported operating system")
