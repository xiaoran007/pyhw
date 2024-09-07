from dataclasses import dataclass


@dataclass
class NICInfo:
    def __init__(self):
        self.number = 0
        self.nics = []
