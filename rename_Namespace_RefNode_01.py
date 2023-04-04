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
    refFile = cmds.referenceQuery( i,filename=True)
    name = cmds.referenceQuery( i,filename=True, shortName=True ).split('.')[0]
    print ('i = ' + str(i))
    print ('refFile = ' + str(refFile))
    print ('name = ' + str(name))
    cmds.file( refFile, e=1, namespace=name)
    cmds.lockNode( i, lock=False)
    cmds.rename( i, name+'RN' )
list = []

