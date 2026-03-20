import pytest
from pyhw.backend.gpu.windows import GPUDetectWindows

def test_gpu_windows_pci(monkeypatch):
    class MockDevice:
        def __init__(self):
            self.vendor_name = "NVIDIA Corporation"
            self.device_name = "GeForce RTX 4090"
            self.subsystem_device_name = ""

    class MockPCIManager:
        def FindAllVGA(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    detector = GPUDetectWindows()
    info = detector.getGPUInfo()
    assert info.number == 1
    assert "NVIDIA GeForce RTX 4090" in info.gpus[0]
