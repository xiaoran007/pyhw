import pytest
from pyhw.backend.gpu.linux import GPUDetectLinux


class _CallableCoreCount:
    argtypes = None
    restype = None

    def __call__(self, bus_id):
        return 8704


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


def test_gpu_linux_pci_subsystem_and_nvml(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.linux.getArch", lambda: "x86_64")

    class MockDevice:
        def __init__(self, device_id, subsystem):
            self.device_id = device_id
            self.vendor_name = "NVIDIA Corporation"
            self.device_name = "GeForce"
            self.subsystem_device_name = subsystem
            self.bus = "01"
            self.class_name = ""

    class MockPCIManager:
        def FindAllVGA(self):
            return [MockDevice("0x1234", "Founders Edition"), MockDevice("0x1234", "Founders Edition")]

    class MockLib:
        GetGPUCoreCountByPciBusId = _CallableCoreCount()

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())

    info = GPUDetectLinux().getGPUInfo()

    assert info.number == 2
    assert info.gpus == [
        "NVIDIA GeForce [Founders Edition] (8704 Cores)",
        "NVIDIA GeForce [Founders Edition] (8704 Cores)",
    ]


def test_gpu_linux_blank_device_name_uses_class_name(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.linux.getArch", lambda: "x86_64")

    class MockDevice:
        device_id = "0x1234"
        vendor_name = ""
        device_name = ""
        subsystem_device_name = ""
        bus = "01"
        class_name = "Display controller"

    class MockPCIManager:
        def FindAllVGA(self):
            return [MockDevice()]

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: (_ for _ in ()).throw(Exception()))

    info = GPUDetectLinux().getGPUInfo()

    assert info.gpus == ["Display controller"]


def test_gpu_linux_sbc_fallback(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.linux.getArch", lambda: "aarch64")

    class MockPCIManager:
        def FindAllVGA(self):
            return []

    class MockCPUDetect:
        def __init__(self, os):
            self.os = os

        def getCPUInfo(self):
            return type("CPUInfo", (), {"model": "BCM2711"})()

    monkeypatch.setattr("pyhw.pyhwUtil.PCIManager.get_instance", lambda: MockPCIManager())
    monkeypatch.setattr("pyhw.backend.gpu.linux.CPUDetect", MockCPUDetect)

    info = GPUDetectLinux().getGPUInfo()

    assert info.gpus == ["BCM2711 [SOC Integrated]"]
