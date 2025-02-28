from dataclasses import dataclass


@dataclass
class ShellInfo:
    def __init__(self):
        """
        ShellInfo class. Attribute info is required.
        """
        self.shell = ""
        self.version = ""
        self.path = ""
        self.info = ""
