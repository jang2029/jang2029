import os, shutil
from fnmatch import fnmatch

list =[]
root = r'P:\projects\eaapexseason17_42048P'.replace('\\', '/')

patternA = "*.ma"
patternB = "*.mb"
count = 0
mayaFile = 0
for path, subdirs, files in os.walk(root):
    for name in files:        
        if fnmatch(name, patternA) or fnmatch(name, patternB):
            count=count+1
            print(f'{count} : {name}')
for path, subdirs, files in os.walk(root):
    for name in files:
        
        if fnmatch(name, patternA) or fnmatch(name, patternB):
            mayaFile=mayaFile+1
            print( f'{mayaFile}/{count} : {name}')
            fileName = (os.path.join(path, name)).replace('\\', '/')
            print(fileName)
            dirpath = (path.replace('\\', '/')).replace('P:', 'D:')
            print(dirpath)
            list.append(fileName)
            if not os.path.isdir(dirpath):
                os.makedirs(dirpath)
            shutil.copy(fileName, fileName.replace('P:', 'D:'))
          


