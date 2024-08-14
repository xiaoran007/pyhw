from .unix import ShellDetectUnix
from ...pyhwException import OSUnsupportedException


class ShellDetect:
    def __init__(self, os):
        self.OS = os

    def getShellInfo(self):
        if self.OS == "linux" or self.OS == "macos":
            return ShellDetectUnix().getShellInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
