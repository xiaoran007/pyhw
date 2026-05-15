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


def test_npu_macos_private_placeholders():
    detector = NPUDetectMacOS()

    detector._NPUDetectMacOS__getNPUAppleSilicon()
    detector._NPUDetectMacOS__getNPUIntel()

    assert detector._NPUDetectMacOS__npuInfo.npus == [
        "Apple Neural Engine [SOC Integrated]",
        "Not Found",
    ]
    assert detector._NPUDetectMacOS__npuInfo.number == 2


@pytest.mark.parametrize(
    "vendor, expected",
    [
        ("sppci_vendor_Apple", "Apple"),
        ("sppci_vendor_intel", "Intel"),
        ("sppci_vendor_amd", "AMD"),
        ("other", "other"),
    ],
)
def test_npu_macos_vendor_helper(vendor, expected):
    assert NPUDetectMacOS._NPUDetectMacOS__handleVendor(vendor) == expected
