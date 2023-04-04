import maya.mel as mel
import maya.cmds as cmds


list = []
ref_list = []


ref_list = mel.eval('ls -type reference')

for i in ref_list:
    if not 'Fx' in i.split(':')[-1] and not 'shared' in i:
        if cmds.referenceQuery( i, isLoaded = True ):      
            list.append(i)
    if 'Fx' in i.split('_')[0] and not 'shared' in i:
        if cmds.referenceQuery( i, isLoaded = True ):        
            list.append(i)

print ( str( len( list )) + str( list ))



for i in list:
    
    ns = cmds.referenceQuery(i ,namespace=True)
    pathName = cmds.referenceQuery( i,filename=True, wcn =True)
    name = cmds.referenceQuery( i,filename=True, shortName=True ).split('.')[0]
    print ('i = ' + str(i))
    print ('ns = ' + str(ns))
    print ('pathName = ' + str(pathName))
    print ('name = ' + str(name))
    
    if not ns == ':':
        mel.eval(f'file -e -namespace "{name}" -referenceNode "{i}" "{pathName}";”')
        cmds.lockNode( i, lock=False)
        cmds.rename( i, name+'RN' )
    
    

