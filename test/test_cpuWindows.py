import pytest
import subprocess
import json
from pyhw.backend.cpu.windows import CPUDetectWindows

def test_cpu_windows(monkeypatch):
    class MockProcess:
        def __init__(self):
            self.stdout = json.dumps({
                "Name": "Intel(R) Core(TM) i9 CPU @ 3.50GHz",
                "NumberOfLogicalProcessors": 16,
                "MaxClockSpeed": 3500
            })

    def mock_run(*args, **kwargs):
        return MockProcess()

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = CPUDetectWindows()
    info = detector.getCPUInfo()
    assert info.model == "Intel Core i9 CPU"
    assert info.cores == "16"
    assert info.frequency == "3.50 GHz"
