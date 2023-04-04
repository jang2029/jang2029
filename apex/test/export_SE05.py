
import maya.cmds as cmds
import json


# Bake_Set 선택

selected = cmds.ls(selection = True)
cmds.select(selected)
# 선택된 오브젝트의 쉐이더 선택

cmds.hyperShade (smn = True)



# 쉐이딩그룹 이름 정리하여 바꾸기

selected = cmds.ls(selection = True)

for i in selected:
    sg = cmds.listConnections(i ,type = 'shadingEngine')
    cmds.rename (sg, i+'_SG')



# 쉐이딩그룹 파일로 내보내기

print (selected)
cmds.select(selected)
shaders = cmds.ls( selection=True)
shadingGroups = cmds.listConnections( shaders,type = 'shadingEngine')
print (shadingGroups)

cmds.select(shadingGroups, ne=True, r=True )


filename =  cmds.file(query=True, sceneName=True, shortName=True)
fullpath =  cmds.file(query=True, sceneName=True)
path = fullpath.replace(filename, '')
savefilename = filename.replace('.mb', '')+'_SD'


cmds.file (path+savefilename, typ='mayaBinary', es=True )