
import os

import multiprocessing as mp

from multiprocessing import Pool




num_cores = mp.cpu_count()
print ('num_cores = ', num_cores) 
pool = Pool(num_cores)

