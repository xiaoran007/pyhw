from dataclasses import dataclass
from .colorSet import ColorSet


class ColorConfigSet:
    def __init__(self, os_name):
        self.__os_name = os_name

    def getColorConfigSet(self):
        if self.__os_name == "macOS":
            return ColorConfigSetM.macOS
        elif self.__os_name == "debian":
            return ColorConfigSetD.debian
        elif self.__os_name == "linux":
            return ColorConfigSetL.linux
        elif self.__os_name == "fedora":
            return ColorConfigSetF.fedora
        elif self.__os_name == "fedora_small":
            return ColorConfigSetF.fedora_small
        elif self.__os_name == "ubuntu":
            return ColorConfigSetU.ubuntu
        elif self.__os_name == "ubuntu_small":
            return ColorConfigSetU.ubuntu_small
        elif self.__os_name == "raspbian":
            return ColorConfigSetR.raspbian
        elif self.__os_name == "armbian":
            return ColorConfigSetA.armbian
        elif self.__os_name == "alpine":
            return ColorConfigSetA.alpine
        elif self.__os_name == "arch":
            return ColorConfigSetA.arch
        elif self.__os_name == "centos":
            return ColorConfigSetC.centos
        else:
            return ColorConfigSetL.linux  # default to Linux


@dataclass
class ColorConfigSetA:
    armbian = {
        "colors": [
            ColorSet.COLOR_FG_RED
        ],
        "colorKeys": ColorSet.COLOR_FG_YELLOW,
        "colorTitle": ColorSet.COLOR_FG_YELLOW
    }
    alpine = {
        "colors": [
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_MAGENTA,
        "colorTitle": ColorSet.COLOR_FG_BLUE
    }
    arch = {
        "colors": [
            ColorSet.COLOR_FG_CYAN,
            ColorSet.COLOR_FG_CYAN
        ],
        "colorKeys": ColorSet.COLOR_FG_CYAN,
        "colorTitle": ColorSet.COLOR_FG_CYAN
    }


@dataclass
class ColorConfigSetC:
    centos = {
        "colors": [
            ColorSet.COLOR_FG_YELLOW,
            ColorSet.COLOR_FG_GREEN,
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_MAGENTA,
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_GREEN,
        "colorTitle": ColorSet.COLOR_FG_YELLOW
    }


@dataclass
class ColorConfigSetD:
    debian = {
        "colors": [
            ColorSet.COLOR_FG_RED,
            ColorSet.COLOR_FG_LIGHT_BLACK
        ],
        "colorKeys": ColorSet.COLOR_FG_RED,
        "colorTitle":  ColorSet.COLOR_FG_RED
    }


@dataclass
class ColorConfigSetF:
    fedora = {
        "colors": [
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_BLUE,
        "colorTitle":  ColorSet.COLOR_FG_BLUE
    }
    fedora_small = {
        "colors": [
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_BLUE,
        "colorTitle": ColorSet.COLOR_FG_BLUE
    }


@dataclass
class ColorConfigSetL:
    linux = {
        "colors": [
            ColorSet.COLOR_FG_WHITE,
            ColorSet.COLOR_FG_BLACK,
            ColorSet.COLOR_FG_YELLOW
        ],
        "colorKeys": ColorSet.COLOR_FG_YELLOW,
        "colorTitle": ColorSet.COLOR_FG_YELLOW
    }


@dataclass
class ColorConfigSetM:
    macOS = {
        "colors": [
            ColorSet.COLOR_FG_GREEN,
            ColorSet.COLOR_FG_YELLOW,
            ColorSet.COLOR_FG_RED,
            ColorSet.COLOR_FG_MAGENTA,
            ColorSet.COLOR_FG_BLUE
        ],
        "colorKeys": ColorSet.COLOR_FG_YELLOW,
        "colorTitle":  ColorSet.COLOR_FG_GREEN
    }


@dataclass
class ColorConfigSetR:
    raspbian = {
        "colors": [
            ColorSet.COLOR_FG_RED,
            ColorSet.COLOR_FG_GREEN
        ],
        "colorKeys": ColorSet.COLOR_FG_RED,
        "colorTitle": ColorSet.COLOR_FG_GREEN
    }


@dataclass
class ColorConfigSetU:
    ubuntu = {
        "colors": [
            ColorSet.COLOR_FG_RED,
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_RED,
        "colorTitle":  ColorSet.COLOR_FG_RED
    }
    ubuntu_small = {
        "colors": [
            ColorSet.COLOR_FG_RED
        ],
        "colorKeys": ColorSet.COLOR_FG_RED,
        "colorTitle": ColorSet.COLOR_FG_RED
    }
