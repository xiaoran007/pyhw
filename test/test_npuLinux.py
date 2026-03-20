import pytest
import os
from pyhw.backend.npu.linux import NPUDetectLinux


def test_npu_linux_pci(monkeypatch):
    class MockDevice:
        def __init__(self):
            self.vendor_name = "Intel"
            self.device_name = "NPU"
            self.subsystem_device_name = ""
            
    class MockPCIManager:
        def FindAllNPU(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    detector = NPUDetectLinux()
    info = detector.getNPUInfo()
    assert info.number == 1
    assert "Intel NPU" in info.npus[0]


def test_npu_linux_fallback(monkeypatch):
    class MockPCIManager:
        def FindAllNPU(self):
            return []
    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    monkeypatch.setattr(os.path, "exists", lambda x: "tpu" in x)
    
    class MockFile:
        def __init__(self, filename):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            return "cvitek,cv1800b"
            
    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))
    
    detector = NPUDetectLinux()
    info = detector.getNPUInfo()
    assert info.number == 1
    assert "Cvitek cv1800b" in info.npus[0]


def test_npu_linux_fallback_not_found(monkeypatch):
    class MockPCIManager:
        def FindAllNPU(self):
            return []
    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    monkeypatch.setattr(os.path, "exists", lambda x: False)
    
    detector = NPUDetectLinux()
    info = detector.getNPUInfo()
    assert info.number == 1
    assert "Not found" in info.npus[0]
