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
        elif self.__os_name == "freebsd":
            return ColorConfigSetF.freebsd
        elif self.__os_name == "windows_old":
            return ColorConfigSetW.windows_old
        elif self.__os_name == "windows_10":
            return ColorConfigSetW.windows_10
        elif self.__os_name == "windows_11":
            return ColorConfigSetW.windows_11
        elif self.__os_name == "windows_2025":
            return ColorConfigSetW.windows_2025
        elif self.__os_name == "kali":
            return ColorConfigSetK.kali
        elif self.__os_name == "linuxmint":
            return ColorConfigSetL.linuxmint
        elif self.__os_name == "opensuse-leap":
            return ColorConfigSetO.openSUSELEAP
        elif self.__os_name == "opensuse-tumbleweed":
            return ColorConfigSetO.openSUSETumbleweed
        elif self.__os_name == "rhel":
            return ColorConfigSetR.rhel
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
    freebsd = {
        "colors": [
            ColorSet.COLOR_FG_WHITE,
            ColorSet.COLOR_FG_RED
        ],
        "colorKeys": ColorSet.COLOR_FG_RED,
        "colorTitle": ColorSet.COLOR_FG_RED
    }


@dataclass
class ColorConfigSetK:
    kali = {
        "colors": [
            ColorSet.COLOR_FG_LIGHT_BLUE,
            ColorSet.COLOR_FG_LIGHT_BLACK
        ],
        "colorKeys": ColorSet.COLOR_FG_LIGHT_GREEN,
        "colorTitle":  ColorSet.COLOR_FG_GREEN
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
    linuxmint = {
        "colors": [
            ColorSet.COLOR_FG_GREEN,
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_GREEN,
        "colorTitle": ColorSet.COLOR_FG_GREEN
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
class ColorConfigSetO:
    openSUSELEAP = {
        "colors": [
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_GREEN,
        "colorTitle":  ColorSet.COLOR_FG_GREEN
    }
    openSUSETumbleweed = {
        "colors": [
            ColorSet.COLOR_FG_WHITE
        ],
        "colorKeys": ColorSet.COLOR_FG_GREEN,
        "colorTitle": ColorSet.COLOR_FG_GREEN
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
    rhel = {
        "colors": [
            ColorSet.COLOR_FG_RED
        ],
        "colorKeys": ColorSet.COLOR_FG_RED,
        "colorTitle": ColorSet.COLOR_FG_RED
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


@dataclass
class ColorConfigSetW:
    windows_old = {
        "colors": [
            ColorSet.COLOR_FG_RED,
            ColorSet.COLOR_FG_GREEN,
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_YELLOW
        ],
        "colorKeys": ColorSet.COLOR_FG_BLUE,
        "colorTitle": ColorSet.COLOR_FG_GREEN
    }
    windows_10 = {
        "colors": [
            ColorSet.COLOR_FG_CYAN,
            ColorSet.COLOR_FG_CYAN,
            ColorSet.COLOR_FG_CYAN,
            ColorSet.COLOR_FG_CYAN
        ],
        "colorKeys": ColorSet.COLOR_FG_YELLOW,
        "colorTitle": ColorSet.COLOR_FG_GREEN
    }
    windows_11 = {
        "colors": [
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_BLUE
        ],
        "colorKeys": ColorSet.COLOR_FG_YELLOW,
        "colorTitle": ColorSet.COLOR_FG_CYAN
    }
    windows_2025 = {
        "colors": [
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_BLUE,
            ColorSet.COLOR_FG_BLUE
        ],
        "colorKeys": ColorSet.COLOR_FG_YELLOW,
        "colorTitle": ColorSet.COLOR_FG_CYAN
    }
