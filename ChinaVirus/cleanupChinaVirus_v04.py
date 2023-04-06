import os, sys
import subprocess
import time
import multiprocessing


def list_chuck(arr, n):
    return [arr[i: i + n] for i in range(0, len(arr), n)]


def serchMayafile(dirname, mayaVersion):

    subprocess.run(f'"C:/Program Files/Autodesk/{mayaVersion}/bin/mayabatch.exe" -command "loadPlugin MayaScanner" -command "loadPlugin MayaScannerCB"')
    list = []
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if (ext == '.ma') or (ext == '.mb'):
                mayaFile = path.replace('\\', '/') + '/' + filename
                list.append("C:/Program Files/Autodesk/" + mayaVersion + "/bin/mayabatch" + " " + mayaFile)
    print (list)

    result_array = list_chuck(list, 16)
    print (result_array)
    print (len(result_array))
    for a in result_array:
        procs = []
        for i in a:
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

    print('\n\n')
    dirname = input('Type serch folder:')
    if not os.path.isdir(dirname):
        print('\n\n')
        print('\033[95m'+'wrong Path!!' + '\033[0m')
        sys.exit(0)


    mayaVersion = input('Type maya version( Maya2018, Maya2022):')
    startTime = time.time()
    if (mayaVersion == 'Maya2022') or (mayaVersion == 'Maya2018'):
        serchMayafile(dirname, mayaVersion)
    else:
        print('\033[95m'+'wrong version!!' + '\033[0m')
        sys.exit(0)

    print('\033[96m' + f"Total takes Time {int(time.time()-int(startTime))} second" + '\033[0m')






