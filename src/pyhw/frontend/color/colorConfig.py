from dataclasses import dataclass
from .colorSet import ColorSet


@dataclass
class ColorConfigSetA:
    pass


@dataclass
class ColorConfigSetD:
    pass


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

