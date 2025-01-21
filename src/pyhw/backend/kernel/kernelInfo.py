from dataclasses import dataclass


@dataclass
class KernelInfo:
    """
    Data class for storing kernel information.
    """
    def __init__(self):
        """
        Initialize the data class, kernel attribute is required.
        """
        self.name = ""
        self.version = ""
        self.machine = ""
        self.kernel = ""
