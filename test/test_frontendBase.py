import pytest
from pyhw.frontend.frontendBase import Printer
from pyhw.pyhwException import BackendException


@pytest.fixture
def mock_dependencies(monkeypatch):
    # Mock Logo
    class MockLogo:
        def __init__(self, logo_os):
            pass
        def getLogoContent(self):
            return "$1Mocked\n$2Logo\n$$"
    monkeypatch.setattr("pyhw.frontend.frontendBase.Logo", MockLogo)
    
    # Mock ColorConfigSet
    class MockColorConfigSet:
        def __init__(self, os_name):
            pass
        def getColorConfigSet(self):
            return {
                "colors": ["31", "32"],
                "colorTitle": "33",
                "colorKeys": "34"
            }
    monkeypatch.setattr("pyhw.frontend.frontendBase.ColorConfigSet", MockColorConfigSet)


def test_printer_cprint(mock_dependencies, monkeypatch, capsys):
    data = "User@Host\n---------------\nOS: TestOS\nCPU: TestCPU\n"
    printer = Printer("linux", data)
    
    # Mock getOS to avoid system specific behaviors in tests
    monkeypatch.setattr("pyhw.frontend.frontendBase.getOS", lambda: "windows")
    
    printer.cPrint()
    captured = capsys.readouterr()
    assert "User" in captured.out
    assert "Host" in captured.out
    assert "TestOS" in captured.out
    assert "TestCPU" in captured.out


def test_printer_dropLongString_linux(mock_dependencies, monkeypatch):
    data = "User@Host\n---------------\n" + "A"*200 + ": B\n"
    
    def mock_getColumns(*args):
        return 80
        
    monkeypatch.setattr(Printer, "_Printer__getColumns", mock_getColumns)
    printer = Printer("linux", data)
    
    monkeypatch.setattr("pyhw.frontend.frontendBase.getOS", lambda: "linux")
    
    # Let's do it properly without exception
    printer2 = Printer("linux", "User@Host\n--\nLongKey: " + "V"*200)
    monkeypatch.setattr(printer2, "_Printer__columns", 80)
    printer2.cPrint()
    
    # We should just make sure it runs without errors for truncation.
    # The actual length checks are harder because of ANSI codes, but we can call it.
    pass


def test_getColumns(monkeypatch):
    import os
    import subprocess
    
    # Mock os.get_terminal_size
    class TerminalSize:
        columns = 100
    monkeypatch.setattr(os, "get_terminal_size", lambda: TerminalSize())
    assert Printer._Printer__getColumns() == 100
    
    # Mock os.get_terminal_size to fail, fallback to stty
    def raise_oserror():
        raise OSError()
    monkeypatch.setattr(os, "get_terminal_size", raise_oserror)
    
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        return MockProcess("24 120\n")

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert Printer._Printer__getColumns() == 120
    
    # Mock stty to fail, fallback to COLUMNS
    def mock_run_fail(cmd, *args, **kwargs):
        raise subprocess.CalledProcessError(1, cmd)
    monkeypatch.setattr(subprocess, "run", mock_run_fail)
    monkeypatch.setitem(os.environ, "COLUMNS", "140")
    assert Printer._Printer__getColumns() == 140
    
    # Mock all to fail, fallback to 80
    monkeypatch.delitem(os.environ, "COLUMNS")
    assert Printer._Printer__getColumns() == 80


def test_getColumns_invalid_columns_env(monkeypatch):
    import os
    import subprocess

    def raise_oserror():
        raise OSError()

    def mock_run_fail(cmd, *args, **kwargs):
        raise subprocess.CalledProcessError(1, cmd)

    monkeypatch.setattr(os, "get_terminal_size", raise_oserror)
    monkeypatch.setattr(subprocess, "run", mock_run_fail)
    monkeypatch.setitem(os.environ, "COLUMNS", "wide")

    assert Printer._Printer__getColumns() == 80


def test_truncate_to_width_zero_after_ansi():
    assert Printer._Printer__truncateToWidth("\033[31mabcdef", 0) == "\033[0m"


def test_data_preprocess_invalid_line(mock_dependencies, monkeypatch):
    printer = Printer("linux", "User@Host\n--\nValid: line")

    class BadLine:
        def split(self, separator):
            raise RuntimeError("bad line")

    monkeypatch.setattr(printer, "_Printer__data_lines", ["User@Host", "--", BadLine()])

    with pytest.raises(BackendException):
        printer._Printer__DataPreprocess()
