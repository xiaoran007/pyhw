import pytest
import subprocess
import json
from pyhw.backend.memory.windows import MemoryDetectWindows

def test_memory_windows(monkeypatch):
    class MockProcess:
        def __init__(self):
            self.stdout = json.dumps({
                "FreePhysicalMemory": "8388608",
                "TotalVisibleMemorySize": "16777216"
            })

    def mock_run(*args, **kwargs):
        return MockProcess()

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = MemoryDetectWindows()
    info = detector.getMemoryInfo()
    assert info.total == 16.0
    assert info.available == 8.0
    assert info.used == 8.0
