from .linux import NICDetectLinux


class NICDetectBSD(NICDetectLinux):
    def __init__(self):
        super().__init__()

