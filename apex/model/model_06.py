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

import os
import csv
import re
import json
import sys

cmds.loadPlugin( 'AbcExport.mll' )
cmds.loadPlugin( 'AbcImport.mll' )

# PIPELINE_SCRIPT = os.getenv('PIPELINE_SCRIPT').replace('\\', '/')
# if PIPELINE_SCRIPT not in sys.path:
#     sys.path.append(PIPELINE_SCRIPT)

# from src.model.cleanup import checkNotEqualShapename
# from src.model.cleanup import checkPolyVertexNormal

# PROJ_DRIVE = os.getenv('PROJ_DRIVE')
PROJ_DRIVE = r'D:'

def getMayaMainWindow():

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

    return mayaMainWindow


class ModelUI(QWidget):

    def __init__(self):

        super().__init__()

        self.window_name = 'keyring_d420fd2bbcb09e01ac0edd8228e34141'
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name)
        self.setParent(getMayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setObjectName(self.window_name)

        self.initUI()

        self.openCurrentENV()

    ###################
    # common function {
    
    def checkNotEqualShapename():

        shapenames = cmds.ls(typ='mesh', ap=True)

        not_equal_shape_name = {}
        for shapename in shapenames:
            transformname = cmds.listRelatives(shapename, p=True, f=True)[0]

            t_name = re.search('[^\|]*$', transformname). group()
            s_name = re.search('[^\|]*$', shapename). group()

            s_number = re.search('\d*$', s_name).group()
            new_t_name = re.sub(s_number, '', t_name)
            new_t_name = f'{new_t_name}Shape{s_number}'

            if new_t_name != s_name:
                not_equal_shape_name[transformname] =shapename

        return not_equal_shape_name

    def checkNotEqualShapename():

        shapenames = cmds.ls(typ='mesh', ap=True)

        not_equal_shape_name = {}
        for shapename in shapenames:
            transformname = cmds.listRelatives(shapename, p=True, f=True)[0]

            t_name = re.search('[^\|]*$', transformname). group()
            s_name = re.search('[^\|]*$', shapename). group()

            s_number = re.search('\d*$', s_name).group()
            new_t_name = re.sub(s_number, '', t_name)
            new_t_name = f'{new_t_name}Shape{s_number}'

            if new_t_name != s_name:
                not_equal_shape_name[transformname] =shapename

        return not_equal_shape_name

        
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

        proj = self.proj_list.currentText()
        ep = self.episode_list.currentRow()
        asset_type = self.asset_type.currentRow()
        asset_name = self.asset_name.currentRow()

        env_docs = {'project': proj, 'episode': ep,
                    'asset_type': asset_type, 'asset_name': asset_name}

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_model.json'

        with open(env_path, 'w') as f:
            data = json.dumps(env_docs, indent=4, separators=(',',':'), sort_keys=True)
            f.write(data)

    def openCurrentENV(self):

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_model.json'

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
        current_ep = self.episode_list.currentItem().text()
        csv_path = f'{PROJ_DRIVE}/{current_proj}/{current_ep}'
        csv_path = f'{csv_path}/assets/3D/asset_list.csv'

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

        department_dir = self.getDepartmentDir('model/output/geometry')

        self.middle_list.clear()
        self.save_wip_version.clear()
        self.publish_version.clear()
        if os.path.isdir(department_dir):
            middle_names = os.listdir(department_dir)
            if 'model_main' in middle_names:
                middle_names.pop(middle_names.index('model_main'))
                self.middle_list.addItem('model_main')
            for middle_name in sorted(middle_names):
                self.middle_list.addItem(middle_name)
        else:
            self.middle_list.addItem('model_main')

    def addMiddleName(self):

        middle_name = self.middle_edit.text()

        self.middle_list.addItem(middle_name)

        self.middle_edit.clear()
        self.middle_list.clearSelection()

    def getDepartmentDir(self, depart=None):

        """
        depart:
            mod, tex, lookdev
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

        department_dir = self.getDepartmentDir('model')
        middle_name = self.middle_list.currentItem().text()

        if 'output' in save_type:
            save_dir = f'{department_dir}/{save_type}/geometry/{middle_name}'
        else:
            save_dir = f'{department_dir}/{save_type}/{middle_name}/maya/scenes/increments'


        
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

        self.save_wip_version.clear()
        wip_dir = self.getSaveDir('work')
        
        if os.path.isdir(wip_dir):
            for wip_file in sorted(os.listdir(wip_dir)):
                re_match = re.search('_(v\d{3}).mb$', wip_file)
                if re_match:
                    self.save_wip_version.addItem(re_match.group(1))

        self.publish_version.clear()
        pub_dir = self.getSaveDir('output')
        
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
        middle_name = self.middle_list.currentItem().text()

        save_file = f'{asset_name}_{middle_name}'
        save_file = f'{save_file}_{save_version}.{save_ext}'

        return save_file

    # common function }
    ###################

    # common function
    def openWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        wip_dir = self.getSaveDir('work')
        selected_version = self.save_wip_version.currentItem().text()
        wip_file = self.getSaveFile(selected_version, 'mb')
        wip_path = f'{wip_dir}/{wip_file}'

        cmds.file(wip_path, o=True, f=True)

    def saveWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save the file?'):
            return 0

        # # check different shapenode name
        # if len(self.checkNotEqualShapename()):
        #     errBox = QMessageBox()
        #     errBox.setText('Not euqal shapenode name')
        #     errBox.exec_()
        #     cmds.error('Not equal shapenode name.')

        # # check normal
        # if self.poly_vertex_normal.checkState() == Qt.Checked:
        #     checkPolyVertexNormal()

        # make WIP maya dir
        wip_maya_dir = self.getSaveDir('work')
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)

        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)
        wip_version = f'v{str(version_num).zfill(3)}'
        wip_maya_file = self.getSaveFile(wip_version, 'mb')
        self.wip_maya_path = f'{wip_maya_dir}/{wip_maya_file}'

        # save file

        self.mayaCleanup()
        cmds.file(rn=self.wip_maya_path)
        cmds.file(s=True, f=True)

        # update version list
        self.getVersion()

    # semi common function
    def openPubBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0
        
        selected_version = self.publish_version.currentItem().text()
        pub_dir = self.getSaveDir('output') + '/' + selected_version +'/maya'
        pub_file = self.getSaveFile(selected_version, 'mb')
        pub_path = f'{pub_dir}/{pub_file}'

        cmds.file(pub_path, o=True, f=True)

    def publishBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save the file?'):
            return 0

        # check asset_grp 
        asset_name = self.asset_name.currentItem().text()
        print ('asset_name : '+asset_name)
        if not cmds.objExists(f'{asset_name}_grp'):
            errBox = QMessageBox()
            errBox.setText(f'Does not exsit {asset_name}_grp')
            # errBox.exec_()
            # cmds.error(f'Does not exsit {asset_name}_grp')

        ############
        # save WIP #
        ############



        # check different shapenode name

        # if len(self.checkNotEqualShapename()):
        #     errBox = QMessageBox()
        #     errBox.setText('Not euqal shapenode name')
        #     errBox.exec_()
        #     cmds.error('Not equal shapenode name.')



        # check normal
        
        if self.poly_vertex_normal.checkState() == Qt.Checked:
            for mesh in cmds.ls(typ='mesh', ap=True):
                tnode = cmds.listRelatives(mesh, p=True, f=True)[0]

                edge_count = cmds.polyEvaluate(tnode, e=True) - 1
                cmds.polySoftEdge(f'{tnode}.e[0:{edge_count}]', a=0) # setToFace
                cmds.polySoftEdge(tnode, a=30, ch=True) # soften/harden edge
                cmds.delete(all=True, ch=True)
            cmds.select(cl=True)


        # make WIP maya dir
        wip_maya_dir = self.getSaveDir('work')
        
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)
        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)-1
        wip_version = f'v{str(version_num).zfill(3)}'
        wip_maya_file = self.getSaveFile(wip_version, 'mb')
        self.wip_maya_path = f'{wip_maya_dir}/{wip_maya_file}'

        # save file

        self.mayaCleanup()
        cmds.file(rn=self.wip_maya_path)
        cmds.file(s=True, f=True)

        ################
        # publish maya #
        ################
        # asset / middle name
        asset_name = self.asset_name.currentItem().text()
        middle_name = self.middle_list.currentItem().text()
        # make publish maya path

        pub_maya_path = self.getSaveDir('output')+'/'+wip_version+'/maya'
        
        pub_maya_file = self.getSaveFile(wip_version, 'mb')



        # make publish maya dir
        
        if not os.path.isdir(pub_maya_path):
            os.makedirs(pub_maya_path)
        else:
            self.errorMessage('!! Pub version is already Exist !!')
            return 0
        # select group
        try:
            cmds.select(f'{asset_name}_grp', r=True)
        except:
            cmds.select('GEO', r=True)
        
        # selected group maya export
        pub_maya_path = f'{pub_maya_path}/{pub_maya_file}'
        cmds.file(pub_maya_path, f=True, op='v=0', typ='mayaBinary', es=True)

        ###################
        # publish alembic #
        ###################

        pub_abc_path = self.getSaveDir('output')+'/' + wip_version + '/alembic'
        pub_abc_file = self.getSaveFile(wip_version, 'abc')
        
        # make publish alembic dir
       
        if not os.path.isdir(pub_abc_path):
            os.makedirs(pub_abc_path)
        pub_abc_path = pub_abc_path+'/'+pub_abc_file
        
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


        # select group alembic export

        selectGroup = cmds.ls(sl=1,sn=True)
        abc_export_cmd = 'AbcExport -j '
        abc_export_cmd += '"-frameRange 1 1 -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa '
        abc_export_cmd += '-root |' + selectGroup[0]
        abc_export_cmd += ' -file ' + pub_abc_path + '"'
        mel.eval(abc_export_cmd)

        # version update

        self.getVersion()

    # common function
    def openWIPFileBrowser(self):

        wip_dir = self.getSaveDir('work')
        wip_dir = wip_dir.replace('/', '\\')
        
        os.system(f'explorer {wip_dir}')

    def openPubFileBrowser(self):
        selected_version = self.publish_version.currentItem().text()
        pub_dir = self.getSaveDir('output') +'/'+selected_version+ '/maya'
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

        # middle name
        self.middle_edit = QLineEdit()
        self.middle_edit.returnPressed.connect(self.addMiddleName)
        self.middle_list = QListWidget()
        self.middle_list.currentItemChanged.connect(self.getVersion)
        ts_different_btn = QPushButton('Different Shapename')
        middle_name_layout = QVBoxLayout()
        middle_name_layout.addWidget(self.middle_edit)
        middle_name_layout.addWidget(self.middle_list)
        middle_name_grp = QGroupBox('Middle Name')
        middle_name_grp.setLayout(middle_name_layout)

        # column1 layout
        column1_layout = QVBoxLayout()
        #
        column1_row1_layout = QHBoxLayout()
        column1_row1_layout.addWidget(episode_grp)
        column1_row1_layout.addWidget(asset_type_grp)
        column1_row1_layout.addWidget(asset_name_grp)
        column1_row1_layout.addWidget(middle_name_grp)
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

        # poly vertex normal
        self.poly_vertex_normal = QCheckBox('Poly Vertex Normal Cleanup')

        # wip/pub button
        # wip button
        open_wip_btn = QPushButton('Open WIP')
        open_wip_btn.setFixedHeight(35)
        open_wip_btn.clicked.connect(self.openWIPBtn)
        save_wip_btn = QPushButton('WIP Save')
        save_wip_btn.clicked.connect(self.saveWIPBtn)
        # wip button layout
        wip_btn_layout = QVBoxLayout()
        wip_btn_layout.addWidget(open_wip_btn)
        wip_btn_layout.addWidget(save_wip_btn)
        # publish button
        open_pub_btn = QPushButton('Open Pub')
        open_pub_btn.setFixedHeight(35)
        open_pub_btn.clicked.connect(self.openPubBtn)
        publish_btn = QPushButton('Publish')
        publish_btn.clicked.connect(self.publishBtn)
        # pub button layout
        pub_btn_layout = QVBoxLayout()
        pub_btn_layout.addWidget(open_pub_btn)
        pub_btn_layout.addWidget(publish_btn)
        # btn layout
        btn_layout = QHBoxLayout()
        btn_layout.addLayout(wip_btn_layout)
        btn_layout.addLayout(pub_btn_layout)

        # column2 layout
        column2_layout = QVBoxLayout()
        column2_layout.addLayout(version_layout)
        column2_layout.addWidget(self.poly_vertex_normal)
        column2_layout.addLayout(btn_layout)

        # main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(column1_layout)
        main_layout.addLayout(column2_layout)
        self.setLayout(main_layout)

        self.setWindowTitle('Modeling')
        self.show()
        
        cmds.window(self.window_name, e=True, w=750)


ModelUI()