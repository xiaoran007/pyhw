from dataclasses import dataclass


@dataclass
class HostInfo:
    """
    HostInfo class to store host information.
    """
    def __init__(self):
        """
        Initialize HostInfo class, model attribute is required.
        """
        self.os = ""
        self.model = ""
        self.family = ""
        self.name = ""
        self.version = ""
        self.sku = ""
        self.serial = ""
        self.uuid = ""
        self.vendor = ""
