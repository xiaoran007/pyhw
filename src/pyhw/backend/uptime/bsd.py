from .macos import UptimeDetectMacOS


class UptimeDetectBSD(UptimeDetectMacOS):
    def __init__(self):
        UptimeDetectMacOS.__init__(self)
