import csv
import maya.cmds as cmds
import maya.mel as mel
import os, shutil, stat, datetime


cmds.loadPlugin( 'AbcExport.mll' )
cmds.loadPlugin( 'AbcImport.mll' )
cmds.loadPlugin( 'atomImportExport.mll' )
cmds.loadPlugin( 'fbxmaya.mll' )
cmds.loadPlugin( 'gameFbxExporter.mll' )
cmds.loadPlugin( 'Type.mll' )


filename = 'apx_9999_animation_v010.mb'

asset_path = 'D:/projects/eaapexseason17_42048P/assets/3D'
shot_path = 'D:/projects/eaapexseason17_42048P/sequences'

currentShot = filename.split('_animation')[0]
version = (filename.split('.')[0]).split('_')[-1]
pub_path = f'{shot_path}/{currentShot}/animation/output/maya/showcase_animation/{version}'
scene_csv = f'{pub_path}/{filename}.csv'

print (scene_csv)



cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
cmds.setAttr("defaultResolution.aspectLock", 0)
cmds.setAttr("defaultResolution.width", 2560)
cmds.setAttr("defaultResolution.height", 1200)
cmds.setAttr("defaultResolution.deviceAspectRatio", 2.133)
cmds.setAttr("defaultResolution.pixelAspect", 1)
cmds.setAttr("defaultResolution.aspectLock", 1)



camPath = f'{shot_path}/{currentShot}/animation/output/camcache/animation_renderCam/{version}/alembic'
file_list = os.listdir(camPath)
camFile = [s for s in file_list if 'renderCam' in s]


if not cmds.objExists('CAM'):
    cmds.group(em=True, name='CAM' )
command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|CAM" "{camPath}/{camFile[0]}";'
mel.eval(command)



with open(scene_csv) as f:
    data = csv.reader(f)
    for asset_type, asset_name in data:
        if not 'Fx' in asset_name:
            if asset_type == 'character' or asset_type == 'prop':
                assetNumber=0
                groupName = asset_name.split('_')[0]
                with open(scene_csv) as f:
                    data = csv.reader(f)
                    for count_type, count_name in data:
                        if groupName in count_name and 'Fx' not in count_name :
                            assetNumber =assetNumber+ 1


                
                print ('groupName = '+' '+asset_type+' '+groupName)
                print ('assetNumber = '+ str(assetNumber))
                if assetNumber == 1 :

                    if asset_type == 'character':
                        if not cmds.objExists('CH'):
                            cmds.group(em=True, name='CH' )
                        cmds.group(em=True, parent='CH', name=groupName )
                        abcName = f'{currentShot}_animation_{asset_type}_{groupName}_{version}.abc'
                        abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{groupName}/{version}/alembic/'
                        command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|CH|{groupName}" "{abcPath}{abcName}";'
                        mel.eval(command)

                    if asset_type == 'prop':
                        if not cmds.objExists('PROP'):
                            cmds.group(em=True, name='PROP' )
                        cmds.group(em=True, parent='PROP', name=groupName )
                        abcName = f'{currentShot}_animation_{asset_type}_{groupName}_{version}.abc'
                        abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{groupName}/{version}/alembic/'
                        command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|PROP|{groupName}" "{abcPath}{abcName}";'
                        mel.eval(command)

                if assetNumber > 1 :

                    if asset_type == 'character':
                        if not cmds.objExists('CH'):
                            cmds.group(em=True, name='CH' )
                        cmds.group(em=True, parent='CH', name=asset_name )


                        abcName = f'{currentShot}_animation_{asset_type}_{asset_name}_{version}.abc'
                        abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{asset_name}/{version}/alembic/'
                        command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|CH|{asset_name}" "{abcPath}{abcName}";'
                        print ('command = '+ command)
                        mel.eval(command)
                    
                    if asset_type == 'prop':
                        if not cmds.objExists('PROP'):
                            cmds.group(em=True, name='PROP' )
                        cmds.group(em=True, parent='PROP', name=asset_name )

                        
                        abcName = f'{currentShot}_animation_{asset_type}_{asset_name}_{version}.abc'
                        abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{asset_name}/{version}/alembic/'
                        print('abcName = '+asset_name)
                        print('abcName = '+abcName)
                        print('abcPathe = '+abcPath)
                        command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|PROP|{asset_name}" "{abcPath}{abcName}";'
                        mel.eval(command)
        if 'bg' == asset_type:
            list = []
            item = asset_name.split('_')[0]

            atomName = f'{currentShot}_animation_{asset_type}_{item}_{version}.atom'
            atomPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{item}/{version}/atom'
            atomName = '"'+atomPath + '/' + atomName+'"'
            mapfile =  f'{atomPath}/{currentShot}_animation_{asset_type}_{item}_{version}.map'


            assetPath = f'{asset_path}/{asset_type}/{item}/rig/output/rig/rig_main'
            assetVer = [ name for name in os.listdir(assetPath) if os.path.isdir(os.path.join(assetPath, name)) ][-1]
            assetFile = f'{item}_rig_main_{assetVer}'
            cmds.file(f'{assetPath}/{assetVer}/maya/{assetFile}.mb', ignoreVersion = True, r=True, gl=True, mnc=False, ns=assetFile)
            
            ref_list = mel.eval('ls -type reference')

            for i in ref_list:
                if assetFile in i:
                    refNode = i

            refMember = cmds.referenceQuery(refNode,nodes=True,dagPath=True)
            for i in refMember:
                if cmds.objectType(i) == 'nurbsCurve':
                    list.append(i)
            list = cmds.listRelatives(list, parent = True)
            print ('list = ' + str(list))
                
            if list:
                with open(mapfile , 'r') as f:
                    line = f.readlines()
                print (line)

                with open(mapfile , 'w') as f:
                    for i in line:
                        for o in list:
                            if o.split(':')[-1] in i:
                                data = (i.split('\n')[0]).split(' ')[0] + ' ' + '"'+ o + '"' + '\n'
                                f.write(data)
                f.close()
                cmds.select(list)
            
                command = f'file -import -type "atomImport" -ra true -options ";;targetTime=3;option=scaleReplace;match=mapFile;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile={mapfile};" {atomName};'
                mel.eval(command)

            topNode = cmds.ls(assemblies=True)
            for i in topNode:
                if refNode.split('RN')[0] in i:
                    bgGrp = i
            print(bgGrp)
            if not cmds.objExists('BG'):
                cmds.group(em=True, name='BG' )
            cmds.parent( bgGrp , 'BG' )

            
        if 'Fx' in asset_name:
            list = []
            item = asset_name.split('_')[0]
            fxitem = asset_name.split(':')[-1]

            
            atomName = f'{currentShot}_animation_{item}_{fxitem}_{version}.atom'
            atomPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_Fx_{item}_{fxitem}/{version}/atom/'
            atomName = '"'+atomPath+atomName+'"'
            mapfile =  f'{atomPath}/{currentShot}_animation_{asset_type}_{item}_{version}.map'

            assetPath = f'{asset_path}/fx/{fxitem.split("_")[0]}/rig/output/rig/rig_main'
            assetVer = [ name for name in os.listdir(assetPath) if os.path.isdir(os.path.join(assetPath, name)) ][-1]
            assetFile = f'{fxitem.split("RN")[0][:-5]}_{assetVer}'
            cmds.file(f'{assetPath}/{assetVer}/maya/{assetFile}.mb', ignoreVersion = True, r=True, gl=True, mnc=False, ns=assetFile)
            

            ref_list = mel.eval('ls -type reference')

            for i in ref_list:
                if assetFile in i:
                    refNode = i

            refMember = cmds.referenceQuery(refNode,nodes=True,dagPath=True)
            
            for i in refMember:
                if cmds.objectType(i) == 'nurbsCurve':
                    list.append(i)
            list = cmds.listRelatives(list, parent = True)
            print ('list = ' + str(list))

            with open(mapfile , 'r') as f:
                line = f.readlines()
            print (line)

            with open(mapfile , 'w') as f:
                for i in line:
                    for o in list:
                        if o.split(':')[-1] in i:
                            data = (i.split('\n')[0]).split(' ')[0] + ' ' + '"'+ o + '"' + '\n'
                            f.write(data)
            f.close()

            topNode = cmds.ls(assemblies=True)
            for i in topNode:
                if refNode.split('RN')[0][:-5] in i:
                    fxGrp = i
            print(fxGrp)
            if not cmds.objExists('FX'):
                cmds.group(em=True, name='FX' )
            cmds.parent( fxGrp , 'FX' )

            cmds.select(list)
            command = f'file -import -type "atomImport" -ra true -options ";;targetTime=3;option=scaleReplace;match=mapFile;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile={mapfile};" {atomName};'
            mel.eval(command)