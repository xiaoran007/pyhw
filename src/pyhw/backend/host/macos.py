"""
    In dev.
"""
from .hostInfo import HostInfo
from ...pyhwUtil import sysctlGetString
import ctypes
from pathlib import Path


class HostDetectMacOS:
    def __init__(self):
        self.__hostInfo = HostInfo()
        self.__HWModel = ""

    def getHostInfo(self):
        if not self.__getHostInfoIOKit():
            # if IOKit fails, fallback to sysctl
            self.__getHWModel()
            self.__hostInfo.model = self.__handleMacName(self.__HWModel)
        return self.__hostInfo

    def __getHostInfoIOKit(self):
        try:
            package_root = Path(__file__).resolve().parent.parent.parent
            lib = ctypes.CDLL(f"{package_root}/library/lib/iokitHostLib.dylib")
            lib.getHostInfo.restype = ctypes.c_char_p
            host_info = lib.getHostInfo()
            product_name = host_info.decode('utf-8').split("; ")
            # If the first element is "Error", it means that the library failed to get the product name.
            # Fall back to sysctl.
            if product_name[0] == "Error":
                return False
            self.__hostInfo.model = product_name[0]
            return True
        except Exception as e:
            # print(f"An error occurred while getting GPU info using IOKit: {e}")
            return False

    def __getHWModel(self):
        self.__HWModel = sysctlGetString("hw.model")

    def __handleMacName(self, hw_model: str):
        # This part of the code is directly re-implemented from the fastfetch project. It seems that there is no
        # more elegant way to get the product name of the Mac.
        # See https://github.com/fastfetch-cli/fastfetch/blob/dev/src/detection/host/host_apple.c for more details.
        if hw_model.startswith("MacBookPro"):
            version = hw_model[len("MacBookPro"):]
            if self.__hwModelCheck(version, "18,3") or self.__hwModelCheck(version, "18,4"):
                return "MacBook Pro (14-inch, 2021)"
            if self.__hwModelCheck(version, "18,1") or self.__hwModelCheck(version, "18,2"):
                return "MacBook Pro (16-inch, 2021)"
            if self.__hwModelCheck(version, "17,1"):
                return "MacBook Pro (13-inch, M1, 2020)"
            if self.__hwModelCheck(version, "16,3"):
                return "MacBook Pro (13-inch, 2020, Two Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "16,2"):
                return "MacBook Pro (13-inch, 2020, Four Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "16,4") or self.__hwModelCheck(version, "16,1"):
                return "MacBook Pro (16-inch, 2019)"
            if self.__hwModelCheck(version, "15,4"):
                return "MacBook Pro (13-inch, 2019, Two Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "15,3"):
                return "MacBook Pro (15-inch, 2019)"
            if self.__hwModelCheck(version, "15,2"):
                return "MacBook Pro (13-inch, 2018/2019, Four Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "15,1"):
                return "MacBook Pro (15-inch, 2018/2019)"
            if self.__hwModelCheck(version, "14,3"):
                return "MacBook Pro (15-inch, 2017)"
            if self.__hwModelCheck(version, "14,2"):
                return "MacBook Pro (13-inch, 2017, Four Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "14,1"):
                return "MacBook Pro (13-inch, 2017, Two Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "13,3"):
                return "MacBook Pro (15-inch, 2016)"
            if self.__hwModelCheck(version, "13,2"):
                return "MacBook Pro (13-inch, 2016, Four Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "13,1"):
                return "MacBook Pro (13-inch, 2016, Two Thunderbolt 3 ports)"
            if self.__hwModelCheck(version, "12,1"):
                return "MacBook Pro (Retina, 13-inch, Early 2015)"
            if self.__hwModelCheck(version, "11,4") or self.__hwModelCheck(version, "11,5"):
                return "MacBook Pro (Retina, 15-inch, Mid 2015)"
            if self.__hwModelCheck(version, "11,2") or self.__hwModelCheck(version, "11,3"):
                return "MacBook Pro (Retina, 15-inch, Late 2013/Mid 2014)"
            if self.__hwModelCheck(version, "11,1"):
                return "MacBook Pro (Retina, 13-inch, Late 2013/Mid 2014)"
            if self.__hwModelCheck(version, "10,2"):
                return "MacBook Pro (Retina, 13-inch, Late 2012/Early 2013)"
            if self.__hwModelCheck(version, "10,1"):
                return "MacBook Pro (Retina, 15-inch, Mid 2012/Early 2013)"
            if self.__hwModelCheck(version, "9,2"):
                return "MacBook Pro (13-inch, Mid 2012)"
            if self.__hwModelCheck(version, "9,1"):
                return "MacBook Pro (15-inch, Mid 2012)"
            if self.__hwModelCheck(version, "8,3"):
                return "MacBook Pro (17-inch, 2011)"
            if self.__hwModelCheck(version, "8,2"):
                return "MacBook Pro (15-inch, 2011)"
            if self.__hwModelCheck(version, "8,1"):
                return "MacBook Pro (13-inch, 2011)"
            if self.__hwModelCheck(version, "7,1"):
                return "MacBook Pro (13-inch, Mid 2010)"
            if self.__hwModelCheck(version, "6,2"):
                return "MacBook Pro (15-inch, Mid 2010)"
            if self.__hwModelCheck(version, "6,1"):
                return "MacBook Pro (17-inch, Mid 2010)"
            if self.__hwModelCheck(version, "5,5"):
                return "MacBook Pro (13-inch, Mid 2009)"
            if self.__hwModelCheck(version, "5,3"):
                return "MacBook Pro (15-inch, Mid 2009)"
            if self.__hwModelCheck(version, "5,2"):
                return "MacBook Pro (17-inch, Mid/Early 2009)"
            if self.__hwModelCheck(version, "5,1"):
                return "MacBook Pro (15-inch, Late 2008)"
            if self.__hwModelCheck(version, "4,1"):
                return "MacBook Pro (17/15-inch, Early 2008)"
        elif hw_model.startswith("MacBookAir"):
            version = hw_model[len("MacBookAir"):]
            if self.__hwModelCheck(version, "10,1"):
                return "MacBook Air (M1, 2020)"
            if self.__hwModelCheck(version, "9,1"):
                return "MacBook Air (Retina, 13-inch, 2020)"
            if self.__hwModelCheck(version, "8,2"):
                return "MacBook Air (Retina, 13-inch, 2019)"
            if self.__hwModelCheck(version, "8,1"):
                return "MacBook Air (Retina, 13-inch, 2018)"
            if self.__hwModelCheck(version, "7,2"):
                return "MacBook Air (13-inch, Early 2015/2017)"
            if self.__hwModelCheck(version, "7,1"):
                return "MacBook Air (11-inch, Early 2015)"
            if self.__hwModelCheck(version, "6,2"):
                return "MacBook Air (13-inch, Mid 2013/Early 2014)"
            if self.__hwModelCheck(version, "6,1"):
                return "MacBook Air (11-inch, Mid 2013/Early 2014)"
            if self.__hwModelCheck(version, "5,2"):
                return "MacBook Air (13-inch, Mid 2012)"
            if self.__hwModelCheck(version, "5,1"):
                return "MacBook Air (11-inch, Mid 2012)"
            if self.__hwModelCheck(version, "4,2"):
                return "MacBook Air (13-inch, Mid 2011)"
            if self.__hwModelCheck(version, "4,1"):
                return "MacBook Air (11-inch, Mid 2011)"
            if self.__hwModelCheck(version, "3,2"):
                return "MacBook Air (13-inch, Late 2010)"
            if self.__hwModelCheck(version, "3,1"):
                return "MacBook Air (11-inch, Late 2010)"
            if self.__hwModelCheck(version, "2,1"):
                return "MacBook Air (Mid 2009)"

        elif hw_model.startswith("Macmini"):
            version = hw_model[len("Macmini"):]
            if self.__hwModelCheck(version, "9,1"):
                return "Mac mini (M1, 2020)"
            if self.__hwModelCheck(version, "8,1"):
                return "Mac mini (2018)"
            if self.__hwModelCheck(version, "7,1"):
                return "Mac mini (Mid 2014)"
            if self.__hwModelCheck(version, "6,1") or self.__hwModelCheck(version, "6,2"):
                return "Mac mini (Late 2012)"
            if self.__hwModelCheck(version, "5,1") or self.__hwModelCheck(version, "5,2"):
                return "Mac mini (Mid 2011)"
            if self.__hwModelCheck(version, "4,1"):
                return "Mac mini (Mid 2010)"
            if self.__hwModelCheck(version, "3,1"):
                return "Mac mini (Early/Late 2009)"

        elif hw_model.startswith("MacBook"):
            version = hw_model[len("MacBook"):]
            if self.__hwModelCheck(version, "10,1"):
                return "MacBook (Retina, 12-inch, 2017)"
            if self.__hwModelCheck(version, "9,1"):
                return "MacBook (Retina, 12-inch, Early 2016)"
            if self.__hwModelCheck(version, "8,1"):
                return "MacBook (Retina, 12-inch, Early 2015)"
            if self.__hwModelCheck(version, "7,1"):
                return "MacBook (13-inch, Mid 2010)"
            if self.__hwModelCheck(version, "6,1"):
                return "MacBook (13-inch, Late 2009)"
            if self.__hwModelCheck(version, "5,2"):
                return "MacBook (13-inch, Early/Mid 2009)"

        elif hw_model.startswith("MacPro"):
            version = hw_model[len("MacPro"):]
            if self.__hwModelCheck(version, "7,1"):
                return "Mac Pro (2019)"
            if self.__hwModelCheck(version, "6,1"):
                return "Mac Pro (Late 2013)"
            if self.__hwModelCheck(version, "5,1"):
                return "Mac Pro (Mid 2010 - Mid 2012)"
            if self.__hwModelCheck(version, "4,1"):
                return "Mac Pro (Early 2009)"

        elif hw_model.startswith("Mac"):
            version = hw_model[len("Mac"):]
            if self.__hwModelCheck(version, "16,3"):
                return "iMac (24-inch, 2024, Four Thunderbolt / USB 4 ports)"
            if self.__hwModelCheck(version, "16,2"):
                return "iMac (24-inch, 2024, Two Thunderbolt / USB 4 ports)"
            if self.__hwModelCheck(version, "16,1") or self.__hwModelCheck(version, "16,6") or self.__hwModelCheck(version, "16,8"):
                return "MacBook Pro (14-inch, 2024, Three Thunderbolt 4 ports)"
            if self.__hwModelCheck(version, "16,5") or self.__hwModelCheck(version, "16,7"):
                return "MacBook Pro (16-inch, 2024, Three Thunderbolt 4 ports)"
            if self.__hwModelCheck(version, "16,10") or self.__hwModelCheck(version, "16,15"):
                return "Mac mini (M4, 2024)"
            if self.__hwModelCheck(version, "15,13"):
                return "MacBook Air (15-inch, M3, 2024)"
            if self.__hwModelCheck(version, "15,2"):
                return "MacBook Air (13-inch, M3, 2024)"
            if self.__hwModelCheck(version, "15,3"):
                return "MacBook Pro (14-inch, Nov 2023, Two Thunderbolt / USB 4 ports)"
            if self.__hwModelCheck(version, "15,4"):
                return "iMac (24-inch, 2023, Two Thunderbolt / USB 4 ports)"
            if self.__hwModelCheck(version, "15,5"):
                return "iMac (24-inch, 2023, Two Thunderbolt / USB 4 ports, Two USB 3 ports)"
            if self.__hwModelCheck(version, "15,6") or self.__hwModelCheck(version, "15,8") or self.__hwModelCheck(version, "15,10"):
                return "MacBook Pro (14-inch, Nov 2023, Three Thunderbolt 4 ports)"
            if self.__hwModelCheck(version, "15,7") or self.__hwModelCheck(version, "15,9") or self.__hwModelCheck(version, "15,11"):
                return "MacBook Pro (16-inch, Nov 2023, Three Thunderbolt 4 ports)"
            if self.__hwModelCheck(version, "14,15"):
                return "MacBook Air (15-inch, M2, 2023)"
            if self.__hwModelCheck(version, "14,14"):
                return "Mac Studio (M2 Ultra, 2023, Two Thunderbolt 4 front ports)"
            if self.__hwModelCheck(version, "14,13"):
                return "Mac Studio (M2 Max, 2023, Two USB-C front ports)"
            if self.__hwModelCheck(version, "14,8"):
                return "Mac Pro (2023)"
            if self.__hwModelCheck(version, "14,6") or self.__hwModelCheck(version, "14,10"):
                return "MacBook Pro (16-inch, 2023)"
            if self.__hwModelCheck(version, "14,5") or self.__hwModelCheck(version, "14,9"):
                return "MacBook Pro (14-inch, 2023)"
            if self.__hwModelCheck(version, "14,3"):
                return "Mac mini (M2, 2023, Two Thunderbolt 4 ports)"
            if self.__hwModelCheck(version, "14,12"):
                return "Mac mini (M2, 2023, Four Thunderbolt 4 ports)"
            if self.__hwModelCheck(version, "14,7"):
                return "MacBook Pro (13-inch, M2, 2022)"
            if self.__hwModelCheck(version, "14,2"):
                return "MacBook Air (M2, 2022)"
            if self.__hwModelCheck(version, "13,1"):
                return "Mac Studio (M1 Max, 2022, Two USB-C front ports)"
            if self.__hwModelCheck(version, "13,2"):
                return "Mac Studio (M1 Ultra, 2022, Two Thunderbolt 4 front ports)"

        elif hw_model.startswith("iMac"):
            version = hw_model[len("iMac"):]
            if self.__hwModelCheck(version, "21,1"):
                return "iMac (24-inch, M1, 2021, Two Thunderbolt / USB 4 ports, Two USB 3 ports)"
            if self.__hwModelCheck(version, "21,2"):
                return "iMac (24-inch, M1, 2021, Two Thunderbolt / USB 4 ports)"
            if self.__hwModelCheck(version, "20,1") or self.__hwModelCheck(version, "20,2"):
                return "iMac (Retina 5K, 27-inch, 2020)"
            if self.__hwModelCheck(version, "19,1"):
                return "iMac (Retina 5K, 27-inch, 2019)"
            if self.__hwModelCheck(version, "19,2"):
                return "iMac (Retina 4K, 21.5-inch, 2019)"
            if self.__hwModelCheck(version, "Pro1,1"):
                return "iMac Pro (2017)"
            if self.__hwModelCheck(version, "18,3"):
                return "iMac (Retina 5K, 27-inch, 2017)"
            if self.__hwModelCheck(version, "18,2"):
                return "iMac (Retina 4K, 21.5-inch, 2017)"
            if self.__hwModelCheck(version, "18,1"):
                return "iMac (21.5-inch, 2017)"
            if self.__hwModelCheck(version, "17,1"):
                return "iMac (Retina 5K, 27-inch, Late 2015)"
            if self.__hwModelCheck(version, "16,2"):
                return "iMac (Retina 4K, 21.5-inch, Late 2015)"
            if self.__hwModelCheck(version, "16,1"):
                return "iMac (21.5-inch, Late 2015)"
            if self.__hwModelCheck(version, "15,1"):
                return "iMac (Retina 5K, 27-inch, Late 2014 - Mid 2015)"
            if self.__hwModelCheck(version, "14,4"):
                return "iMac (21.5-inch, Mid 2014)"
            if self.__hwModelCheck(version, "14,2"):
                return "iMac (27-inch, Late 2013)"
            if self.__hwModelCheck(version, "14,1"):
                return "iMac (21.5-inch, Late 2013)"
            if self.__hwModelCheck(version, "13,2"):
                return "iMac (27-inch, Late 2012)"
            if self.__hwModelCheck(version, "13,1"):
                return "iMac (21.5-inch, Late 2012)"
            if self.__hwModelCheck(version, "12,2"):
                return "iMac (27-inch, Mid 2011)"
            if self.__hwModelCheck(version, "12,1"):
                return "iMac (21.5-inch, Mid 2011)"
            if self.__hwModelCheck(version, "11,3"):
                return "iMac (27-inch, Mid 2010)"
            if self.__hwModelCheck(version, "11,2"):
                return "iMac (21.5-inch, Mid 2010)"
            if self.__hwModelCheck(version, "10,1"):
                return "iMac (27/21.5-inch, Late 2009)"
            if self.__hwModelCheck(version, "9,1"):
                return "iMac (24/20-inch, Early 2009)"

        return hw_model

    @staticmethod
    def __hwModelCheck(version: str, target: str):
        return version == target
