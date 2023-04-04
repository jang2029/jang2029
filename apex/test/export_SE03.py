
import maya.cmds as cmds
import json

cmds.hyperShade (smn =True)

selected = cmds.ls( selection=True)

for i in selected:
    sg = cmds.listConnections( i,type = 'shadingEngine')
    print (i)
    print (sg)
    cmds.rename (sg, i+'_SG')
print (selected)
cmds.select(selected)


shaders = cmds.ls( selection=True)
shadingGroups = cmds.listConnections( shaders,type = 'shadingEngine')
print (shadingGroups)

cmds.select(shadingGroups, ne=True, r=True, )

