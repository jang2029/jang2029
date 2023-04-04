import maya.mel as mel
import maya.cmds as cmds


ref_list = []
off_list = []
ref_list = mel.eval('ls -type reference')

for i in ref_list:
    if not 'shared' in i:
        if not cmds.referenceQuery( i, isLoaded = True ):
            off_list.append(i)
        
    
print ('ref_list = ' + str(len(ref_list)) + str(ref_list))
print ('off_list = ' + str(len(off_list)) + str(off_list))

for i in ref_list:
    
    
    if not 'shared' in i and not 'Fx' in i.split(':')[-1]:
        refFile = cmds.referenceQuery( i,filename=True)
        print ('refFile = ', refFile)
        print ('i = ', i)
        if cmds.referenceQuery( i, isLoaded = True ):                      
            cmds.file(refFile.replace('P:', 'D:'), loadReference=i)
        

    if 'Fx' in i.split(':')[-1]:
        refFile = cmds.referenceQuery( i,filename=True)
        print ('refFile = ', refFile)
        print ('i = ', i)
        if cmds.referenceQuery( i, isLoaded = True ):                      
            cmds.file(refFile.replace('P:', 'D:'), loadReference=i)
            

for i in off_list:
    cmds.file(unloadReference = i )
    