import pytest
import subprocess
import json
from datetime import datetime
from pyhw.backend.uptime.windows import UptimeDetectWindows

def test_uptime_windows(monkeypatch):
    class MockProcessFixed:
        def __init__(self):
            # 1600000000000 ms is a fixed point in time
            self.stdout = json.dumps({
                "LastBootUpTime": f"/Date(1600000000000)/"
            })
            
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockProcessFixed())

    class MockDatetime(datetime):
        @classmethod
        def utcnow(cls):
            # 1 day = 86400, 2 hours = 7200, 3 mins = 180, 4 secs = 4 => 93784 seconds later
            return datetime.utcfromtimestamp(1600000000 + 93784)
    
    monkeypatch.setattr("pyhw.backend.uptime.windows.datetime", MockDatetime)
    
    detector = UptimeDetectWindows()
    info = detector.getUptimeInfo()
    assert info.uptime == "1 days 2 hours 3 mins 4 secs"
