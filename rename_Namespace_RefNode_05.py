import maya.mel as mel
import maya.cmds as cmds


list = []
ref_list = []


ref_list = mel.eval('ls -type reference')
print (ref_list)

for i in ref_list:
    
    if not 'Fx' in i.split(':')[-1] and not 'shared' in i:
        if cmds.referenceQuery( i, isLoaded = True ):      
            list.append(i)

for i in ref_list:
    
    if 'Fx' in i.split('_')[0] and not 'shared' in i:
        if cmds.referenceQuery( i, isLoaded = True ):        
            list.append(i)


for i in list.copy():
    if 'Fx' in i.split(':')[-1] and ':' in i:
        list.remove(i)
    print(i)


print ( str( len( list )) + str( list ))



for i in list:
    
    ns = cmds.referenceQuery(i ,namespace=True)
    pathName = cmds.referenceQuery( i,filename=True, wcn =True)
    name = cmds.referenceQuery( i,filename=True, shortName=True ).split('.')[0]
    print ('i = ' + str(i))
    print ('ns = ' + str(ns))
    print ('pathName = ' + str(pathName))
    print ('name = ' + str(name))
    
    if not '{' in cmds.referenceQuery( i,filename=True, shortName=True ):
        ver = ''
    else:
        ver = 'a'+cmds.referenceQuery( i,filename=True, shortName=True ).split('{')[-1].split('}')[0]    
    
    if not ns == ':' and not name+ver == ns.split(':')[-1]:
        mel.eval(f'file -e -namespace "{name}{ver}" -referenceNode "{i}" "{cmds.referenceQuery( i,filename=True)}";”')
        cmds.lockNode( i, lock=False)
        cmds.rename( i, name+'RN' )
    if not ns == ':' and name+ver == ns.split(':')[-1]:
        mel.eval(f'file -referenceNode "{i}" "{pathName}";”')
        cmds.lockNode( i, lock=False)
        cmds.rename( i, name+'RN' )

list.clear()
ref_list.clear()
