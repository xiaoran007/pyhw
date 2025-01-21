from dataclasses import dataclass


@dataclass
class ShellInfo:
    def __init__(self):
        self.shell = ""
        self.version = ""
        self.path = ""
        self.info = ""
