import pytest
import subprocess
import json
from datetime import datetime
from pyhw.backend.uptime.windows import UptimeDetectWindows
from pyhw.pyhwException import BackendException

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


@pytest.mark.parametrize(
    "elapsed_seconds, expected",
    [
        (125, "2 mins 5 secs"),
        (3725, "1 hours 2 mins 5 secs"),
    ],
)
def test_uptime_windows_same_day_formats(monkeypatch, elapsed_seconds, expected):
    class MockProcessFixed:
        stdout = json.dumps({"LastBootUpTime": "/Date(1600000000000)/"})

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockProcessFixed())

    class MockDatetime(datetime):
        @classmethod
        def utcnow(cls):
            return datetime.utcfromtimestamp(1600000000 + elapsed_seconds)

    monkeypatch.setattr("pyhw.backend.uptime.windows.datetime", MockDatetime)

    info = UptimeDetectWindows().getUptimeInfo()

    assert info.uptime == expected


def test_uptime_windows_subprocess_error(monkeypatch):
    def mock_run(*args, **kwargs):
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run)

    with pytest.raises(BackendException):
        UptimeDetectWindows().getUptimeInfo()


def test_uptime_windows_missing_timestamp(monkeypatch):
    class MockProcess:
        stdout = json.dumps({"LastBootUpTime": "missing"})

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockProcess())

    with pytest.raises(BackendException):
        UptimeDetectWindows().getUptimeInfo()
