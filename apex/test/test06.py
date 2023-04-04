import maya.cmds as cmds


def buttonMethod(args):
    cmds.polyCube()


def showUI():
    myWindow = cmds.window(title = 'Prompt', widthHeight =(250,200))
    cmds.columnLayout()
    cmds.text(label='Welcom to the 3D Model Creator')
    cmds.text(label='Button below createGeo')
    cmds.button(label='Cube', command = buttonMethod, enable = True )
    
    
    cmds.showWindow(myWindow)

showUI()