from pyhw.backend.host import HostDetect
from pyhw.backend.title import TitleDetect

ans = TitleDetect('linux').getTitle()
print(ans.title)
