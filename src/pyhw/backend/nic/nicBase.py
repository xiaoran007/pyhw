from ...pyhwException import OSUnsupportedException


class NICDetect:
    """
    Class for network interface (NIC) detection.
    """
    def __init__(self, os):
        self.OS = os

    def getNICInfo(self):
        """
        Detects the network interfaces (NICs) connected to the system.
        :return: dataclass NICInfo, direct attr: nics
        """
        if self.OS == "linux":
            from .linux import NICDetectLinux
            return NICDetectLinux().getNICInfo()
        elif self.OS == "macos":
            from .macos import NICDetectMacOS
            return NICDetectMacOS().getNICInfo()
        elif self.OS == "freebsd":
            from .bsd import NICDetectBSD
            return NICDetectBSD().getNICInfo()
        elif self.OS == "windows":
            from .windows import NICDetectWindows
            return NICDetectWindows().getNICInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
