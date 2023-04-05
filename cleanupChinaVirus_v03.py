import os
import subprocess
import time
from multiprocessing import Process



def list_chuck(arr, n):
    return [arr[i: i + n] for i in range(0, len(arr), n)]



def search(dirname):
    list = []
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if (ext == '.ma') or (ext == '.mb'):
                mayaFile = path.replace('\\', '/') + '/' + filename
                list.append("C:/Program Files/Autodesk/Maya2022/bin/mayabatch" + " " + mayaFile)
                
    
    result_array = list_chuck(list, 1)
    print(result_array)

    # try:
    #     p1 = Process(target=scan, args=(result_array[0],))
    #     p1.start(); p1.join()
    # except:
    #     pass

    # try:
    #     p2 = Process(target=scan, args=(result_array[1],))
    #     p2.start(); p2.join()
    # except:
    #     pass

def scan(file):

    print('PID :', os.getpid())
    for i in file:
        subprocess.run(i)




if __name__ == '__main__':
    filePath = r'D:\projects\eaapexseason17_42048P\assets\3D\character\ash\model\output'
    startTime = time.time()
    search(filePath)
    print(f"Total takes Time {time.time()-int(startTime)} second")

