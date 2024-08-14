"""
    In dev.
"""
from dataclasses import dataclass
import os
import subprocess


@dataclass
class ShellInfoUnix:
    shell = ""
    version = ""
    path = ""
    info = ""


class ShellDetectUnix:
    def __init__(self):
        self.__shellInfo = ShellInfoUnix()

    def getShellInfo(self):
        self.__getShell()
        self.__getVersion()
        self.__shellInfo.info = self.__shellInfo.shell + " " + self.__shellInfo.version
        return self.__shellInfo

    def __getShell(self):
        # Get the default shell, not the current shell.
        shell_env = os.getenv("SHELL", "")
        if shell_env != "":
            self.__shellInfo.shell = shell_env.split("/")[-1]
            self.__shellInfo.path = shell_env

    def __getVersion(self):
        shell = self.__shellInfo.shell
        if shell != "":
            if shell in ["sh", "ash", "dash", "es"]:
                pass
            elif shell == "bash":
                try:
                    result = subprocess.run(["bash", "-c", "echo $BASH_VERSION"], capture_output=True, text=True)
                    self.__shellInfo.version = result.stdout.strip()
                except subprocess.SubprocessError:
                    pass
            elif shell == "zsh":
                try:
                    result = subprocess.run(["zsh", "-c", "echo $ZSH_VERSION"], capture_output=True, text=True)
                    self.__shellInfo.version = result.stdout.strip()
                except subprocess.SubprocessError:
                    pass






