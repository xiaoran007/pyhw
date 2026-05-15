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


def test_cpu_linux_model_with_inline_frequency(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda path: False)

    class MockFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            return "model name      : AMD Ryzen @ 3.80GHz\nprocessor       : 0"

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())

    info = CPUDetectLinux().getCPUInfo()

    assert info.model == "AMD Ryzen"
    assert info.frequency == "3.80GHz"


def test_cpu_linux_cpufreq_file_missing(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda path: path == "/sys/devices/system/cpu/cpu0/cpufreq")

    class MockFile:
        def __init__(self, filename):
            self.filename = filename

        def __enter__(self):
            if "scaling_max_freq" in self.filename:
                raise FileNotFoundError()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            return "model name      : Intel CPU\nprocessor       : 0"

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    info = CPUDetectLinux().getCPUInfo()

    assert info.frequency == ""


@pytest.mark.parametrize(
    "line, expected",
    [
        ("cpu MHz         : 2400.000", "2.4 Ghz"),
        ("clock           : 1200 MHz", "1.2 Ghz"),
        ("clock           : 1.5 GHz", "1.5 Ghz"),
        ("clock           : 900 bogomips", "0.9 Ghz"),
    ],
)
def test_cpu_linux_frequency_from_cpuinfo(monkeypatch, line, expected):
    monkeypatch.setattr(os.path, "exists", lambda path: False)

    class MockFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            return f"model name      : Generic CPU\n{line}\nprocessor       : 0"

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())

    info = CPUDetectLinux().getCPUInfo()

    assert info.frequency == expected


def test_cpu_linux_sbc_compatible_file_missing(monkeypatch):
    monkeypatch.setattr(os.path, "exists", lambda path: path == "/sys/firmware/devicetree/base/compatible")

    class MockFile:
        def __init__(self, filename):
            self.filename = filename

        def __enter__(self):
            if "compatible" in self.filename:
                raise FileNotFoundError()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            return "model name      : Generic CPU\nprocessor       : 0"

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    info = CPUDetectLinux().getCPUInfo()

    assert info.model == "Generic CPU"


@pytest.mark.parametrize(
    "compatible, expected_model",
    [
        ("orangepi,allwinner,sun50i-h616", "Allwinner H616 (sun50i-h616)"),
        ("cvitek,cv1800b", "Cvitek cv1800b"),
    ],
)
def test_cpu_linux_sbc_other_vendors(monkeypatch, compatible, expected_model):
    monkeypatch.setattr(os.path, "exists", lambda path: path == "/sys/firmware/devicetree/base/compatible")

    class MockFile:
        def __init__(self, filename):
            self.filename = filename

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            if "compatible" in self.filename:
                return compatible
            return "processor       : 0"

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    info = CPUDetectLinux().getCPUInfo()

    assert info.model == expected_model
