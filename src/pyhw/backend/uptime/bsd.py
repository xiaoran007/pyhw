from .macos import UptimeDetectMacOS


class UptimeDetectBSD(UptimeDetectMacOS):
    def __init__(self):
        super().__init__()

