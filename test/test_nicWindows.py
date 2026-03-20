import pytest
from pyhw.backend.nic.windows import NICDetectWindows

def test_nic_windows(monkeypatch):
    class MockDevice:
        def __init__(self):
            self.vendor_name = "Intel Corporation"
            self.device_name = "Wi-Fi 6 AX200"
            self.subsystem_device_name = ""

    class MockPCIManager:
        def FindAllNIC(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    detector = NICDetectWindows()
    info = detector.getNICInfo()
    assert info.number == 1
    assert "Intel Wi-Fi 6 AX200" in info.nics[0]
