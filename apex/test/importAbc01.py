
import maya.cmds as cmds




assetName = 'ash'
fileName =  'D:/test/ash_rig_main_v025.abc'
cmds.group( em=True, name=assetName )
groupName = cmds.ls(selection =True)
print (groupName)
cmds.AbcImport (fileName, reparent = groupName[0])
cmds.select (groupName)
cmds.sets(groupName, name = 'attatchSet_' + assetName )
