
import os, sys
import subprocess
import time
import multiprocessing as mp
from multiprocessing import Pool


class cleanup():

    def __init__(self):

        super().__init__()
        self.body()
        input(input('END....press Enter'))



    def body(self):



        print('\n\n')
        dirname = input('Type serch folder:')
        
        if not os.path.isdir(dirname):
            print('\n\n')
            print('wrong Path!!')
            sys.exit(0)

        # mayaVersion = input('Type maya version( Maya2018, Maya2022):')
        mayaVersion = 'Maya2018'
        startTime = time.time()
        # if (mayaVersion == 'Maya2022') or (mayaVersion == 'Maya2018'):
        #     mayaVersion = 'Maya2018'
        # else:
        #     print('wrong version!!')
        #     sys.exit(0)

        subprocess.run(f'"C:/Program Files/Autodesk/{mayaVersion}/bin/mayabatch.exe" -command "loadPlugin MayaScanner; loadPlugin MayaScannerCB;"')

        list = []
        for (path, dir, files) in os.walk(dirname):
            for filename in files:
                ext = os.path.splitext(filename)[-1]
                if (ext == '.ma') or (ext == '.mb'):
                    mayaFile = path.replace('\\', '/') + '/' + filename
                    list.append("C:/Program Files/Autodesk/" + mayaVersion + "/bin/maya.exe -batch -file " + mayaFile)
        print (list)

        result_array = self.list_chuck(list, 16)
        print (result_array)
        print (len(result_array))
        
        
        num_cores = mp.cpu_count()
        print ('num_cores = ', num_cores) 
        pool = Pool(num_cores)
        pool.map(self.scan, list)

        print('\n\n')

        print(f"Total {len(list)} Files Checked")
        print(f"Total takes Time {int(time.time()-int(startTime))} second")


    def scan(self, file):

        print('\n\n')        
        print('PID :', os.getpid())
        print (f'process: {file}')
        subprocess.run(file)


    def list_chuck(self,arr, n):
        return [arr[i: i + n] for i in range(0, len(arr), n)]



if __name__ == '__main__':

    cleanup()
