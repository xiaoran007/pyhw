import pytest
import sys
import site
import os
import json
from unittest.mock import MagicMock
from pyhw.pyhwUtil.cliUtil import ReleaseChecker


@pytest.mark.parametrize("sys_prefix, site_packages, env_vars, expected", [
    ("pipx", [], {}, True),
    ("normal_prefix", ["/some/path/pipx"], {}, True),
    ("normal_prefix", [], {"PIPX_BIN_DIR": "/some/dir"}, True),
    ("normal_prefix", [], {}, False)
])
def test_is_running_in_pipx(sys_prefix, site_packages, env_vars, expected, monkeypatch):
    monkeypatch.setattr(sys, "prefix", sys_prefix)
    monkeypatch.setattr(site, "getsitepackages", lambda: site_packages)
    monkeypatch.setattr(os, "environ", env_vars)

    checker = ReleaseChecker()
    assert checker.isInPIPX == expected


@pytest.fixture
def mock_installed_version(monkeypatch):
    def mock_version(package_name):
        return "0.10.1" if package_name == "pyhw" else None

    monkeypatch.setattr("importlib.metadata.version", mock_version)


def test_get_installed_version(mock_installed_version):
    checker = ReleaseChecker()
    assert checker.CurrentVersion == "0.10.1"


@pytest.fixture
def mock_pypi_response(monkeypatch):
    mock_response = MagicMock()
    mock_response.__enter__.return_value = mock_response
    mock_response.read.return_value = json.dumps({"info": {"version": "0.11.0"}}).encode()

    monkeypatch.setattr("urllib.request.urlopen", lambda *args, **kwargs: mock_response)


def test_get_latest_version(mock_pypi_response):
    checker = ReleaseChecker()
    assert checker.LatestVersion == "0.11.0"


@pytest.mark.parametrize("version, expected", [
    ("0.10.1", (0, 10, 1)),
    ("1.2.3", (1, 2, 3)),
    ("2.0.0", (2, 0, 0)),
    ("3.11.22", (3, 11, 22))
])
def test_parse_version(version, expected):
    assert ReleaseChecker.parse_version(version) == expected


@pytest.mark.parametrize("installed, latest, expected", [
    ("0.10.1", "0.11.0", True),
    ("0.11.0", "0.11.0", False),
    ("0.12.0", "0.11.0", False),
    (None, "0.11.0", False),
    ("0.10.1", None, False)
])
def test_is_newer_version(installed, latest, expected, monkeypatch):
    monkeypatch.setattr(ReleaseChecker, "_ReleaseChecker__get_installed_version", lambda self: installed)
    monkeypatch.setattr(ReleaseChecker, "_ReleaseChecker__get_latest_version", lambda self: latest)

    checker = ReleaseChecker()
    assert checker.check_for_updates() == expected
