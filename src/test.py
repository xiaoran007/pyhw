from pyhw.backend.host import HostDetect

info = HostDetect("linux").getHostInfo()
print(info)
print(info["model"])
