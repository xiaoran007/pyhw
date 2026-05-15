from pyhw.backend.cpu.bsd import CPUDetectBSD
from pyhw.backend.gpu.bsd import GPUDetectBSD
from pyhw.backend.host.bsd import HostDetectBSD
from pyhw.backend.memory.bsd import MemoryDetectBSD
from pyhw.backend.nic.bsd import NICDetectBSD
from pyhw.backend.npu.bsd import NPUDetectBSD
from pyhw.backend.os.bsd import OSDetectBSD
from pyhw.backend.uptime.bsd import UptimeDetectBSD


def test_cpu_bsd(monkeypatch):
    monkeypatch.setattr("pyhw.backend.cpu.bsd.sysctlGetString", lambda key: "BSD CPU")

    info = CPUDetectBSD().getCPUInfo()

    assert info.cpu == "BSD CPU"


def test_memory_bsd(monkeypatch):
    values = {
        "hw.pagesize": 4096,
        "hw.physmem": 8 * 1024 * 1024 * 1024,
        "vm.stats.vm.v_free_count": 512 * 1024,
    }

    monkeypatch.setattr("pyhw.backend.memory.bsd.sysctlGetInt", lambda key: values[key])

    info = MemoryDetectBSD().getMemoryInfo()

    assert info.total == 8
    assert info.used == 6
    assert info.memory == "6.0 GiB / 8.0 GiB"


def test_host_bsd(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "x86_64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)

    info = HostDetectBSD().getHostInfo()

    assert info.name == "General x86_64 FreeBSD Host"
    assert info.model == "General x86_64 FreeBSD Host "


def test_bsd_inherited_detector_constructors():
    assert isinstance(GPUDetectBSD(), GPUDetectBSD)
    assert isinstance(NICDetectBSD(), NICDetectBSD)
    assert isinstance(NPUDetectBSD(), NPUDetectBSD)
    assert isinstance(OSDetectBSD(), OSDetectBSD)
    assert isinstance(UptimeDetectBSD(), UptimeDetectBSD)
