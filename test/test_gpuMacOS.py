import pytest
import json
import subprocess
from pyhw.backend.gpu.macos import GPUDetectMacOS


class _CallableBytes:
    def __init__(self, value):
        self.value = value
        self.restype = None

    def __call__(self):
        return self.value


def test_gpu_macos_apple_silicon_fallback(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "aarch64")
    
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    def mock_check_output(*args, **kwargs):
        return json.dumps({
            "SPDisplaysDataType": [
                {"sppci_model": "Apple M1", "sppci_cores": "8"}
            ]
        }).encode('utf-8')
    monkeypatch.setattr(subprocess, "check_output", mock_check_output)
    
    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()
    assert info.number == 1
    assert "Apple M1 (8 Cores) [SOC Integrated]" in info.gpus[0]


def test_gpu_macos_intel_fallback(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "x86_64")
    
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    def mock_check_output(*args, **kwargs):
        return json.dumps({
            "SPDisplaysDataType": [
                {"sppci_model": "Intel UHD Graphics 630", "spdisplays_vendor": "sppci_vendor_intel"},
                {"sppci_model": "Radeon Pro 5500M", "spdisplays_vendor": "sppci_vendor_amd", "spdisplays_vram": "4 GB"}
            ]
        }).encode('utf-8')
    monkeypatch.setattr(subprocess, "check_output", mock_check_output)
    
    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()
    assert info.number == 2
    assert "Intel UHD Graphics 630 [CPU Integrated]" in info.gpus
    assert "Radeon Pro 5500M 4 GB [Discrete]" in info.gpus


def test_gpu_macos_apple_silicon_iokit_success(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "aarch64")

    class MockLib:
        getAppleSiliconGPUInfo = _CallableBytes(b"10")

    class MockCPUDetect:
        def __init__(self, os):
            self.os = os

        def getCPUInfo(self):
            return type("CPUInfo", (), {"model": "Apple M2"})()

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())
    monkeypatch.setattr("pyhw.backend.gpu.macos.CPUDetect", MockCPUDetect)

    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()

    assert info.number == 1
    assert info.gpus == ["Apple M2 (10 Cores) [SOC Integrated]"]


def test_gpu_macos_apple_silicon_iokit_zero_fallback_no_profiler_key(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "aarch64")

    class MockLib:
        getAppleSiliconGPUInfo = _CallableBytes(b"0")

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())
    monkeypatch.setattr(subprocess, "check_output", lambda *args, **kwargs: json.dumps({}).encode("utf-8"))

    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()

    assert info.number == 0
    assert info.gpus == []


def test_gpu_macos_apple_silicon_profiler_exception(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "aarch64")

    class MockLib:
        getAppleSiliconGPUInfo = _CallableBytes(b"0")

    def mock_check_output(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0])

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())
    monkeypatch.setattr(subprocess, "check_output", mock_check_output)

    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()

    assert info.number == 0


def test_gpu_macos_intel_iokit_success(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "x86_64")

    class MockLib:
        getGPUInfo = _CallableBytes(b"Intel UHD, 0x8086, 1536; Radeon Pro, 0x1002, 4096")

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())

    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()

    assert info.number == 2
    assert info.gpus == ["Intel UHD [CPU Integrated]", "Radeon Pro 4 GB [Discrete]"]


def test_gpu_macos_intel_iokit_error_fallback_no_profiler_key(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "x86_64")

    class MockLib:
        getGPUInfo = _CallableBytes(b"Error; missing")

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())
    monkeypatch.setattr(subprocess, "check_output", lambda *args, **kwargs: json.dumps({}).encode("utf-8"))

    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()

    assert info.number == 0


def test_gpu_macos_intel_profiler_exception(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "x86_64")
    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: (_ for _ in ()).throw(Exception()))

    def mock_check_output(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0])

    monkeypatch.setattr(subprocess, "check_output", mock_check_output)

    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()

    assert info.number == 0


def test_gpu_macos_intel_fallback_ignores_nvidia(monkeypatch):
    monkeypatch.setattr("pyhw.backend.gpu.macos.getArch", lambda: "x86_64")
    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: (_ for _ in ()).throw(Exception()))

    monkeypatch.setattr(
        subprocess,
        "check_output",
        lambda *args, **kwargs: json.dumps({
            "SPDisplaysDataType": [
                {"sppci_model": "GeForce GT", "spdisplays_vendor": "Nvidia"}
            ]
        }).encode("utf-8"),
    )

    detector = GPUDetectMacOS()
    info = detector.getGPUInfo()

    assert info.number == 1
    assert info.gpus == []


def test_gpu_macos_vendor_helpers():
    assert GPUDetectMacOS._GPUDetectMacOS__handleVendor("sppci_vendor_Apple") == "Apple"
    assert GPUDetectMacOS._GPUDetectMacOS__handleVendor("unknown") == "unknown"
    assert GPUDetectMacOS._GPUDetectMacOS__handleVendorID("0xbeef") == "0xbeef"
