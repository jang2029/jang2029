

import os
import csv
''' 
-- TYPE --
    bg
    character
    prop 
    
'''


bgPath = r'P:\projects\eaapexseason17_42048P\assets\3D\bg'
characterPath = r'P:\projects\eaapexseason17_42048P\assets\3D\character'
propPath = r'P:\projects\eaapexseason17_42048P\assets\3D\prop'

bgDirectoryList = os.listdir(bgPath)
characterDirectoryList = os.listdir(characterPath)
propDirectoryList = os.listdir(propPath)

bgList = [a for a in bgDirectoryList if os.path.isdir((bgPath+'\\'+a))]
characterList = [a for a in characterDirectoryList if os.path.isdir((characterPath+'\\'+a))]
propList = [a for a in propDirectoryList if os.path.isdir((propPath+'\\'+a))]

f = open(r'P:\projects\eaapexseason17_42048P\assets\3D\asset_list.csv','w', newline='')
wr = csv.writer(f)
for i in bgList:
    wr.writerow(['bg',i])
for i in characterList:
    wr.writerow(['character',i])
for i in propList:
    wr.writerow(['prop',i])

f.close()

