from dataclasses import dataclass


@dataclass
class TitleInfo:
    def __init__(self):
        self.username = ""
        self.hostname = ""
        self.title = ""
