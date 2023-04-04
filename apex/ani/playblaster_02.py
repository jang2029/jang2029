import maya.cmds as cmds
import os, datetime

slateFile = r'D:/test/playblaster/slate_cam.mb'

cameraName = cmds.ls(sl=1)
if not '_cam' in cameraName[0]:
    print ('select main CAMERA!!')
    exit
        
else:
    cmds.file(slateFile, r=True, type="mayaBinary", ignoreVersion=True, gl=True, namespace = ":", options = "v=0", mergeNamespacesOnClash = True)
            
print (cameraName)
        
cmds.select( clear=True )

filepath = cmds.file(q=True, sn=True)
filename = cmds.file(q=True, sn=True, shn=True)
raw_name, extension = os.path.splitext(filename)
shotName = filename.split('_')[0]+'_'+filename.split('_')[1]
projName =  filename.split('_')[0]
artistName = os.environ['COMPUTERNAME']
currentFrame = round(cmds.currentTime(query=True))
startFrame = int(cmds.playbackOptions (q=True, minTime=True))
endFrame = int(cmds.playbackOptions (q=True, maxTime=True))
frameLength = endFrame - startFrame + 1
range = str(startFrame) + '-' + str(endFrame) + '(' + str(frameLength) + ')'
todayDate = datetime.datetime.now()
todayDate = todayDate.date()
movName = filepath.split('.')[0]+'.mov'

print ('filepath : '+filepath)
print ('filename : '+filename)
print ('raw_name : '+raw_name)
print ('extension : '+extension)
print ('shotName : '+shotName)
print ('projName : '+projName)
print ('artistName : '+artistName)
print ('currentFrame : '+ str(currentFrame))
print ('startFrame : '+str(startFrame))
print ('endFrame : '+str(endFrame))
print ('frameLength : '+str(frameLength))
print ('todayDate : '+str(todayDate))
print ('range : '+str(range))


cmds.setAttr( 'shotName.shotName', shotName, type= "string" )
cmds.setAttr( 'projectName.projectName', projName, type= "string" )
cmds.setAttr( 'versionName.versionName', raw_name, type= "string" )
cmds.setAttr( 'artistName.artistName', artistName, type= "string" )
cmds.setAttr( 'date.date', str(todayDate), type= "string" )
cmds.setAttr( 'range.range', str(range), type= "string" )



cmds.parentConstraint( cameraName, 'camUI_gr', maintainOffset = True )


cmds.playblast(
filename = movName,
forceOverwrite = True,
format = "qt",
sequenceTime = False,
clearCache = True,
viewer = True,
showOrnaments = False,
fp = 4,
percent = 100,
compression = "PNG",
quality = 100,
widthHeight = (2560, 1080)
)





cmds.file(slateFile, removeReference = True)

cmds.delete( 'slate_camRNfosterParent1')