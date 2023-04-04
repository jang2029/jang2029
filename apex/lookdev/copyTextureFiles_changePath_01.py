import maya.cmds as cmds
import os, shutil, stat
import re


  #텍스쳐파일 복사
wip_texture_path = r'D:\projects\eaapexseason17_42048P\assets\3D\bg\bloodhound\shade\work\maya\textures'
if not os.path.isdir(wip_texture_path):
    os.makedirs(wip_texture_path)
        
for i in cmds.file(query=True, list=True):
    filename = i.split('.')
    if not filename[-1] in ['', 'mb', 'ma', 'abc']:
        #print (i+' copyed to '+wip_texture_path)
        newName = i.split('/')
        newName = (wip_texture_path+'\\' + newName[-1])
        if os.path.isfile(newName):
            print(newName+' 지웡')
            os.chmod( newName, stat.S_IWRITE )
            os.remove(newName)
            
        shutil.copy(i, newName)


        
# 파일경로 바꾸기
fileNodes = cmds.ls(type='file')

for fileNode in fileNodes:
    orgPath = cmds.getAttr(fileNode+'.fileTextureName')
    texture_name = re.split('/', orgPath)
    texture_name = texture_name[-1]
    print (texture_name)
    newName = (wip_texture_path+'/' + texture_name)
    cmds.setAttr(fileNode+'.fileTextureName', newName, type ='string' )
    
