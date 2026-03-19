import pytest
from pyhw.backend.uptime.linux import UptimeDetectLinux


def test_uptime_linux_days(monkeypatch):
    class MockFile:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def readline(self):
            # 1 day, 2 hours, 3 minutes, 4 seconds = 86400 + 7200 + 180 + 4 = 93784
            return "93784.12 123456.78\n"

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    detector = UptimeDetectLinux()
    info = detector.getUptimeInfo()
    
    assert info.uptime == "1 days 2 hours 3 mins 4 secs"


def test_uptime_linux_hours(monkeypatch):
    class MockFile:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def readline(self):
            # 2 hours, 3 minutes, 4 seconds = 7200 + 180 + 4 = 7384
            return "7384.12 123456.78\n"

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    detector = UptimeDetectLinux()
    info = detector.getUptimeInfo()
    
    assert info.uptime == "2 hours 3 mins 4 secs"


def test_uptime_linux_minutes(monkeypatch):
    class MockFile:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def readline(self):
            # 3 minutes, 4 seconds = 180 + 4 = 184
            return "184.12 123456.78\n"

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())
    
    detector = UptimeDetectLinux()
    info = detector.getUptimeInfo()
    
    assert info.uptime == "3 mins 4 secs"
