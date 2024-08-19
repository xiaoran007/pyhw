from .linux import GPUDetectLinux
from .macos import GPUDetectMacOS


class GPUDetect:
    def __init__(self, os):
        self.OS = os

    def getGPUInfo(self):
        if self.OS == "linux":
            return GPUDetectLinux().getGPUInfo()
        elif self.OS == "macos":
            return GPUDetectMacOS().getGPUInfo()
        else:
            raise NotImplementedError("Unsupported operating system")
