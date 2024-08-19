from dataclasses import dataclass


@dataclass
class GPUInfo:
    def __init__(self):
        self.number = 0
        self.gpus = []
