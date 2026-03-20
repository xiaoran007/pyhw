import pytest
from pyhw.backend.npu.macos import NPUDetectMacOS


def test_npu_macos(monkeypatch):
    class MockCPUInfo:
        model = "Apple M1"
    
    class MockCPUDetect:
        def __init__(self, os):
            pass
        def getCPUInfo(self):
            return MockCPUInfo()
            
    monkeypatch.setattr("pyhw.backend.npu.macos.CPUDetect", MockCPUDetect)
    monkeypatch.setattr("pyhw.backend.npu.macos.getArch", lambda: "aarch64")
    monkeypatch.setattr("pyhw.backend.npu.macos.getOS", lambda: "macos")
    
    detector = NPUDetectMacOS()
    info = detector.getNPUInfo()
    assert info.number == 1
    assert "Apple Neural Engine 16 Cores" in info.npus[0]


def test_npu_macos_intel(monkeypatch):
    class MockCPUInfo:
        model = "Intel Core i9"
    
    class MockCPUDetect:
        def __init__(self, os):
            pass
        def getCPUInfo(self):
            return MockCPUInfo()
            
    monkeypatch.setattr("pyhw.backend.npu.macos.CPUDetect", MockCPUDetect)
    monkeypatch.setattr("pyhw.backend.npu.macos.getArch", lambda: "x86_64")
    monkeypatch.setattr("pyhw.backend.npu.macos.getOS", lambda: "macos")
    
    detector = NPUDetectMacOS()
    info = detector.getNPUInfo()
    assert info.number == 1
    assert "Not Found" in info.npus[0]
