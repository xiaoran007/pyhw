from ...pyhwException import OSUnsupportedException


class FoundationModelsDetect:
    def __init__(self, os):
        self.OS = os

    def getFoundationModelsInfo(self):
        if self.OS == "macos":
            from .macos import FoundationModelsDetectMacOS
            return FoundationModelsDetectMacOS().getFoundationModelsInfo()
        raise OSUnsupportedException("Foundation Models detection requires macOS")
