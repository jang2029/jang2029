
import os, sys, csv
import subprocess
import time
import multiprocessing




def scan(file):
    
    print('PID :', os.getpid())
    print (f'process: {file}')
    subprocess.run(file)
    



def list_chuck(arr, n):
    return [arr[i: i + n] for i in range(0, len(arr), n)]


def serchMayafile(dirname, mayaVersion):    
    
    subprocess.run(f'"C:/Program Files/Autodesk/{mayaVersion}/bin/mayabatch.exe" -command "loadPlugin MayaScanner; loadPlugin MayaScannerCB;"')
    list = []
    for (path, dir, files) in os.walk(dirname):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if (ext == '.ma') or (ext == '.mb'):
                mayaFile = path.replace('\\', '/') + '/' + filename
                list.append("C:/Program Files/Autodesk/" + mayaVersion + "/bin/maya.exe -batch -file " + mayaFile)
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


def main():

    print('\n\n')
    dirname = input('Type serch folder:')
    if not os.path.isdir(dirname):
        print('\n\n')
        print('wrong Path!!')
        sys.exit(0)


    # mayaVersion = input('Type maya version( Maya2018, Maya2022):')
    mayaVersion = 'Maya2022'
    startTime = time.time()
    if (mayaVersion == 'Maya2022') or (mayaVersion == 'Maya2018'):
        serchMayafile(dirname, mayaVersion)
    else:
        print('wrong version!!')
        sys.exit(0)

    print(f"Total takes Time {int(time.time()-int(startTime))} second")
    


if __name__ == '__main__':
    
    main()


