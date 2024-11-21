from .linux import NICDetectLinux
from .macos import NICDetectMacOS
from .bsd import NICDetectBSD


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
            return NICDetectLinux().getNICInfo()
        elif self.OS == "macos":
            return NICDetectMacOS().getNICInfo()
        elif self.OS == "freebsd":
            return NICDetectBSD().getNICInfo()
        else:
            raise NotImplementedError("Unsupported operating system")
