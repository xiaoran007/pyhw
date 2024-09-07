from .nicInfo import NICInfo


class NICDetectMacOS:
    def __init__(self):
        self.__nicInfo = NICInfo()

    def getNICInfo(self):
        self.__nicInfo.nics.append("en0")
        self.__nicInfo.number = 1
        return self.__nicInfo
