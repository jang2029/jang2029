import maya.cmds as cmds
import json


cmds.hyperShade (smn =True)
shaders = cmds.ls( selection=True)


shadingGroups = cmds.listConnections( shaders,type = 'shadingEngine')
print (shadingGroups)

cmds.select(shadingGroups, ne=True, r=True, )

