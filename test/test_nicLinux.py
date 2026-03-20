import pytest
import os
import subprocess
from pyhw.backend.nic.linux import NICDetectLinux


def test_nic_linux_pci(monkeypatch):
    class MockDevice:
        def __init__(self):
            self.vendor_name = "Intel"
            self.device_name = "Ethernet"
            self.subsystem_device_name = ""
            
    class MockPCIManager:
        def FindAllNIC(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    detector = NICDetectLinux()
    info = detector.getNICInfo()
    assert info.number == 1
    assert "Intel Ethernet" in info.nics[0]


def test_nic_linux_fallback(monkeypatch):
    class MockPCIManager:
        def FindAllNIC(self):
            return []
    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    monkeypatch.setattr(os, "listdir", lambda x: ["lo", "eth0"])
    
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout
            
    def mock_run(cmd, *args, **kwargs):
        if "eth0" in cmd[2]:
            return MockProcess("192.168.1.100\n")
        return MockProcess("")
        
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    detector = NICDetectLinux()
    info = detector.getNICInfo()
    assert info.number == 1
    assert "eth0 @ 192.168.1.100" in info.nics[0]


def test_nic_linux_fallback_error(monkeypatch):
    class MockPCIManager:
        def FindAllNIC(self):
            return []
    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    
    monkeypatch.setattr(os, "listdir", lambda x: ["lo"])
    
    detector = NICDetectLinux()
    info = detector.getNICInfo()
    assert info.number == 1
    assert "Not found" in info.nics[0]
