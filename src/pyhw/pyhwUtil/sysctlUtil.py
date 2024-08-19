import subprocess


def sysctlGet(key):
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
