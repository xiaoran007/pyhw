import pytest
from pyhw.backend.gpu.linux import GPUDetectLinux


def test_gpu_linux_pci(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.linux.getArch", lambda: "x86_64")
    
    class MockDevice:
        def __init__(self):
            self.device_id = "0x1234"
            self.vendor_name = "NVIDIA Corporation"
            self.device_name = "GeForce RTX 3080"
            self.subsystem_device_name = ""
            self.bus = "01"
            self.class_name = ""

    class MockPCIManager:
        def FindAllVGA(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    detector = GPUDetectLinux()
    info = detector.getGPUInfo()
    assert info.number == 1
    assert "NVIDIA GeForce RTX 3080" in info.gpus[0]


def test_gpu_linux_fallback(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.linux.getArch", lambda: "x86_64")
    
    class MockPCIManager:
        def FindAllVGA(self):
            return []

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    detector = GPUDetectLinux()
    info = detector.getGPUInfo()
    assert info.number == 1
    assert "Not found" in info.gpus[0]
