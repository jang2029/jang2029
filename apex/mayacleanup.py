import pymel.core as pm     
import maya.cmds as cmds      
        
# delete unknown nodes
cmds.delete(cmds.ls(type="unknown"))

# delete unknown plugins
plugins_list = cmds.unknownPlugin(q=True, l=True)
if plugins_list:
    for plugin in plugins_list:
        print(plugin)
        cmds.unknownPlugin(plugin, r=True)
         
# delete onModelChange3dc ERR
# Get all model editors in Maya and reset the editorChanged event

for item in pm.lsUI(editors=True):
    if isinstance(item, pm.ui.ModelEditor):
        pm.modelEditor(item, edit=True, editorChanged="")

# delete onModelChange3dc ERR

# killTurtle

try:
    pm.lockNode( 'TurtleDefaultBakeLayer', lock=False )
    pm.delete('TurtleDefaultBakeLayer')
except:
    pass
try:
    pm.lockNode( 'TurtleBakeLayerManager', lock=False )
    pm.delete('TurtleBakeLayerManager')
except:
    pass
try:
    pm.lockNode( 'TurtleRenderOptions', lock=False )
    pm.delete('TurtleRenderOptions')
except:
    pass
try:
    pm.lockNode( 'TurtleUIOptions', lock=False )
    pm.delete('TurtleUIOptions')
except:
    pass
pm.unloadPlugin("Turtle.mll")