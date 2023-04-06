import os
import subprocess
import time
from multiprocessing import Process


def search(dirname):
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if (ext == '.ma') or (ext == '.mb'):
                mayaFile = path.replace('\\', '/') + '/' + filename
                
                print(mayaFile)

                subprocess.run(f'"C:/Program Files/Autodesk/Maya2022/bin/mayabatch" "{mayaFile}"')


if __name__ == '__main__':
    # filePath = input('Type serch folder:')
    filePath = r'D:\projects\eaapexseason17_42048P\assets\3D\character\ash\model\output'
    currtime = time.time()
    p = Process(target=search, args=(filePath.replace('\\', '/'),))
    p.start()
    p.join()
    print(f"Total takes Time {int(currtime-time.time())*-1} second")


