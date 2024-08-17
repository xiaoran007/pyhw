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


@dataclass
class ColorConfigSetA:
    pass


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
class ColorConfigSetL:
    linux = {
        "colors": [
            ColorSet.COLOR_FG_WHITE,
            ColorSet.COLOR_FG_BLACK,
            ColorSet.COLOR_FG_YELLOW
        ],
        "colorKeys": ColorSet.COLOR_FG_BLACK,
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

