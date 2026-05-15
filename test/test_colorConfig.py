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
    ("almalinux", "31"),
    ("artix", "36"),
    ("alpine", "34"),
    ("arch", "36"),
    ("cachyos", "36"),
    ("centos", "33"),
    ("deepin", "34"),
    ("elementary", "39"),
    ("endeavouros", "31"),
    ("freebsd", "31"),
    ("garuda", "31"),
    ("gentoo", "35"),
    ("windows_old", "32"),
    ("windows_10", "32"),
    ("windows_11", "36"),
    ("windows_2025", "36"),
    ("kali", "32"),
    ("linuxmint", "32"),
    ("manjaro", "32"),
    ("nixos", "36"),
    ("nobara", "39"),
    ("openbsd", "39"),
    ("opensuse-leap", "32"),
    ("opensuse-tumbleweed", "32"),
    ("oracle", "39"),
    ("pop", "36"),
    ("rhel", "31"),
    ("rocky", "32"),
    ("solus", "39"),
    ("void", "32"),
    ("zorin", "34"),
    ("unknown_os", "33"),  # default to Linux
])
def test_getColorConfigSet(os_name, expected_title_color):
    config = ColorConfigSet(os_name).getColorConfigSet()
    assert config["colorTitle"] == expected_title_color
    assert "colors" in config
    assert "colorKeys" in config
