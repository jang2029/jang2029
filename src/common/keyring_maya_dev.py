#!/usr/bin/env python

import os

# OS env
os.putenv('PIPELINE_SCRIPT', r'C:\Users\jongtae_han.IT-TD01\pipeline_script')
os.putenv('PROJ_DRIVE', r'Y:')

# Maya env
os.putenv('MAYA_SHELF_PATH', r'C:\Users\jongtae_han.IT-TD01\pipeline_script\maya\2022\prefs\shelves')

# Maya execute
maya2022 = r'"C:\Program Files\Autodesk\Maya2022\bin\maya.exe"'
os.system(maya2022)
