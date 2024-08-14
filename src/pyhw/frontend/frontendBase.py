from .logo import Logo
from .color import ColorConfigSetM, colorPrefix, colorSuffix
import re


class Printer:
    def __init__(self, logo_os: str, data: str):
        self.__logo = Logo(logo_os).getLogoContent()
        self.__data = data
        self.__config = ColorConfigSetM.macOS  # for test
        self.__logo_lines = self.__logo.split("\n")
        self.__data_lines = self.__data.strip().split("\n")
        self.__processed_logo_lines = []
        self.__processed_data_lines = []
        self.__combined_lines = []
        self.__logo_color_indexes = {}
        self.__reg = r'\$\d+'

    def cPrint(self):
        self.__LogoPreprocess()
        self.__DataPreprocess()
        max_len_logo = max(len(i) for i in self.__processed_logo_lines)
        for i, (logo_line, data_line) in enumerate(zip(self.__processed_logo_lines, self.__processed_data_lines)):
            if i in self.__logo_color_indexes.keys():
                combined_line = colorPrefix(self.__logo_color_indexes[i]) + logo_line.ljust(max_len_logo) + colorSuffix() + "    " + data_line
            else:
                combined_line = logo_line.ljust(max_len_logo) + "    " + data_line
            self.__combined_lines.append(combined_line)

        for i, logo_line in enumerate(self.__processed_logo_lines[len(self.__processed_data_lines):], start=len(self.__processed_data_lines)):
            self.__combined_lines.append(colorPrefix(self.__logo_color_indexes[i]) + logo_line + colorSuffix())

        for data_line in self.__processed_data_lines[len(self.__processed_logo_lines):]:
            self.__combined_lines.append(" " * max_len_logo + "    " + data_line)

        print("\n".join(self.__combined_lines))

    def __LogoPreprocess(self):
        i = 0
        color = self.__config.get("colors")[0]
        for logo_line in self.__logo_lines:
            match = re.search(self.__reg, logo_line)
            if match:
                color = self.__config.get("colors")[int(match[0][-1]) - 1]
                self.__processed_logo_lines.append(re.sub(self.__reg, "", logo_line))
                self.__logo_color_indexes[i] = color
            else:
                self.__processed_logo_lines.append(logo_line)
                self.__logo_color_indexes[i] = color
            i += 1

    def __DataPreprocess(self):
        header_color = self.__config.get("colorTitle")
        keys_color = self.__config.get("colorKeys")
        self.__processed_data_lines.append(colorPrefix(header_color) + self.__data_lines[0])
        self.__processed_data_lines.append(colorPrefix(header_color) + self.__data_lines[1])
        for data_line in self.__data_lines[2:]:
            name, value = data_line.split(": ")
            self.__processed_data_lines.append(colorPrefix(keys_color) + name + ": " + colorSuffix() + value)

