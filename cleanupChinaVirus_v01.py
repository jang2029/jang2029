import os
import subprocess

def search(dirname):
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if (ext == '.ma') or (ext == '.mb'):
                mayaFile = path.replace('\\', '/') + '/' + filename
                
                print(mayaFile)

                subprocess.run(f'"C:/Program Files/Autodesk/Maya2022/bin/mayabatch" "{mayaFile}"')

filePath = input('Type serch folder:')
search(filePath.replace('\\', '/'))

