from .linux import OSDetectLinux


class OSDetectBSD(OSDetectLinux):
    def __init__(self):
        super().__init__()

