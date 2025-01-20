from .linux import OSDetectLinux
from .macos import OSDetectMacOS
from .bsd import OSDetectBSD
from .windows import OSDetectWindows
from ...pyhwException import OSUnsupportedException


class OSDetect:
    def __init__(self, os):
        self.__OS = os

    def getOSInfo(self):
        if self.__OS == "linux":
            return OSDetectLinux().getOSInfo()
        elif self.__OS == "macos":
            return OSDetectMacOS().getOSInfo()
        elif self.__OS == "freebsd":
            return OSDetectBSD().getOSInfo()
        elif self.__OS == "windows":
            raise OSDetectWindows.getOSInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
