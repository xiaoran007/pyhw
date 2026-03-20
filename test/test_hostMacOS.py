import pytest
from pyhw.backend.host.macos import HostDetectMacOS


def test_host_macos_fallback(monkeypatch):
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    monkeypatch.setattr("pyhw.backend.host.macos.sysctlGetString", lambda x: "MacBookPro18,3")
    
    detector = HostDetectMacOS()
    info = detector.getHostInfo()
    assert info.model == "MacBook Pro (14-inch, 2021)"


def test_host_macos_fallback_other(monkeypatch):
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    monkeypatch.setattr("pyhw.backend.host.macos.sysctlGetString", lambda x: "MacBookAir10,1")
    
    detector = HostDetectMacOS()
    info = detector.getHostInfo()
    assert info.model == "MacBook Air (M1, 2020)"
