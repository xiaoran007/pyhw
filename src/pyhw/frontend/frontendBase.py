from .logo import Logo
from .color import ColorConfigSet, colorPrefix, colorSuffix, ColorSet
from ..pyhwUtil import getOS
import os
import re


class Printer:
    def __init__(self, logo_os: str, data: str):
        self.__logo = Logo(logo_os).getLogoContent()
        self.__data = data
        self.__config = ColorConfigSet(logo_os).getColorConfigSet()
        self.__logo_lines = self.__logo.split("\n")
        self.__data_lines = self.__data.strip().split("\n")
        self.__line_length = []
        self.__processed_logo_lines = []
        self.__processed_data_lines = []
        self.__combined_lines = []
        self.__logo_color_indexes = {}
        self.__reg = r'\$(\d)'
        self.__columns = self.__getColumns()

    def cPrint(self):
        self.__LogoPreprocess()
        self.__DataPreprocess()
        max_len_logo = max(self.__line_length)
        for i, (logo_line, data_line) in enumerate(zip(self.__processed_logo_lines, self.__processed_data_lines)):
            combined_line = logo_line + " " * (max_len_logo - self.__line_length[i] + 1) + data_line
            self.__combined_lines.append(combined_line)

        for i, logo_line in enumerate(self.__processed_logo_lines[len(self.__processed_data_lines):], start=len(self.__processed_data_lines)):
            self.__combined_lines.append(logo_line)

        for data_line in self.__processed_data_lines[len(self.__processed_logo_lines):]:
            self.__combined_lines.append(" " * (max_len_logo + 1) + data_line)

        self.__dropLongString()

        print("\n".join(self.__combined_lines))

    def __dropLongString(self):
        # Need more accurate way to drop long strings
        if getOS() == "linux":
            fixed_lines = list()
            for line in self.__combined_lines:
                if len(line) > self.__columns+20:
                    fixed_lines.append(line[:self.__columns+20])
                else:
                    fixed_lines.append(line)
            self.__combined_lines = fixed_lines
        else:
            pass


    @staticmethod
    def __getColumns() -> int:
        if getOS() == "linux":
            try:
                _, columns_str = os.popen('stty size', 'r').read().split()
                columns = int(columns_str)
            except:
                columns = 80  # default terminal size is 80 columns
        else:
            # macOS default terminal size is 80 columns
            columns = 80
        return columns

    def __LogoPreprocess(self):
        global_color = self.__config.get("colors")[0]
        for logo_line in self.__logo_lines:
            matches = re.findall(pattern=self.__reg, string=logo_line)
            color_numbers = len(matches)
            line_length = len(logo_line)
            if color_numbers > 0:
                colors = [int(match) - 1 for match in matches]  # color indexes
                temp_line = colorPrefix(ColorSet.COLOR_MODE_BOLD) + colorPrefix(global_color) + logo_line + colorSuffix()
                for color in colors:
                    temp_line = temp_line.replace(f"${color+1}", colorPrefix(self.__config.get("colors")[color]))
                global_color = self.__config.get("colors")[colors[-1]]  # set the global color to the last used color
            else:
                temp_line = colorPrefix(ColorSet.COLOR_MODE_BOLD) + colorPrefix(global_color) + logo_line + colorSuffix()
            flags_number = len(re.findall(pattern=r'\$\$', string=logo_line)) + len(re.findall(pattern=r'\$\0', string=logo_line))
            if flags_number > 0:
                temp_line = temp_line.replace("$$", "$")
                temp_line = temp_line.replace("$\0", "$")
            self.__line_length.append(line_length - 2 * color_numbers - flags_number)
            self.__processed_logo_lines.append(temp_line)

    def __DataPreprocess(self):
        header_color = self.__config.get("colorTitle")
        keys_color = self.__config.get("colorKeys")
        self.__processed_data_lines.append(" " + colorPrefix(ColorSet.COLOR_MODE_BOLD) + colorPrefix(header_color) +
                                           self.__data_lines[0].split("@")[0] + colorSuffix() + colorPrefix(ColorSet.COLOR_MODE_BOLD) +
                                           "@" + colorPrefix(header_color) +
                                           self.__data_lines[0].split("@")[1] + colorSuffix())
        self.__processed_data_lines.append(colorSuffix() + self.__data_lines[1])
        for data_line in self.__data_lines[2:]:
            name, value = data_line.split(": ")
            self.__processed_data_lines.append(colorPrefix(ColorSet.COLOR_MODE_BOLD) + colorPrefix(keys_color) + name + ": " + colorSuffix() + value)


