import pytest
import json
import subprocess
from pyhw.backend.gpu.macos import GPUDetectMacOS


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
