import sys
import site
import os
import urllib.request
import json
import importlib.metadata


class ReleaseChecker:
    """
    Helper Class to check if there is a newer version of the package.
    """
    PACKAGE_NAME = "pyhw"

    def __init__(self):
        """
        Initialize the ReleaseChecker.
        """
        self.isInPIPX = self.__is_running_in_pipx()
        self.CurrentVersion = self.__get_installed_version()
        self.LatestVersion = self.__get_latest_version()

    @staticmethod
    def __is_running_in_pipx():
        return (
            "pipx" in sys.prefix or
            any("pipx" in path for path in site.getsitepackages()) or
            "PIPX_BIN_DIR" in os.environ
        )

    def __get_installed_version(self):
        try:
            return importlib.metadata.version(self.PACKAGE_NAME)
        except importlib.metadata.PackageNotFoundError:
            return None

    def __get_latest_version(self):
        url = f"https://pypi.org/pypi/{self.PACKAGE_NAME}/json"
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                data = json.load(response)
                return data["info"]["version"]
        except Exception:
            return None

    @staticmethod
    def parse_version(version):
        """
        Parse the version string to a tuple of integers.
        :param version: version string
        :return: tuple of integers
        """
        return tuple(map(int, version.split(".")))

    def __is_newer_version(self):
        if self.CurrentVersion is None or self.LatestVersion is None:
            return False
        else:
            return self.parse_version(self.CurrentVersion) < self.parse_version(self.LatestVersion)

    def check_for_updates(self):
        """
        Check if there is a newer version of the package.
        :return: Boolean
        """
        return self.__is_newer_version()

    def check_for_updates_print(self):
        if self.__is_newer_version():
            print(f"🔔 Found newer version: {self.CurrentVersion} (current: {self.LatestVersion})")
            print("👉 You can use the following command to upgrade:")
            if self.isInPIPX:
                print(f"   pipx upgrade {self.PACKAGE_NAME}")
            else:
                print(f"   pip install -U {self.PACKAGE_NAME}")


