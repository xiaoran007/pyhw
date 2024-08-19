import subprocess


def __sysctlGet(key):
    """
    Get value from sysctl by key.
    :param key: str, sysctl key
    :return: value of sysctl key or "" if not found
    """
    try:
        output = subprocess.run(["sysctl", "-n", key], capture_output=True, text=True).stdout.strip()
    except subprocess.SubprocessError:
        output = ""
    return output


def sysctlGetString(key):
    """
    Get value from sysctl by key.
    :param key: str, sysctl key
    :return: value of sysctl key or "" if not found
    """
    return __sysctlGet(key)


def sysctlGetInt(key):
    """
    Get value from sysctl by key.
    :param key: str, sysctl key
    :return: value of sysctl key as int or None if not found
    """
    value = __sysctlGet(key)
    try:
        res = int(value)
    except Exception:
        res = None
    return res
