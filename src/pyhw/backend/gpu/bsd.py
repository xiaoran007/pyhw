from .linux import GPUDetectLinux


class GPUDetectBSD(GPUDetectLinux):
    def __init__(self):
        super().__init__()

