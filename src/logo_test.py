from pyhw.frontend import Printer
from pyhw.backend import Data
from pyhw.pyhwUtil import createDataString, selectOSLogo


data = Data()
data.title = "xiaoran@007"

Printer(logo_os=selectOSLogo("rhel"), data=createDataString(data)).cPrint()
