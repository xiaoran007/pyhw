from dataclasses import dataclass


@dataclass
class KernelInfo:
    def __init__(self):
        self.name = ""
        self.version = ""
        self.machine = ""
        self.kernel = ""
