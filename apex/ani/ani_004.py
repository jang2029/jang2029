#
# maya 2022
# mayapy 3.7.7

from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

import os, shutil, stat
import sys
import csv
import re
import json

cmds.loadPlugin( 'AbcExport.mll' )
cmds.loadPlugin( 'AbcImport.mll' )

# PROJ_DRIVE = os.getenv('PROJ_DRIVE')
PROJ_DRIVE = r'D:'


def getMayaMainWindow():

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

    return mayaMainWindow

class AniToolUI(QWidget):

    def __init__(self):

        super().__init__()

        self.window_name = 'keyring_9bf05780542d4c712ad2e5923be39533'
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name)
        self.setParent(getMayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setObjectName(self.window_name)

        self.initUI()

        self.openCurrentENV()



    ###################
    # common function #
    ###################


    def confirmMessage(self, msg):

        msgBox = QMessageBox()
        msgBox.setWindowTitle('Confirm')
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setDefaultButton(QMessageBox.No)
        ret = msgBox.exec_()

        return ret
    def errorMessage(self, msg):

        msgBox = QMessageBox()
        msgBox.setWindowTitle('ERROR')
        msgBox.setText(msg)
        ret = msgBox.exec_()

        return ret

    def mayaCleanup(self):
     
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



    def saveCurrentENV(self):

        proj       = self.proj_list.currentText()
        ep         = self.episode_list.currentRow()
        asset_type = self.asset_type.currentRow()
        asset_name = self.asset_name.currentRow()

        env_docs = {'project': proj,          'episode': ep,
                    'asset_type': asset_type, 'asset_name': asset_name}

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_AniTool.json'

        with open(env_path, 'w') as f:
            data = json.dumps(env_docs, indent=4, separators=(',',':'), sort_keys=True)
            f.write(data)


    def openCurrentENV(self):

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_AniTool.json'

        with open(env_path) as f:
            env_docs = json.load(f)

        self.proj_list.setCurrentText(env_docs['project'])
        self.episode_list.setCurrentRow(env_docs['episode'])
        self.asset_type.setCurrentRow(env_docs['asset_type'])
        self.asset_name.setCurrentRow(env_docs['asset_name'])

    def readAssetCSV(self):
        ###########################
        # asset_list.csv 자동만들기#
        ###########################
        current_proj = self.proj_list.currentText()
        current_ep   = self.episode_list.currentItem().text()
        csv_path     = f'{PROJ_DRIVE}/{current_proj}/{current_ep}'
        csv_path     = f'{csv_path}/assets/3D/asset_list.csv'

        print (csv_path)

        bgPath = f'{PROJ_DRIVE}/{current_proj}/{current_ep}/assets/3D/bg'
        characterPath = f'{PROJ_DRIVE}/{current_proj}/{current_ep}/assets/3D/character'
        propPath = f'{PROJ_DRIVE}/{current_proj}/{current_ep}/assets/3D/prop'
        bgpropPath = f'{PROJ_DRIVE}/{current_proj}/{current_ep}/assets/3D/bgprop'

        bgDirectoryList = os.listdir(bgPath)
        characterDirectoryList = os.listdir(characterPath)
        propDirectoryList = os.listdir(propPath)
        bgpropDirectoryList = os.listdir(bgpropPath)


        bgList = [a for a in bgDirectoryList if os.path.isdir((bgPath+'\\'+a))]
        characterList = [a for a in characterDirectoryList if os.path.isdir((characterPath+'\\'+a))]
        propList = [a for a in propDirectoryList if os.path.isdir((propPath+'\\'+a))]
        bgpropList = [a for a in bgpropDirectoryList if os.path.isdir((bgpropPath+'\\'+a))]

        f = open(csv_path,'w', newline='')
        wr = csv.writer(f)

        for i in bgList:
            wr.writerow(['bg',i])
        
        for i in characterList:
            wr.writerow(['character',i])
        
        for i in propList:
            wr.writerow(['prop',i])
        
        for i in bgpropList:
            wr.writerow(['bgprop',i])

        
        f.close()
        

        ###########################
        # asset_list.csv 읽어오기 #
        ###########################

        self.assets = {}

        if os.path.isfile(csv_path):
            with open(csv_path) as f:
                data = csv.reader(f)
                for asset_type, asset_name in data:

                    if asset_type not in self.assets:
                        self.assets[asset_type] = []

                    self.assets[asset_type].append(asset_name)
        else:
            self.asset_type.clear()
            self.asset_name.clear()

    def getProjectList(self):

        self.proj_list.clear()

        self.proj_list.addItem('( Select Project )')
        for proj_name in sorted(os.listdir(PROJ_DRIVE)):
            if os.path.isdir(f'{PROJ_DRIVE}/{proj_name}'):
                self.proj_list.addItem(proj_name)

    def getEpisodeList(self):

        current_proj = self.proj_list.currentText()
        current_proj = f'{PROJ_DRIVE}/{current_proj}'

        self.episode_list.clear()
        if os.path.isdir(current_proj):
            for ep_name in sorted(os.listdir(current_proj)):
                if os.path.isdir(f'{current_proj}/{ep_name}'):
                    self.episode_list.addItem(ep_name)

    def getAssetType(self):

        self.readAssetCSV()

        self.asset_name.clear()
        self.asset_type.clear()
        self.asset_type.addItems(sorted(self.assets.keys()))

    def getAssetName(self):

        if self.asset_type.currentItem():
            current_asset_type = self.asset_type.currentItem().text()
            
            self.asset_name.clear()
            self.asset_name.addItems(sorted(self.assets[current_asset_type]))

    def getMiddleName(self):

        department_dir = self.getDepartmentDir('rig/output/rig')

        self.middle_list.clear()
        if os.path.isdir(department_dir):
            middle_names = os.listdir(department_dir)
            if 'rig_main' in middle_names:
                middle_names.pop(middle_names.index('rig_main'))
                self.middle_list.addItem('rig_main')
            for middle_name in sorted(middle_names):
                self.middle_list.addItem(middle_name)
        else:
            self.middle_list.addItem('rig_main')

        self.getVersion()

    def addMiddleName(self):

        middle_name = self.middle_edit.text()

        self.middle_list.addItem(middle_name)

        self.middle_edit.clear()
        self.middle_list.clearSelection()

    def getDepartmentDir(self, depart=None):

        """
        depart:
            mod, tex, lookdev, rig
        """

        proj = self.proj_list.currentText()
        ep = self.episode_list.currentItem().text()
        asset_type = self.asset_type.currentItem().text()
        asset_name = self.asset_name.currentItem().text()

        department_dir = f'{PROJ_DRIVE}/{proj}/{ep}'
        department_dir = f'{department_dir}/assets/3D'
        department_dir = f'{department_dir}/{asset_type}/{asset_name}'
        department_dir = f'{department_dir}/{depart}'

        return department_dir

    # semi common
    def getSaveDir(self, save_type=None):

        """
        save_type:
            wip, pub
        """

        department_dir = self.getDepartmentDir('shade')

        save_dir = f'{department_dir}/{save_type}'

        return save_dir

    def getSaveVersion(self, save_dir=None):

        re_pattern = re.compile('_v(\d{3}).mb$')

        version_num = 0
        if os.listdir(save_dir):
            for save_file in sorted(os.listdir(save_dir)):
                if re.search(re_pattern, save_file):
                    version_num = int(re.search(re_pattern, save_file).group(1))

        return version_num + 1

    def getVersion(self):
        # lookdev 버젼 리스트
        self.save_wip_version.clear()
        wip_dir = self.getSaveDir('work') + '/maya/scenes/increments'
        if os.path.isdir(wip_dir):
            for wip_file in sorted(os.listdir(wip_dir)):
                re_match = re.search('_(v\d{3}).mb$', wip_file)
                if re_match:
                    self.save_wip_version.addItem(re_match.group(1))

        self.publish_version.clear()
        pub_dir = self.getSaveDir('output') + '/shadegeo/shade_main'
        if os.path.isdir(pub_dir):
            for pub_file in sorted(os.listdir(pub_dir)):
                pub_file = pub_dir+'/'+ pub_file+'/maya'
                pub_file = os.listdir(pub_file)
                for i in pub_file:
                    re_match = re.search('_(v\d{3}).mb$', i)
                    if re_match:
                        self.publish_version.addItem(re_match.group(1))

    # semi common
    def getSaveFile(self, save_version=None, save_ext=None):

        ep = self.episode_list.currentItem().text()
        asset_name = self.asset_name.currentItem().text()

        save_file = f'{asset_name}_shade_main'
        save_file = f'{save_file}_{save_version}.{save_ext}'

        return save_file

    ###################
    # common function #
    ###################

    ########################
    # model data reference #
    ########################

    def getRigPubVersion(self):

        self.rig_pub_ver.clear()

        pub_dir = self.getRigPubDir()

        #  Rig pub 경로 지정
        print('pub_dir = ' + pub_dir)

        if os.path.isdir(pub_dir):
            for pub_file in sorted(os.listdir(pub_dir)):
                pub_file = pub_dir+'/'+ pub_file+'/maya/'
                try:
                    pub_file = os.listdir(pub_file)
                except:
                    continue
                pub_file = [file for file in pub_file if file.endswith(".mb") or file.endswith(".ma")]
                re_match = re.search('_(v\d{3})', pub_file[0])
                if re_match:
                    self.rig_pub_ver.addItem(re_match.group(1))
                

    def getRigPubDir(self):

        """
        depart:
            mod, tex, lookdev, rig
        """

        department_dir = self.getDepartmentDir('rig')
        middle_name = self.middle_list.currentItem().text()
        
        save_dir = f'{department_dir}/output/rig/{middle_name}'
        print ('save_dir = ' + save_dir)


        return save_dir

    def getRigPubFile(self, save_version=None):

        ep = self.episode_list.currentItem().text()
        asset_name = self.asset_name.currentItem().text()
        middle_name = self.middle_list.currentItem().text()

        save_file = f'{asset_name}_{middle_name}'
        save_file = f'{save_file}_{save_version}'
        print ('save_file = '+save_file)
        return save_file

    def assetRefBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        selected_version = self.rig_pub_ver.currentItem().text()
        pub_file = self.getRigPubFile(selected_version)
        pub_dir = self.getRigPubDir() + '/'+ selected_version + '/maya'
        
        
        print ('pub_file = '+pub_file)
        print ('pub_dir = '+pub_dir)
        



        pub_path = f'{pub_dir}/{pub_file}'
        namespace = ':'
        print (pub_path)
        if os.path.isfile(pub_path+'.ma'):
            pub_path = pub_path+'.ma'
        if os.path.isfile(pub_path+'.mb'):
            pub_path = pub_path+'.mb'

        cmds.file(pub_path, ignoreVersion = True, r=True, gl=True, mnc=False, ns=namespace)
        

        

   

    ########################
    # model data reference #
    ########################

    # common function
    def openWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        wip_dir = self.getSaveDir('work') + '/maya/scenes/increments'
        selected_version = self.save_wip_version.currentItem().text()
        wip_file = self.getSaveFile(selected_version, 'mb')
        wip_path = f'{wip_dir}/{wip_file}'

        cmds.file(wip_path, o=True, f=True)

    def saveWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save the file?'):
            return 0

        # make WIP maya dir
        wip_maya_dir = self.getSaveDir('work') + '/maya/scenes/increments'
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)

        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)
        wip_version = f'v{str(version_num).zfill(3)}'
        wip_maya_file = self.getSaveFile(wip_version, 'mb')
        wip_maya_path = f'{wip_maya_dir}/{wip_maya_file}'

        # save file

        self.mayaCleanup()
        cmds.file(rn=wip_maya_path)
        cmds.file(s=True, f=True)

        # update version list
        self.getVersion()

    def publishBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save the file?'):
            return 0

        # save WIP
        # make WIP maya dir
        wip_maya_dir = self.getSaveDir('work') + '/maya/scenes/increments'
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)
        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)-1
        print('version_num = '+str(version_num))
        wip_version = f'v{str(version_num).zfill(3)}'

        print('wip_version = '+ wip_version)
        pub_maya_file = self.getSaveFile(wip_version, 'mb')
        pub_maya_path = self.getSaveDir('output') + '/shadegeo/shade_main/' + wip_version + '/maya'
        if not os.path.isdir(pub_maya_path):
            os.makedirs(pub_maya_path)
        else:
            self.errorMessage('!! Pub version is already Exist !!')
            return 0

        pub_maya_path = f'{pub_maya_path}/{pub_maya_file}'

        print ('wip_maya_file = ' + pub_maya_file)
        print ('pub_maya_path = ' + pub_maya_path)

        # save file
        self.mayaCleanup()
        cmds.file(rn=pub_maya_path)
        cmds.file(s=True, f=True)

        # make Publish dir
        pub_maya_dir = self.getSaveDir('output') + '/shadegeo/shade_main/' + wip_version + '/maya'
        
        if not os.path.isdir(pub_maya_dir):
            os.makedirs(pub_maya_dir)

        pub_json_dir = self.getSaveDir('output') + '/shadegeo/shade_main' + '/' + wip_version + '/maya'
        if not os.path.isdir(pub_json_dir):
            os.makedirs(pub_json_dir)

        # shader dictionary
        # shading group, material, object
        shader_dict = {'surface': dict(), 'vray_displacement': dict()}
        for sg in [se for se in cmds.ls(typ='shadingEngine') if not re.search('^init', se)]:
            shader_dict['surface'][sg] = {'materials': [], 'objects': []}
            mat_list = cmds.ls(cmds.listConnections(sg), materials=True)

            for mat in mat_list:
                shader_dict['surface'][sg]['materials'].append(mat)
                cmds.select(mat, r=True)
                cmds.hyperShade(o='')
                
                for obj in cmds.ls(sl=True):
                    obj_split = obj.split('|')

                    if len(obj_split) == 1:
                        # obj = re.search('[^:]*$', obj_split[0]).group()
                        obj = obj_split[0]
                    else:
                        obj_arr = []
                        for split_ele in obj_split:
                            split_name = re.search('[^:]*$', split_ele).group()
                            obj_arr.append(split_name)
                        obj = '|'.join(obj_arr)

                    shader_dict['surface'][sg]['objects'].append(obj)
        # vray displacement
        for dis in cmds.ls(typ='VRayDisplacement'):
            shader_dict['vray_displacement'][dis] = list()
            for obj in cmds.listConnections(dis, s=True):
                obj_split = obj.split('|')

                if len(obj_split) == 1:
                    # obj = re.search('[^:]*$', obj_split[0]).group()
                    obj = obj_split[0]
                else:
                    obj_arr = []
                    for split_ele in obj_split:
                        split_name = re.search('[^:]*$', split_ele).group()
                        obj_arr.append(split_name)
                    obj = '|'.join(obj_arr)
                shader_dict['vray_displacement'][dis].append(obj)
        #
        cmds.select(cl=True)



        # export json
        
        pub_json_path = pub_json_dir
        if not os.path.isdir(pub_json_path):os.makedirs(pub_json_path)
        pub_json_file = cmds.file(query=True, sceneName=True, shortName=True).replace('.mb', '')
        pub_json_file = pub_json_path + '/' + pub_json_file + '.json'

        pub_mayaSD_path = pub_maya_dir
        if not os.path.isdir(pub_mayaSD_path):os.makedirs(pub_mayaSD_path)
        pub_mayaSD_file = cmds.file(query=True, sceneName=True, shortName=True).replace('.mb', '')+'_SD'
        pub_mayaSD_file = pub_mayaSD_path + '/' + pub_mayaSD_file

        print ('pub_json_file : '+pub_json_file)
        print ('pub_mayaSD_file : '+pub_mayaSD_file)

        with open(pub_json_file, 'w') as f:
            data = json.dumps(shader_dict, indent=4, separators=(',',':'), sort_keys=True)
            f.write(data)



        ###################
        # publish alembic #
        ###################

        asset_type = self.asset_type.currentItem().text()
        asset_name = self.asset_name.currentItem().text()
        if asset_type == 'character'or asset_type == 'prop':

            pub_abc_path = self.getSaveDir('output') + '/shadegeo/shade_main' + '/' + wip_version + '/alembic'
            
            pub_abc_file = self.getSaveFile(wip_version, 'abc')

            # make publish alembic dir

            if not os.path.isdir(pub_abc_path):
                os.makedirs(pub_abc_path)
            pub_abc_path = pub_abc_path+'/'+pub_abc_file
            
            print ('pub_abc_path : ' + pub_abc_path)

            

            # select group

            try:
                cmds.select(f'{asset_name}_grp', r=True)
            except:
                print(f'{asset_name}_grp is not exist!!')
            try:
                cmds.select('GEO', r=True)
            except:
                print('GEO is not exist!!')
            try:
                cmds.select('geo', r=True)
            except:
                print('geo is not exist!!')
            
            # export alembic selected group

            selectGroup = cmds.ls(sl=1,sn=True)
            abc_export_cmd = 'AbcExport -j '
            abc_export_cmd += '"-frameRange 1 1 -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa '
            abc_export_cmd += '-root |' + selectGroup[0]
            abc_export_cmd += ' -file ' + pub_abc_path + '"'
            mel.eval(abc_export_cmd)
        else:
            print('DO not make ABC')



        #텍스쳐파일 복사
        pub_texture_path = self.getSaveDir('output') + '/shadegeo/shade_main' + '/' + wip_version + '/maya/textures'
        if not os.path.isdir(pub_texture_path):
            os.makedirs(pub_texture_path)
        
        for i in cmds.file(query=True, list=True):
            filename = i.split('.')
            if not filename[-1] in ['', 'mb', 'ma', 'abc']:
                print (i+' copyed to '+pub_texture_path)
                newName = i.split('/')
                newName = (pub_texture_path + '\\' + newName[-1])
                print ('newName = '+newName)
                if os.path.isfile(newName):
                    print(newName+' 지웡')
                    os.chmod( newName, stat.S_IWRITE )
                    os.remove(newName)
                
                shutil.copy(i, newName)
                
                
        #텍스쳐경로 변환
        fileNodes = cmds.ls(type='file')
        print (fileNodes)
        for fileNode in fileNodes:
            orgPath = cmds.getAttr(fileNode+'.fileTextureName')
            print (orgPath)
            
            texture_name = re.split('/', orgPath)
            texture_name = texture_name[-1]
            newName = (pub_texture_path + '/'+ texture_name)
            cmds.setAttr(fileNode+'.fileTextureName', newName, type ='string' )
         




        # export shader
        cmds.select([se for se in cmds.ls(typ='shadingEngine') if not re.search('^init', se)], ne=True, r=True)
        cmds.file(pub_mayaSD_file, op='v=0;', typ='mayaBinary', pr=True, es=True)
        cmds.select(cl=True)

        # save file
        self.mayaCleanup()
        cmds.file(s=True, f=True)

        # update version
        self.getVersion()

    def assignShaderBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to assign shader?'):
            return 0

        # get model namespace
        #네임스페이스 유무 확인
        selected = cmds.ls(sl=True)
        if ':' in selected[0]:
            namespace = re.search('^[^:]*', selected[0]).group()
        else:
            print('namespace is not exist')
            namespace = ''
        
        # load shader json
        selected_version = self.publish_version.currentItem().text()
        pub_dir = self.getSaveDir('output') + '/shadegeo/shade_main/' + selected_version + '/maya'
        print ('json:pub_dir = '+pub_dir)
        
        pub_file = self.getSaveFile(selected_version, 'json')
        print ('json:pub_file = '+pub_file)
        json_path = f'{pub_dir}/{pub_file}'
        print ('json:son_path = '+json_path)
        #
        with open(json_path) as f:
            shader_dict = json.load(f)

        # import shader without namespace
        selected_version = self.publish_version.currentItem().text()
        shader_pub_dir = self.getSaveDir('output') + '/shadegeo/shade_main/' + selected_version + '/maya'
        shader_pub_file = self.getSaveFile(selected_version, 'mb')
        shader_pub_file = shader_pub_file.split('.')
        shader_pub_file = shader_pub_file[0]+'_SD.mb'
        shader_pub_path = f'{shader_pub_dir}/{shader_pub_file}'
        print('shader:shader_pub_path = '+shader_pub_path )
        cmds.file(shader_pub_path, i=True, typ='mayaBinary', iv=True, mnc=False, op="v=0;p=17;f=0", pr=True, itr='combine')

        # assign shader
        # surface shader
        for sg in shader_dict['surface']:
            mat = shader_dict['surface'][sg]['materials'][0]
            for obj in shader_dict['surface'][sg]['objects']:
                obj_split = obj.split('|')

                if len(obj_split) == 1:
                    obj = f'{namespace}:{obj}'
                else:
                    obj_arr = []
                    for split_ele in obj_split:
                        split_ele = f'{namespace}:{split_ele}'
                        obj_arr.append(split_ele)
                    obj = '|'.join(obj_arr)

                if cmds.objExists(obj):
                    cmds.select(obj, r=True)
                    cmds.hyperShade(a=mat)
        # make vray displacement
        for dis in shader_dict['vray_displacement']:
            # create node VRayDisplacement
            cmds.createNode('VRayDisplacement', n=dis)
            # set VRayDisplacement attribute
            for attr in ['vray_subdivision', 'vray_displacement', 'vray_subquality']:
                attr_cmd = f'vray addAttributesFromGroup {dis} {attr} 1'
                mel.eval(attr_cmd)
            # add object
            for obj in shader_dict['vray_displacement'][dis]:
                obj_split = obj.split('|')

                if len(obj_split) == 1:
                    obj = f'{namespace}:{obj}'
                else:
                    obj_arr = []
                    for split_ele in obj_split:
                        split_ele = f'{namespace}:{split_ele}'
                        obj_arr.append(split_ele)
                    obj = '|'.join(obj_arr)

                if cmds.objExists(obj):
                    cmds.sets(obj, add=dis)

        #
        cmds.select(cl=True)

    # common function
    def openModelPubFileBrowser(self):
        
        selected_version = self.rig_pub_ver.currentItem().text()
        modelPub_dir = self.getRigPubDir() + '/' + selected_version + '/maya'
        modelPub_dir = modelPub_dir.replace('/', '\\')
        print('modelPub_dir = '+ modelPub_dir)
        os.system(f'explorer {modelPub_dir}')


    def openWIPFileBrowser(self):

        wip_dir = self.getSaveDir('work') + '/maya/scenes/increments'
        wip_dir = wip_dir.replace('/', '\\')
        print('wip_dir = '+ wip_dir)
        os.system(f'explorer {wip_dir}')

    # semi common function
    def openPubFileBrowser(self):

        pub_dir = self.getSaveDir('output') + '/shadegeo/shade_main/'+ self.publish_version.currentItem().text() + '/maya'
        print ('pub_dir : '+pub_dir)
        pub_dir = pub_dir.replace('/', '\\')
        os.system(f'explorer {pub_dir}')

    def closeEvent(self, event):

        self.saveCurrentENV()

    def initUI(self):

        # project list
        self.proj_list = QComboBox()
        self.getProjectList()
        self.proj_list.currentIndexChanged.connect(self.getEpisodeList)

        # episode list
        self.episode_list = QListWidget()
        self.episode_list.currentItemChanged.connect(self.getAssetType)
        episode_layout = QVBoxLayout()
        episode_layout.addWidget(self.episode_list)
        episode_grp = QGroupBox('Episode')
        episode_grp.setLayout(episode_layout)

         # shot list
        self.shot_list = QListWidget()
        self.shot_list.currentItemChanged.connect(self.getAssetType)
        shot_layout = QVBoxLayout()
        shot_layout.addWidget(self.shot_list)
        shot_grp = QGroupBox('shot')
        shot_grp.setLayout(shot_layout)


        # asset type
        self.asset_type = QListWidget()
        self.asset_type.currentItemChanged.connect(self.getAssetName)
        asset_type_layout = QVBoxLayout()
        asset_type_layout.addWidget(self.asset_type)
        asset_type_grp = QGroupBox('Asset Type')
        asset_type_grp.setLayout(asset_type_layout)

        # asset name
        self.asset_name = QListWidget()
        self.asset_name.currentItemChanged.connect(self.getMiddleName)
        asset_name_layout = QVBoxLayout()
        asset_name_layout.addWidget(self.asset_name)
        asset_name_grp = QGroupBox('Asset Name')
        asset_name_grp.setLayout(asset_name_layout)

        # asset middle name
        middle_name_label = QLabel('Mid Name')
        self.middle_list = QListWidget()
        self.middle_list.currentItemChanged.connect(self.getRigPubVersion)
        middle_name_layout = QVBoxLayout()
        middle_name_layout.addWidget(middle_name_label)
        middle_name_layout.addWidget(self.middle_list)
        # asset middle name version
        middle_ver_label = QLabel('Asset Pub Ver')
        self.rig_pub_ver = QListWidget()
        self.rig_pub_ver.itemDoubleClicked.connect(self.openModelPubFileBrowser)
        middle_ver_layout = QVBoxLayout()
        middle_ver_layout.addWidget(middle_ver_label)
        middle_ver_layout.addWidget(self.rig_pub_ver)
        # asset reference import
        Asset_ref_btn = QPushButton('Asset Ref import')
        Asset_ref_btn.clicked.connect(self.assetRefBtn)


       
        #
        middle_layout = QHBoxLayout()
        middle_layout.addLayout(middle_name_layout)
        middle_layout.addLayout(middle_ver_layout)
        middle_name_grp = QGroupBox('Rig')
        middle_name_grp.setLayout(middle_layout)
        #
        asset_ref_layout = QVBoxLayout()
        asset_ref_layout.addWidget(middle_name_grp)
        asset_ref_layout.addWidget(Asset_ref_btn)
        

        # column1 layout
        column1_layout = QVBoxLayout()
        #
        column1_row1_layout = QHBoxLayout()
        column1_row1_layout.addWidget(episode_grp)
        column1_row1_layout.addWidget(asset_type_grp)
        column1_row1_layout.addWidget(asset_name_grp)
        column1_row1_layout.addLayout(asset_ref_layout)
        #
        column1_layout.addWidget(self.proj_list)
        column1_layout.addLayout(column1_row1_layout)

        # version
        # wip version list
        self.save_wip_version = QListWidget()
        self.save_wip_version.setFixedWidth(80)
        self.save_wip_version.itemDoubleClicked.connect(self.openWIPFileBrowser)
        save_wip_version_layout = QVBoxLayout()
        save_wip_version_layout.addWidget(self.save_wip_version)
        save_wip_version_grp = QGroupBox('WIP Version')
        save_wip_version_grp.setLayout(save_wip_version_layout)
        # publish version list
        self.publish_version = QListWidget()
        self.publish_version.setFixedWidth(80)
        self.publish_version.itemDoubleClicked.connect(self.openPubFileBrowser)
        publish_version_layout = QVBoxLayout()
        publish_version_layout.addWidget(self.publish_version)
        publish_version_grp = QGroupBox('Publish Version')
        publish_version_grp.setLayout(publish_version_layout)
        # version layout
        version_layout = QHBoxLayout()
        version_layout.addWidget(save_wip_version_grp)
        version_layout.addWidget(publish_version_grp)

        # wip/pub button
        # wip button
        open_wip_btn = QPushButton('Open WIP')
        open_wip_btn.setFixedHeight(35)
        open_wip_btn.clicked.connect(self.openWIPBtn)
        save_wip_btn = QPushButton('WIP Save')
        save_wip_btn.clicked.connect(self.saveWIPBtn)
        wip_btn_layout = QVBoxLayout()
        wip_btn_layout.addWidget(open_wip_btn)
        wip_btn_layout.addWidget(save_wip_btn)
        # publish button 
        publish_btn = QPushButton('Publish')
        publish_btn.clicked.connect(self.publishBtn)
        assign_shader_btn = QPushButton('Assign Shader')
        assign_shader_btn.setFixedHeight(35)
        assign_shader_btn.clicked.connect(self.assignShaderBtn)
        pub_btn_layout = QVBoxLayout()
        pub_btn_layout.addWidget(assign_shader_btn)
        pub_btn_layout.addWidget(publish_btn)
        # button layout
        btn_layout = QHBoxLayout()
        btn_layout.addLayout(wip_btn_layout)
        btn_layout.addLayout(pub_btn_layout)

        # column2 layout
        column2_layout = QVBoxLayout()
        column2_layout.addLayout(version_layout)
        column2_layout.addLayout(btn_layout)

        # main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(column1_layout)
        main_layout.addLayout(column2_layout)
        self.setLayout(main_layout)

        self.setWindowTitle('AniTool')
        self.show()

        cmds.window(self.window_name, e=True, w=835)



AniToolUI()