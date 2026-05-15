import pytest
from pyhw.backend.npu.windows import NPUDetectWindows

def test_npu_windows(monkeypatch):
    class MockDevice:
        def __init__(self):
            self.vendor_name = "Intel Corporation"
            self.device_name = "NPU"
            self.subsystem_device_name = ""

    class MockPCIManager:
        def FindAllNPU(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    detector = NPUDetectWindows()
    info = detector.getNPUInfo()
    assert info.number == 1
    assert "Intel NPU" in info.npus[0]


def test_npu_windows_pci_subsystem(monkeypatch):
    class MockDevice:
        vendor_name = "Intel Corporation"
        device_name = "NPU"
        subsystem_device_name = "Meteor Lake"

    class MockPCIManager:
        def FindAllNPU(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    info = NPUDetectWindows().getNPUInfo()

    assert info.npus == ["Intel NPU (Meteor Lake)"]


def test_npu_windows_not_found(monkeypatch):
    class MockPCIManager:
        def FindAllNPU(self):
            return []

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())

    info = NPUDetectWindows().getNPUInfo()

    assert info.npus == ["Not found"]
