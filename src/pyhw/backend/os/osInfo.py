from dataclasses import dataclass


@dataclass
class OSInfo:
    def __init__(self):
        self.prettyName = ""
        self.name = ""
        self.id = ""
        self.idLike = ""
        self.variant = ""
        self.variantID = ""
        self.version = ""
        self.versionID = ""
        self.versionCodename = ""
        self.codeName = ""
        self.buildID = ""
