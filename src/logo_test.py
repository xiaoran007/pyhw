from pyhw.frontend import Printer
from pyhw.backend import Data
from pyhw.pyhwUtil import createDataString


data = Data()
data.title = "xiaoran@007"

Printer(logo_os="macOS", data=createDataString(data)).cPrint()