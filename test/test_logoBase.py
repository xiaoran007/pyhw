import pytest
from pyhw.frontend.logo.logoBase import Logo
from pyhw.pyhwException import LogoNotFoundException


def test_logo_success(monkeypatch):
    class MockFile:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            return "Mocked Logo Content"

    def mock_open(*args, **kwargs):
        return MockFile()

    monkeypatch.setattr("builtins.open", mock_open)
    logo = Logo("ubuntu")
    assert logo.getLogoContent() == "Mocked Logo Content"


def test_logo_not_found(monkeypatch):
    def mock_open(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_open)
    logo = Logo("unknown_os")
    with pytest.raises(LogoNotFoundException):
        logo.getLogoContent()
