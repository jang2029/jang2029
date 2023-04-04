
import maya.cmds as cmds




assetName = 'ash'
abcfileName = 'D:/test/ash_rig_main_v025.abc'
sdFileName = 'D:/test/ash_rig_main_v025_SD.mb'
sdJsonFileName = 'D:/test/ash_rig_main_v025_SD.json'

cmds.file(sdFileName, i = True, ignoreVersion = True, ra = True, mergeNamespacesOnClash = True, namespace = ":", options = "v=0",  pr = True,  importTimeRange = "combine" )
cmds.group( em=True, name=assetName )
groupName = cmds.ls(selection =True)
print (groupName)
cmds.AbcImport (abcfileName, reparent = groupName[0])
cmds.select (groupName)
cmds.sets(groupName, name = 'attatchSet_' + assetName )








