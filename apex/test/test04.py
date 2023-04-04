import maya.cmds as cmds
import json




# cmds.hyperShade (objects = "")





# cmds.hyperShade (smn =True)


# cmds.ls(typ='shadingEngine')



cmds.hyperShade (smn =True)
shadingGroups = cmds.ls( selection=True)

SG = cmds.listConnections( shadingGroups,type = 'shadingEngine')
print (SG)

cmds.select(SG, ne=True, r=True, )

