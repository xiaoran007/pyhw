import pytest
from pyhw.frontend.color.colorConfig import ColorConfigSet


@pytest.mark.parametrize("os_name, expected_title_color", [
    ("macOS", "32"),  # ColorSet.COLOR_FG_GREEN
    ("debian", "31"), # ColorSet.COLOR_FG_RED
    ("linux", "33"),  # ColorSet.COLOR_FG_YELLOW
    ("fedora", "34"), # ColorSet.COLOR_FG_BLUE
    ("fedora_small", "34"),
    ("ubuntu", "31"),
    ("ubuntu_small", "31"),
    ("raspbian", "32"),
    ("armbian", "33"),
    ("alpine", "34"),
    ("arch", "36"),
    ("centos", "33"),
    ("freebsd", "31"),
    ("windows_old", "32"),
    ("windows_10", "32"),
    ("windows_11", "36"),
    ("windows_2025", "36"),
    ("kali", "32"),
    ("linuxmint", "32"),
    ("opensuse-leap", "32"),
    ("opensuse-tumbleweed", "32"),
    ("rhel", "31"),
    ("unknown_os", "33"),  # default to Linux
])
def test_getColorConfigSet(os_name, expected_title_color):
    config = ColorConfigSet(os_name).getColorConfigSet()
    assert config["colorTitle"] == expected_title_color
    assert "colors" in config
    assert "colorKeys" in config
