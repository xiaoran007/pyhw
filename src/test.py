from pyhw.backend.shell import ShellDetect

ans = ShellDetect('linux').getShellInfo()
print(ans.info)

