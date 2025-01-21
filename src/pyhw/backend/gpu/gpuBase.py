from ...pyhwException import OSUnsupportedException


class GPUDetect:
    def __init__(self, os):
        self.OS = os

    def getGPUInfo(self):
        if self.OS == "linux":
            from .linux import GPUDetectLinux
            return GPUDetectLinux().getGPUInfo()
        elif self.OS == "macos":
            from .macos import GPUDetectMacOS
            return GPUDetectMacOS().getGPUInfo()
        elif self.OS == "freebsd":
            from .bsd import GPUDetectBSD
            return GPUDetectBSD().getGPUInfo()
        elif self.OS == "windows":
            from .windows import GPUDetectWindows
            return GPUDetectWindows().getGPUInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
