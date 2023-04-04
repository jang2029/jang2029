
import maya.cmds as cmds
import json



assetName = 'Ballistic'
abcfileName = r'D:\test\Ballistic_mod_v00.abc'
sdFileName = r'D:\test\Ballistic_mod_v00_SD.mb'
sdJsonFileName = r'D:\test\Ballistic_mod_v00_SD.json'




# 쉐이터 파일불러오기, Abc 파일 읽어 오기, 셋그룹만들기
cmds.file(sdFileName, i = True, ignoreVersion = True, ra = True, mergeNamespacesOnClash = True, namespace = ":", options = "v=0",  pr = True,  importTimeRange = "combine" )
cmds.group( em=True, name=assetName )
groupName = cmds.ls(selection =True)
print (groupName)
cmds.AbcImport (abcfileName, reparent = groupName[0])
cmds.select (groupName, hierarchy=True)
cmds.select (groupName, d=True)
cmds.sets( name = 'attatchSet_' + assetName )


cmds.select ('attatchSet_'+ assetName, r=True, add=True)
objlist = cmds.ls(sl=True,type='geometryShape' )
for i in objlist:
    cmds.setAttr(i+'.displayColors', 0)

# json 파일 읽어 오고 쉐이더 등록
with open(sdJsonFileName, 'r', encoding='utf-8') as file:
    diclistSD = json.load(file)

for i in diclistSD:
    data = diclistSD[i]
    for t in data:
        if cmds.ls(t):
            cmds.select(t, add=1)
        else:
            print ('no Objects = '+t)
    print (i)
    cmds.sets(e=True, forceElement = i)
    cmds.select(cl=True)


