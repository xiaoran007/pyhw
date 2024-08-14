from ...pyhwException import LogoNotFoundException
from pathlib import Path
import os


class Logo:
    def __init__(self, logo_os):
        self.__logo_os = logo_os
        self.__logo_ascii = ""

    def getLogoContent(self):
        self.__loadLogoAscii()
        return self.__logo_ascii

    def __loadLogoAscii(self):
        try:
            file_path = os.path.join(Path(__file__).parent, f"ascii/{self.__logo_os}.pyhw")
            with open(file_path, "r") as f:
                self.__logo_ascii = f.read()
        except FileNotFoundError:
            raise LogoNotFoundException(f"Logo for {self.__logo_os} not found.")

