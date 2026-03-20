import pytest
import os
from pyhw.backend.cpu.linux import CPUDetectLinux


def test_cpu_linux_normal(monkeypatch):
    def mock_exists(path):
        return path == "/sys/devices/system/cpu/cpu0/cpufreq"

    monkeypatch.setattr(os.path, "exists", mock_exists)

    class MockFile:
        def __init__(self, filename):
            self.filename = filename
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            if "cpuinfo" in self.filename:
                return "model name      : Intel(R) Core(TM) i7 CPU\nprocessor       : 0\nprocessor       : 1"
            elif "scaling_max_freq" in self.filename:
                return "2400000"
            return ""

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    detector = CPUDetectLinux()
    info = detector.getCPUInfo()
    assert info.model == "Intel Core i7 CPU"
    assert info.cores == 2
    assert info.frequency == "2.4 Ghz"


def test_cpu_linux_sbc(monkeypatch):
    def mock_exists(path):
        return path == "/sys/firmware/devicetree/base/compatible"

    monkeypatch.setattr(os.path, "exists", mock_exists)

    class MockFile:
        def __init__(self, filename):
            self.filename = filename
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            if "cpuinfo" in self.filename:
                return "processor : 0"
            elif "compatible" in self.filename:
                return "raspberrypi,bcm2835"
            return ""

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    detector = CPUDetectLinux()
    info = detector.getCPUInfo()
    assert info.model == "BCM2835"
    assert info.cores == 1


def test_cpu_linux_error(monkeypatch):
    def mock_exists(path):
        return False

    monkeypatch.setattr(os.path, "exists", mock_exists)

    def mock_open_error(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_open_error)

    detector = CPUDetectLinux()
    info = detector.getCPUInfo()
    assert info.model == "Unknown"
