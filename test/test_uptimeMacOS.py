import pytest
import subprocess
from pyhw.backend.uptime.macos import UptimeDetectMacOS


def test_uptime_macos(monkeypatch):
    monkeypatch.setattr("pyhw.backend.uptime.macos.sysctlGetString", lambda x: "sec = 1600000000, usec = 0")
    
    def mock_check_output(*args, **kwargs):
        # 1 day = 86400, 2 hours = 7200, 3 mins = 180, 4 secs = 4 => 93784
        return b"1600093784\n"
        
    monkeypatch.setattr(subprocess, "check_output", mock_check_output)
    
    detector = UptimeDetectMacOS()
    info = detector.getUptimeInfo()
    assert info.uptime == "1 days 2 hours 3 mins 4 secs"


def test_uptime_macos_no_days(monkeypatch):
    monkeypatch.setattr("pyhw.backend.uptime.macos.sysctlGetString", lambda x: "sec = 1600000000, usec = 0")
    
    def mock_check_output(*args, **kwargs):
        # 2 hours = 7200, 3 mins = 180, 4 secs = 4 => 7384
        return b"1600007384\n"
        
    monkeypatch.setattr(subprocess, "check_output", mock_check_output)
    
    detector = UptimeDetectMacOS()
    info = detector.getUptimeInfo()
    assert info.uptime == "2 hours 3 mins 4 secs"
