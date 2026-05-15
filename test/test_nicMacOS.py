import pytest
import json
import subprocess
from pyhw.backend.nic.macos import NICDetectMacOS


class _Callable:
    def __init__(self, func):
        self.func = func
        self.argtypes = None
        self.restype = None

    def __call__(self, *args):
        return self.func(*args)


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


def test_nic_macos_iokit_wifi_success(monkeypatch):
    class MockLib:
        def __init__(self):
            self.getDefaultInterface = _Callable(self._get_default_interface)
            self.getNetworkInfo = _Callable(self._get_network_info)

        def _get_default_interface(self, interface):
            interface.value = b"en0"
            return True

        def _get_network_info(self, interface, is_wifi, ip_address, speed, band, channel, conn_type, wifi_standard):
            is_wifi._obj.value = True
            ip_address.value = b"192.168.1.10"
            speed._obj.value = 1200
            band.value = b"6GHz"
            channel.value = b"37"
            conn_type.value = b"Wi-Fi"
            wifi_standard.value = b"802.11ax"
            return True

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())

    detector = NICDetectMacOS()
    info = detector.getNICInfo()

    assert info.number == 1
    assert info.nics == ["en0 @ 192.168.1.10 - Wi-Fi (802.11ax 6GHz 1200 Mbps)"]


def test_nic_macos_iokit_wired_success(monkeypatch):
    class MockLib:
        def __init__(self):
            self.getDefaultInterface = _Callable(self._get_default_interface)
            self.getNetworkInfo = _Callable(self._get_network_info)

        def _get_default_interface(self, interface):
            interface.value = b"en1"
            return True

        def _get_network_info(self, interface, is_wifi, ip_address, speed, band, channel, conn_type, wifi_standard):
            is_wifi._obj.value = False
            ip_address.value = b"10.0.0.8"
            conn_type.value = b"Ethernet"
            return True

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())

    detector = NICDetectMacOS()
    info = detector.getNICInfo()

    assert info.nics == ["en1 @ 10.0.0.8 - Ethernet"]


@pytest.mark.parametrize("default_result, network_result", [(False, True), (True, False)])
def test_nic_macos_iokit_failure_falls_back(monkeypatch, default_result, network_result):
    class MockLib:
        def __init__(self):
            self.getDefaultInterface = _Callable(self._get_default_interface)
            self.getNetworkInfo = _Callable(self._get_network_info)

        def _get_default_interface(self, interface):
            interface.value = b"en0"
            return default_result

        def _get_network_info(self, *args):
            return network_result

    class MockProcess:
        def __init__(self, stdout, returncode=0):
            self.stdout = stdout
            self.returncode = returncode

    def mock_run(cmd, *args, **kwargs):
        cmd_str = " ".join(cmd)
        if "route get default" in cmd_str:
            return MockProcess("interface: en0\n")
        if "ipconfig getifaddr" in cmd_str:
            return MockProcess("192.168.1.100\n")
        if "networksetup -getairportpower" in cmd_str:
            return MockProcess("", returncode=1)
        if "networksetup -getmedia" in cmd_str:
            return MockProcess("Active: 100Base-T <full-duplex>\n")
        return MockProcess("")

    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: MockLib())
    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = NICDetectMacOS()
    info = detector.getNICInfo()

    assert info.nics == ["en0 @ 192.168.1.100 - Wired (100 Mbps)"]


@pytest.mark.parametrize(
    "media, expected",
    [
        ("Active: 2500Base-T <full-duplex>\n", "Wired (2.5 Gbps)"),
        ("Active: 100Base-T <full-duplex>\n", "Wired (100 Mbps)"),
        ("Active: 10000Base-T <full-duplex>\n", "Wired (10 Gbps)"),
        ("Active: 5000Base-T <full-duplex>\n", "Wired (5.0 Gbps)"),
        ("Active: 10Base-T <full-duplex>\n", "Wired (10 Mbps)"),
        ("Active: FastBase-T <full-duplex>\n", "Wired (FastBase-T)"),
    ],
)
def test_nic_macos_wired_speed_parsing(monkeypatch, media, expected):
    monkeypatch.setattr("ctypes.CDLL", lambda *args, **kwargs: (_ for _ in ()).throw(Exception()))

    class MockProcess:
        def __init__(self, stdout, returncode=0):
            self.stdout = stdout
            self.returncode = returncode

    def mock_run(cmd, *args, **kwargs):
        cmd_str = " ".join(cmd)
        if "networksetup -getairportpower" in cmd_str:
            return MockProcess("", returncode=1)
        if "networksetup -getmedia" in cmd_str:
            return MockProcess(media)
        return MockProcess("")

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = NICDetectMacOS()

    assert detector._NICDetectMacOS__getLinkInfo("en0") == expected


def test_nic_macos_link_info_exception(monkeypatch):
    def mock_run(*args, **kwargs):
        raise RuntimeError("networksetup failed")

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = NICDetectMacOS()

    assert detector._NICDetectMacOS__getLinkInfo("en0") == "Unknown connection type"


@pytest.mark.parametrize(
    "channel, expected_band",
    [
        ("6 (2GHz, 20MHz)", "2.4GHz"),
        ("5 (6GHz, 160MHz)", "6GHz"),
    ],
)
def test_nic_macos_wifi_band_parsing(monkeypatch, channel, expected_band):
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: MockProcess(json.dumps({
            "SPAirPortDataType": [{
                "spairport_airport_interfaces": [{
                    "_name": "en0",
                    "spairport_current_network_information": {
                        "spairport_network_rate": "144",
                        "spairport_network_channel": channel,
                    },
                }]
            }]
        })),
    )

    detector = NICDetectMacOS()

    assert detector._NICDetectMacOS__getWifiInfo("en0") == ("144", channel, expected_band)


def test_nic_macos_wifi_info_unknown_when_interface_missing(monkeypatch):
    class MockProcess:
        stdout = json.dumps({"SPAirPortDataType": [{"spairport_airport_interfaces": []}]})

    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: MockProcess())

    detector = NICDetectMacOS()

    assert detector._NICDetectMacOS__getWifiInfo("en0") == ("Unknown", "Unknown", "Unknown")


def test_nic_macos_wifi_info_exception(monkeypatch):
    def mock_run(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], timeout=5)

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = NICDetectMacOS()

    assert detector._NICDetectMacOS__getWifiInfo("en0") == ("Unknown", "Unknown", "Unknown")
