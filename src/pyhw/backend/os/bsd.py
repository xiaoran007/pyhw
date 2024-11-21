from .linux import OSDetectLinux


class OSDetectBSD(OSDetectLinux):
    def __init__(self):
        OSDetectLinux.__init__(self)

