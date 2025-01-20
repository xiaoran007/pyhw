"""
    In dev.
"""
from .shellInfo import ShellInfo
import os
import subprocess


class ShellDetectWindows:
    def __init__(self):
        self.__shellInfo = ShellInfo()

    def getShellInfo(self):
        self.__shellInfo.info = "PowerShell"
        return self.__shellInfo
