"""
    In dev.
"""
from ...pyhwUtil import getArch
from .hostInfo import HostInfo
import os


class HostDetectLinux:
    def __init__(self):
        self.__hostInfo = HostInfo()
        self.__arch = getArch()

    def getHostInfo(self):
        self.__getModel()
        return self.__hostInfo

    def __getModel(self):
        if self.__arch in ["x86_64", "x86"]:
            try:
                with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                    product_name = f.read().strip()
                    if product_name.startswith("To be filled by O.E.M."):
                        self.__hostInfo.name = f"General {self.__arch} Host"
                    else:
                        self.__hostInfo.name = product_name
                with open("/sys/devices/virtual/dmi/id/product_version", "r") as f:
                    version = f.read().strip()
                    if version.startswith("To be filled by O.E.M."):
                        self.__hostInfo.version = ""
                    else:
                        self.__hostInfo.version = version
                self.__hostInfo.model = self.__hostInfo.name + " " + self.__hostInfo.version
            except FileNotFoundError:
                pass
        elif self.__arch in ["aarch64", "arm32"]:
            # try to find dmi folder since some arm based desktops and servers may have same structure as x86_64 machines.
            if os.path.exists("/sys/devices/virtual/dmi/id"):
                try:
                    with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                        self.__hostInfo.name = f.read().strip()
                    with open("/sys/devices/virtual/dmi/id/product_version", "r") as f:
                        self.__hostInfo.version = f.read().strip()
                    self.__hostInfo.model = self.__hostInfo.name + " " + self.__hostInfo.version
                except FileNotFoundError:
                    pass
            else:
                # some single board computers may not have dmi folder, try to find model name in device tree.
                try:
                    with open("/sys/firmware/devicetree/base/model", "r") as f:
                        self.__hostInfo.model = f.read().strip()
                except FileNotFoundError:
                    pass

    def __getHostFamily(self):
        pass

    def __getHostProductName(self):
        pass
