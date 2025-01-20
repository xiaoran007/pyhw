from dataclasses import dataclass


@dataclass
class OSInfo:
    """
    Dataclass to hold the OS information
    """
    def __init__(self):
        """
        Initialize the dataclass, prettyName and id attributes are required.
        """
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
