from .logo import Logo
from .color import ColorConfigSetM, colorPrefix, colorSuffix
import re


class Printer:
    def __init__(self, logo_os: str, data: str):
        self.logo = Logo(logo_os).getLogoContent()
        self.data = data
        self.config = ColorConfigSetM.macOS
        self.logo_lines = self.logo.split("\n")
        self.data_lines = self.data.strip().split("\n")
        self.line_length = []
        self.processed_logo_lines = []
        self.combined_lines = []
        self.reg = r'\$\d+'

    def cPrint(self):
        self.__preprocess()
        max_len_ascii = max(line for line in self.line_length)
        for i, (logo_line, data_line) in enumerate(zip(self.processed_logo_lines, self.data_lines)):
            combined_line = logo_line.ljust(max_len_ascii) + "    " + data_line
            self.combined_lines.append(combined_line)

        for i, logo_line in enumerate(self.processed_logo_lines[len(self.data_lines):], start=len(self.data_lines)):
            self.combined_lines.append(logo_line)

        for data_line in self.data_lines[len(self.processed_logo_lines):]:
            self.combined_lines.append(" " * max_len_ascii + "    " + data_line)

        print("\n".join(self.combined_lines))

    def __preprocess(self):
        for logo_line in self.logo_lines:
            match = re.search(self.reg, logo_line)
            if match:
                self.line_length.append(len(logo_line) - 2)
                color = ColorConfigSetM.macOS.get("colors")[int(match[0][-1]) - 1]
                self.processed_logo_lines.append(re.sub(self.reg, colorPrefix(color), logo_line))
            else:
                self.line_length.append(len(logo_line))
                self.processed_logo_lines.append(logo_line)

