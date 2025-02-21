"""
    In dev.
"""
from ...pyhwUtil import getArch, getDocker
from .hostInfo import HostInfo
import os


class HostDetectLinux:
    def __init__(self):
        self._hostInfo = HostInfo()
        self._arch = getArch()
        self._docker = getDocker()

    def getHostInfo(self):
        self._getModel()
        return self._hostInfo

    def _getModel(self):
        if self._docker:
            self._hostInfo.name = f"General {self._arch} Docker Host"
            self._hostInfo.version = ""
            self._hostInfo.model = self._hostInfo.name + " " + self._hostInfo.version
        else:
            if self._arch in ["x86_64", "x86"]:
                try:
                    with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                        product_name = f.read().strip()
                        if product_name.startswith("To be filled by O.E.M.") or product_name.startswith("Default string"):
                            self._hostInfo.name = f"General {self._arch} Host"
                        else:
                            self._hostInfo.name = product_name
                    with open("/sys/devices/virtual/dmi/id/product_version", "r") as f:
                        version = f.read().strip()
                        if version.startswith("To be filled by O.E.M.") or product_name.startswith("Default string"):
                            self._hostInfo.version = ""
                        else:
                            self._hostInfo.version = version
                    self._hostInfo.model = self._hostInfo.name + " " + self._hostInfo.version
                except FileNotFoundError:
                    pass
            elif self._arch in ["aarch64", "arm32", "riscv64"]:
                # try to find dmi folder since some arm based desktops and servers may have same structure as x86_64 machines.
                if os.path.exists("/sys/devices/virtual/dmi/id"):
                    try:
                        with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                            self._hostInfo.name = f.read().strip()
                        with open("/sys/devices/virtual/dmi/id/product_version", "r") as f:
                            self._hostInfo.version = f.read().strip()
                        self._hostInfo.model = self._hostInfo.name + " " + self._hostInfo.version
                    except FileNotFoundError:
                        pass
                else:
                    # some single board computers may not have dmi folder, try to find model name in device tree.
                    try:
                        with open("/sys/firmware/devicetree/base/model", "r") as f:
                            self._hostInfo.model = f.read().strip()
                    except FileNotFoundError:
                        pass

    def __getHostFamily(self):
        pass

    def __getHostProductName(self):
        pass
