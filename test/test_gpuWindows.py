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


def test_gpu_windows_pci_subsystem(monkeypatch):
    class MockDevice:
        vendor_name = "AMD Corporation"
        device_name = "Radeon"
        subsystem_device_name = "Pro"

    class MockPCIManager:
        def FindAllVGA(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    info = GPUDetectWindows().getGPUInfo()

    assert info.gpus == ["AMD Radeon (Pro)"]


def test_gpu_windows_not_found(monkeypatch):
    class MockPCIManager:
        def FindAllVGA(self):
            return []

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    info = GPUDetectWindows().getGPUInfo()

    assert info.number == 1
    assert info.gpus == ["Not found"]
