import maya.cmds as cmds
import os, datetime


'''
------ 사용 방법 ------

1.랜더카메라를 선택합니다.
2.스크립트를 실행하면 마야 씬이 있는 폴더에 플레이블레스터 mov가 만들어 짐니다.
3.랜더 카메라 이름에는 "_cam" 문자가 포함 되어 있어야 합니다.
4.slate.mb 는 슬레이트를 구성하는 마야 파일입니다. 레퍼런스로 불러와서 플레이플레스터를 만들고 자동으로 지워짐니다.

'''




slateFile = r'Q:/pipeline_script/apex/maya/2022/slate_cam.mb'


try:
    cmds.file(slateFile, removeReference = True)
    cmds.delete( 'slate_camRNfosterParent1')
except:
    pass

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
cmds.setAttr( 'projectName.projectName', projName.upper(), type= "string" )
cmds.setAttr( 'versionName.versionName', raw_name, type= "string" )
cmds.setAttr( 'artistName.artistName', artistName, type= "string" )
cmds.setAttr( 'date.date', str(todayDate), type= "string" )
cmds.setAttr( 'range.range', str(range), type= "string" )



cmds.parentConstraint( cameraName, 'camUI_parent_gr', maintainOffset = False )


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