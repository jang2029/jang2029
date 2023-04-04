import maya.cmds as cmds


def exportAbc():

    selectedSet = cmds.ls(selection = True)
    cmds.select(selectedSet)
    selectedObj = cmds.ls(selection = True, l=True)
    
    
    
    startFrame = cmds.playbackOptions( q=True,min=True )
    endFrame  = cmds.playbackOptions( q=True,max=True )

    currentFile =  cmds.file(query=True, sceneName=True, shortName=True)
    fullpath =  cmds.file(query=True, sceneName=True)
    path = fullpath.replace(currentFile, '')
    abcFilename = path + currentFile.replace('.mb', '')+'.abc'
    print ( abcFilename )

    
    bakeObj = ' -root '.join(selectedObj)
    print (bakeObj)
    command = '-frameRange ' + str(startFrame) + ' ' + str(endFrame) + ' -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root ' + bakeObj + ' -file ' + abcFilename
    cmds.AbcExport ( j = command )
    print (abcFilename)

exportAbc()