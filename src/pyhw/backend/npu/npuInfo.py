from dataclasses import dataclass


@dataclass
class NPUInfo:
    def __init__(self):
        self.number = 0
        self.npus = []


