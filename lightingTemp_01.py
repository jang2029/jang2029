import csv
import maya.cmds as cmds
import maya.mel as mel
import os, shutil, stat, datetime

cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
cmds.setAttr("defaultResolution.aspectLock", 0)
cmds.setAttr("defaultResolution.width", 2560)
cmds.setAttr("defaultResolution.height", 1200)
cmds.setAttr("defaultResolution.deviceAspectRatio", 2.133)
cmds.setAttr("defaultResolution.pixelAspect", 1)
cmds.setAttr("defaultResolution.aspectLock", 1)



shot_path = 'P:/projects/eaapexseason17_42048P/sequences'
currentShot = 'apx_9999'
version = 'v010'
pub_path = f'{shot_path}/{currentShot}/animation/output/maya/showcase_animation/{version}'
filename = 'apx_9999_animation_v010.mb'
scene_csv = f'{pub_path}/{filename}.csv'


print (scene_csv)


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
