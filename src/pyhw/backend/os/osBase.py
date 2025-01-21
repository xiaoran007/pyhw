from ...pyhwException import OSUnsupportedException


class OSDetect:
    def __init__(self, os):
        self.__OS = os

    def getOSInfo(self):
        if self.__OS == "linux":
            from .linux import OSDetectLinux
            return OSDetectLinux().getOSInfo()
        elif self.__OS == "macos":
            from .macos import OSDetectMacOS
            return OSDetectMacOS().getOSInfo()
        elif self.__OS == "freebsd":
            from .bsd import OSDetectBSD
            return OSDetectBSD().getOSInfo()
        elif self.__OS == "windows":
            from .windows import OSDetectWindows
            return OSDetectWindows().getOSInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
