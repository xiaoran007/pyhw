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


def test_cpu_windows_name_without_at(monkeypatch):
    class MockProcess:
        stdout = json.dumps({
            "Name": "AMD Ryzen 9",
            "NumberOfLogicalProcessors": 24,
            "MaxClockSpeed": 4200,
        })

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockProcess())

    info = CPUDetectWindows().getCPUInfo()

    assert info.model == "AMD Ryzen 9"
    assert info.cpu == "AMD Ryzen 9 (24) @ 4.20 GHz"


def test_cpu_windows_subprocess_error(monkeypatch):
    def mock_run(*args, **kwargs):
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run)

    with pytest.raises(SystemExit):
        CPUDetectWindows().getCPUInfo()


def test_cpu_windows_empty_model_becomes_unknown(monkeypatch):
    monkeypatch.setattr(CPUDetectWindows, "_CPUDetectWindows__getCPUInfo", lambda self: None)

    info = CPUDetectWindows().getCPUInfo()

    assert info.model == "Unknown"
    assert info.cpu == "Unknown"
