"""
    In dev.
"""
from ...pyhwException import BackendException
from .shellInfo import ShellInfo
import json
import subprocess


class ShellDetectWindows:
    def __init__(self):
        self.__shellInfo = ShellInfo()

    def getShellInfo(self):
        COMMAND = "$PSVersionTable.PSVersion | ConvertTo-JSON"

        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", COMMAND], capture_output=True, text=True)
        except subprocess.SubprocessError:
            raise BackendException("Error running PowerShell command.")

        res = json.loads(result.stdout)
        major = res["Major"]
        minor = res["Minor"]

        self.__shellInfo.shell = "PowerShell"
        self.__shellInfo.version = f"{major}.{minor}"
        self.__shellInfo.info = f"PowerShell {major}.{minor}"
        return self.__shellInfo
