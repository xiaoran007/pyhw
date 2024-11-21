from .linux import NPUDetectLinux


class NPUDetectBSD(NPUDetectLinux):
    def __init__(self):
        super().__init__()

