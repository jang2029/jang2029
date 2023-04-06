import os
import subprocess
import time
import multiprocessing







def search(dirname):
    
    list = []
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if (ext == '.ma') or (ext == '.mb'):
                mayaFile = path.replace('\\', '/') + '/' + filename
                list.append("C:/Program Files/Autodesk/Maya2022/bin/mayabatch" + " " + mayaFile)
    print (list)            
    procs = []
    for i in list:
        p = multiprocessing.Process(target=scan, args=(i, ))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

def scan(file):

    print('PID :', os.getpid())
    subprocess.run(file)
    print (f'process: {file}')



if __name__ == '__main__':
    filePath = r'D:\projects\eaapexseason17_42048P\assets\3D\character\ash\model\output'
    startTime = time.time()
    search(filePath)
    print(f"Total takes Time {int(time.time()-int(startTime))} second")

