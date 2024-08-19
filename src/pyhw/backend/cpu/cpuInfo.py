from dataclasses import dataclass


@dataclass
class CPUInfo:
    """
    Class to store CPU information. Print key: cpu
    """
    def __init__(self):
        self.cpu = ""
        self.model = ""
        self.cores = ""
        self.frequency = ""
