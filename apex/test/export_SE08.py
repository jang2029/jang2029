
import maya.cmds as cmds
import json

def exportSD():
    # Bake_Set 선택

    selectedSet = cmds.ls(selection = True)
    cmds.select(selectedSet)
    
    # 선택된 오브젝트의 쉐이더 선택

    cmds.hyperShade (smn = True)



    # 쉐이딩그룹 이름 정리하여 바꾸기

    selectedSD = cmds.ls(selection = True)

    for i in selectedSD:
        sg = cmds.listConnections(i ,type = 'shadingEngine')
        cmds.rename (sg[0], i+'_sg')
        


    # 쉐이딩그룹 mb파일로 내보내기

    print (selectedSD)
    cmds.select(selectedSD)
    shaders = cmds.ls( selection=True)
    shadingGroups = cmds.listConnections( shaders,type = 'shadingEngine')
    print (shadingGroups)

    cmds.select(shadingGroups, ne=True, r=True )


    currentFile =  cmds.file(query=True, sceneName=True, shortName=True)
    fullpath =  cmds.file(query=True, sceneName=True)
    path = fullpath.replace(currentFile, '')
    save_SD_File = currentFile.replace('.mb', '')+'_SD'


    cmds.file (path+save_SD_File, typ='mayaBinary', es=True )

    # 쉐이딩리스트 json파일로 내보내기

    diclistSD = {}
    
    for i in shadingGroups:

        cmds.select (i)
        mesh = cmds.ls(sl=1)
        print (i, mesh)
        diclistSD[i] = mesh
        cmds.select(cl=True)
    
    print (diclistSD)
    save_SD_jsonFile = currentFile.replace('.mb', '')+'_SD.json'
    with open(path+save_SD_jsonFile, 'w', encoding='utf-8') as file:
        json.dump(diclistSD, file, indent='\t')

    cmds.select (clear=True)

exportSD()