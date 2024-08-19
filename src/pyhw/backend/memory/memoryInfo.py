from dataclasses import dataclass


@dataclass
class MemoryInfo:
    def __init__(self):
        self.memory = ""
        self.total = 0
        self.available = 0
        self.used = 0
