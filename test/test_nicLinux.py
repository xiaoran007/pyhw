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


def test_nic_linux_pci_subsystem(monkeypatch):
    class MockDevice:
        vendor_name = "Intel Corporation"
        device_name = "Ethernet"
        subsystem_device_name = "I225-V"

    class MockPCIManager:
        def FindAllNIC(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    info = NICDetectLinux().getNICInfo()

    assert info.nics == ["Intel Ethernet (I225-V)"]


def test_nic_linux_fallback_skips_empty_ip(monkeypatch):
    class MockPCIManager:
        def FindAllNIC(self):
            return []

    class MockProcess:
        stdout = "\n"

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    monkeypatch.setattr(os, "listdir", lambda x: ["eth0"])
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockProcess())

    info = NICDetectLinux().getNICInfo()

    assert info.nics == ["Not found"]


def test_nic_linux_fallback_ignores_command_error(monkeypatch):
    class MockPCIManager:
        def FindAllNIC(self):
            return []

    def mock_run(*args, **kwargs):
        raise RuntimeError("ip failed")

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    monkeypatch.setattr(os, "listdir", lambda x: ["eth0"])
    monkeypatch.setattr(subprocess, "run", mock_run)

    info = NICDetectLinux().getNICInfo()

    assert info.nics == ["Not found"]
