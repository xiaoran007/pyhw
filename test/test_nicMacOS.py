import pytest
import subprocess
from pyhw.backend.nic.macos import NICDetectMacOS


def test_nic_macos_fallback_wired(monkeypatch):
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    class MockProcess:
        def __init__(self, stdout, returncode=0):
            self.stdout = stdout
            self.returncode = returncode
            
    def mock_run(cmd, *args, **kwargs):
        cmd_str = " ".join(cmd)
        if "route get default" in cmd_str:
            return MockProcess("interface: en0\n")
        elif "ipconfig getifaddr" in cmd_str:
            return MockProcess("192.168.1.100\n")
        elif "networksetup -getairportpower" in cmd_str:
            return MockProcess("", returncode=1) # Not wifi
        elif "networksetup -getmedia" in cmd_str:
            return MockProcess("Active: 1000Base-T <full-duplex>\n")
        return MockProcess("")

    monkeypatch.setattr(subprocess, "run", mock_run)
    
    detector = NICDetectMacOS()
    info = detector.getNICInfo()
    assert info.number == 1
    assert "en0 @ 192.168.1.100 - Wired (1 Gbps)" in info.nics[0]


def test_nic_macos_fallback_wifi(monkeypatch):
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    class MockProcess:
        def __init__(self, stdout, returncode=0):
            self.stdout = stdout
            self.returncode = returncode
            
    def mock_run(cmd, *args, **kwargs):
        cmd_str = " ".join(cmd)
        if "route get default" in cmd_str:
            return MockProcess("interface: en0\n")
        elif "ipconfig getifaddr" in cmd_str:
            return MockProcess("192.168.1.100\n")
        elif "networksetup -getairportpower" in cmd_str:
            return MockProcess("On", returncode=0) # Wifi
        elif "system_profiler SPAirPortDataType" in cmd_str:
            import json
            return MockProcess(json.dumps({
                "SPAirPortDataType": [{
                    "spairport_airport_interfaces": [{
                        "_name": "en0",
                        "spairport_current_network_information": {
                            "spairport_network_rate": "866",
                            "spairport_network_channel": "149 (5GHz, 80MHz)"
                        }
                    }]
                }]
            }))
        return MockProcess("")

    monkeypatch.setattr(subprocess, "run", mock_run)
    
    detector = NICDetectMacOS()
    info = detector.getNICInfo()
    assert info.number == 1
    assert "en0 @ 192.168.1.100 - Wi-Fi 5GHz (866 Mbps)" in info.nics[0]


def test_nic_macos_error(monkeypatch):
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    def mock_run_error(*args, **kwargs):
        raise Exception()

    monkeypatch.setattr(subprocess, "run", mock_run_error)
    
    detector = NICDetectMacOS()
    info = detector.getNICInfo()
    assert info.number == 1
    assert "en0 - Unknown connection" in info.nics[0]
