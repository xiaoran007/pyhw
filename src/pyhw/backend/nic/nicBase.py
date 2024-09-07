from .linux import NICDetectLinux


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