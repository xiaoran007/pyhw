from .linux import NPUDetectLinux


class NPUDetectBSD(NPUDetectLinux):
    def __init__(self):
        NPUDetectLinux.__init__(self)
