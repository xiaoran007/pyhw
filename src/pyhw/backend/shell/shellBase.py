from .unix import ShellDetectUnix
from .windows import ShellDetectWindows
from ...pyhwException import OSUnsupportedException


class ShellDetect:
    def __init__(self, os):
        self.OS = os

    def getShellInfo(self):
        if self.OS in ["linux", "macos", "freebsd"]:
            return ShellDetectUnix().getShellInfo()
        elif self.OS == "windows":
            return ShellDetectWindows().getShellInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
