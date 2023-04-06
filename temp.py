

import subprocess

mayaVersion = 'Maya2022'
# subprocess.run(f'"C:/Program Files/Autodesk/{mayaVersion}/bin/mayabatch.exe" -command "loadPlugin MayaScanner"')
# subprocess.run(f'"C:/Program Files/Autodesk/{mayaVersion}/bin/mayabatch.exe" -command "loadPlugin MayaScannerCB"')
subprocess.run(f'"C:/Program Files/Autodesk/{mayaVersion}/bin/mayabatch.exe" -command "loadPlugin MayaScanner; loadPlugin MayaScannerCB;"')