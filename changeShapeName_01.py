import maya.cmds as cmds


meshShape = cmds.listRelatives(cmds.ls(sl=True), type='mesh', allDescendents = True, fullPath = True)

for i in meshShape:
    transform = cmds.listRelatives(i, parent=True)
    if (i.split('|')[-1].split('Shape')[0] != transform[0]) or (i.split('|')[-1].split('Shape')[-1] != ''):
        cmds.rename(i, f'{transform[0]}Shape')
        print(f'{i} changed to {transform[0]}Shape')

