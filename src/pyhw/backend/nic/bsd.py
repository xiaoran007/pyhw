from .linux import NICDetectLinux


class NICDetectBSD(NICDetectLinux):
    def __init__(self):
        NICDetectLinux.__init__(self)
