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

import os
import sys
import csv
import re
import json

# PROJ_DRIVE = os.getenv('PROJ_DRIVE')
PROJ_DRIVE = r'D:'


def getMayaMainWindow():

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

    return mayaMainWindow

class LookdevUI(QWidget):

    def __init__(self):

        super().__init__()

        self.window_name = 'keyring_1894d9507f34d4bb0c844634b69f6383'
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

    def saveCurrentENV(self):

        proj       = self.proj_list.currentText()
        ep         = self.episode_list.currentRow()
        asset_type = self.asset_type.currentRow()
        asset_name = self.asset_name.currentRow()

        env_docs = {'project': proj,          'episode': ep,
                    'asset_type': asset_type, 'asset_name': asset_name}

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_lookdev.json'

        with open(env_path, 'w') as f:
            data = json.dumps(env_docs, indent=4, separators=(',',':'), sort_keys=True)
            f.write(data)

    def openCurrentENV(self):

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_lookdev.json'

        with open(env_path) as f:
            env_docs = json.load(f)

        self.proj_list.setCurrentText(env_docs['project'])
        self.episode_list.setCurrentRow(env_docs['episode'])
        self.asset_type.setCurrentRow(env_docs['asset_type'])
        self.asset_name.setCurrentRow(env_docs['asset_name'])

    def readAssetCSV(self):

        current_proj = self.proj_list.currentText()
        current_ep   = self.episode_list.currentItem().text()
        csv_path     = f'{PROJ_DRIVE}/{current_proj}/{current_ep}'
        csv_path     = f'{csv_path}/assets/3D/asset_list.csv'
        print (csv_path)

        bgPath = f'{PROJ_DRIVE}/{current_proj}/{current_ep}/assets/3D/bg'
        characterPath = f'{PROJ_DRIVE}/{current_proj}/{current_ep}/assets/3D/character'
        propPath = f'{PROJ_DRIVE}/{current_proj}/{current_ep}/assets/3D/prop'

        bgDirectoryList = os.listdir(bgPath)
        characterDirectoryList = os.listdir(characterPath)
        propDirectoryList = os.listdir(propPath)



        bgList = [a for a in bgDirectoryList if os.path.isdir((bgPath+'\\'+a))]
        characterList = [a for a in characterDirectoryList if os.path.isdir((characterPath+'\\'+a))]
        propList = [a for a in propDirectoryList if os.path.isdir((propPath+'\\'+a))]

        f = open(csv_path,'w', newline='')
        wr = csv.writer(f)

        for i in bgList:
            wr.writerow(['bg',i])
        
        for i in characterList:
            wr.writerow(['character',i])
        
        for i in propList:
            wr.writerow(['prop',i])

        f.close()


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

        department_dir = self.getDepartmentDir('mod')

        self.middle_list.clear()
        if os.path.isdir(department_dir):
            middle_names = os.listdir(department_dir)
            if 'main' in middle_names:
                middle_names.pop(middle_names.index('main'))
                self.middle_list.addItem('main')
            for middle_name in sorted(middle_names):
                self.middle_list.addItem(middle_name)
        else:
            self.middle_list.addItem('main')

        self.getVersion()

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

        department_dir = self.getDepartmentDir('lookdev')

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

        self.save_wip_version.clear()
        wip_dir = self.getSaveDir('wip') + '/maya'
        if os.path.isdir(wip_dir):
            for wip_file in sorted(os.listdir(wip_dir)):
                re_match = re.search('_(v\d{3}).mb$', wip_file)
                if re_match:
                    self.save_wip_version.addItem(re_match.group(1))

        self.publish_version.clear()
        pub_dir = self.getSaveDir('pub') + '/maya_shd'
        if os.path.isdir(pub_dir):
            for pub_file in sorted(os.listdir(pub_dir)):
                re_match = re.search('_(v\d{3}).mb$', pub_file)
                if re_match:
                    self.publish_version.addItem(re_match.group(1))

    # semi common
    def getSaveFile(self, save_version=None, save_ext=None):

        ep = self.episode_list.currentItem().text()
        asset_name = self.asset_name.currentItem().text()

        save_file = f'{ep}_{asset_name}_lookdev'
        save_file = f'{save_file}_{save_version}.{save_ext}'

        return save_file

    # common function }
    ###################

    ########################
    # model data reference {

    def getModPubVersion(self):

        self.model_pub_ver.clear()

        pub_dir = self.getModPubDir() + '/abc'

        if os.path.isdir(pub_dir):
            for pub_file in sorted(os.listdir(pub_dir)):
                re_match = re.search('_(v\d{3}).abc$', pub_file)
                if re_match:
                    self.model_pub_ver.addItem(re_match.group(1))

    def getModPubDir(self):

        """
        depart:
            mod, tex, lookdev
        """

        department_dir = self.getDepartmentDir('mod')
        middle_name = self.middle_list.currentItem().text()

        save_dir = f'{department_dir}/{middle_name}/pub'

        return save_dir

    def getModPubFile(self, save_version=None):

        ep = self.episode_list.currentItem().text()
        asset_name = self.asset_name.currentItem().text()
        middle_name = self.middle_list.currentItem().text()

        save_file = f'{ep}_{asset_name}_mod_{middle_name}'
        save_file = f'{save_file}_{save_version}.abc'

        return save_file

    def modelRefBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        selected_version = self.model_pub_ver.currentItem().text()
        pub_file = self.getModPubFile(selected_version)

        pub_dir = self.getModPubDir() + '/abc'

        pub_path = f'{pub_dir}/{pub_file}'

        namespace = re.search('^[^\.]*', pub_file).group()
        cmds.file(pub_path, r=True, typ='Alembic', gl=True, mnc=False, ns=namespace)

    def modelRefUpdateBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to update the file?'):
            return 0

        selected_version = self.model_pub_ver.currentItem().text()
        mod_pub_abc_file = self.getModPubFile(selected_version)
        mod_pub_abc_dir = self.getModPubDir() + '/abc'
        mod_pub_abc_path = f'{mod_pub_abc_dir}/{mod_pub_abc_file}'

        reference_name = str()
        reference_path = cmds.file(q=True, r=True)[0]
        reference_name = cmds.file(reference_path, q=True, rfn=True)
        cmds.file(mod_pub_abc_path, lr=reference_name)

    ########################
    # model data reference #
    ########################

    # common function
    def openWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        wip_dir = self.getSaveDir('wip') + '/maya'
        selected_version = self.save_wip_version.currentItem().text()
        wip_file = self.getSaveFile(selected_version, 'mb')
        wip_path = f'{wip_dir}/{wip_file}'

        cmds.file(wip_path, o=True, f=True)

    def saveWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save the file?'):
            return 0

        # make WIP maya dir
        wip_maya_dir = self.getSaveDir('wip') + '/maya'
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)

        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)
        wip_version = f'v{str(version_num).zfill(3)}'
        wip_maya_file = self.getSaveFile(wip_version, 'mb')
        wip_maya_path = f'{wip_maya_dir}/{wip_maya_file}'

        # save file
        cmds.file(rn=wip_maya_path)
        cmds.file(s=True, f=True)

        # update version list
        self.getVersion()

    def publishBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save the file?'):
            return 0

        # save WIP
        # make WIP maya dir
        wip_maya_dir = self.getSaveDir('wip') + '/maya'
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)
        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)
        wip_version = f'v{str(version_num).zfill(3)}'
        wip_maya_file = self.getSaveFile(wip_version, 'mb')
        wip_maya_path = f'{wip_maya_dir}/{wip_maya_file}'
        # save file
        cmds.file(rn=wip_maya_path)
        cmds.file(s=True, f=True)

        # make Publish dir
        pub_maya_dir = self.getSaveDir('pub') + '/maya_shd'
        if not os.path.isdir(pub_maya_dir):
            os.makedirs(pub_maya_dir)
        pub_json_dir = self.getSaveDir('pub') + '/json'
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
                        obj = re.search('[^:]*$', obj_split[0]).group()
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
                    obj = re.search('[^:]*$', obj_split[0]).group()
                else:
                    obj_arr = []
                    for split_ele in obj_split:
                        split_name = re.search('[^:]*$', split_ele).group()
                        obj_arr.append(split_name)
                    obj = '|'.join(obj_arr)
                shader_dict['vray_displacement'][dis].append(obj)
        #
        cmds.select(cl=True)

        #  regex string
        pattern_maya_str = '/lookdev/wip/maya'
        dst_maya_str = '/lookdev/pub/maya_shd'
        dst_json_str = '/lookdev/pub/json'

        # export json
        pub_maya_path = re.sub(pattern_maya_str, dst_maya_str, wip_maya_path)
        pub_json_path = re.sub(pattern_maya_str, dst_json_str, wip_maya_path)
        pub_json_path = re.sub('mb$', 'json', pub_json_path)
        with open(pub_json_path, 'w') as f:
            data = json.dumps(shader_dict, indent=4, separators=(',',':'), sort_keys=True)
            f.write(data)

        # export shader
        cmds.select([se for se in cmds.ls(typ='shadingEngine') if not re.search('^init', se)], ne=True, r=True)
        cmds.file(pub_maya_path, op='v=0;', typ='mayaBinary', pr=True, es=True)
        cmds.select(cl=True)

        # update version
        self.getVersion()

    def assignShaderBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to assign shader?'):
            return 0

        # get model namespace
        selected = cmds.ls(sl=True)
        namespace = re.search('^[^:]*', selected[0]).group()

        # load shader json
        pub_dir = self.getSaveDir('pub') + '/json'
        selected_version = self.publish_version.currentItem().text()
        pub_file = self.getSaveFile(selected_version, 'json')
        json_path = f'{pub_dir}/{pub_file}'
        #
        with open(json_path) as f:
            shader_dict = json.load(f)

        # import shader without namespace
        selected_version = self.publish_version.currentItem().text()
        shader_pub_dir = self.getSaveDir('pub') + '/maya_shd'
        shader_pub_file = self.getSaveFile(selected_version, 'mb')
        shader_pub_path = f'{shader_pub_dir}/{shader_pub_file}'
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
    def openWIPFileBrowser(self):

        wip_dir = self.getSaveDir('wip') + '/maya'
        wip_dir = wip_dir.replace('/', '\\')
        os.system(f'explorer {wip_dir}')

    # semi common function
    def openPubFileBrowser(self):

        pub_dir = self.getSaveDir('pub') + '/maya_shd'
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

        # model middle name
        middle_name_label = QLabel('Mid Name')
        self.middle_list = QListWidget()
        self.middle_list.currentItemChanged.connect(self.getModPubVersion)
        middle_name_layout = QVBoxLayout()
        middle_name_layout.addWidget(middle_name_label)
        middle_name_layout.addWidget(self.middle_list)
        # model middle name version
        middle_ver_label = QLabel('Pub Ver')
        self.model_pub_ver = QListWidget()
        self.model_pub_ver.setFixedWidth(80)
        middle_ver_layout = QVBoxLayout()
        middle_ver_layout.addWidget(middle_ver_label)
        middle_ver_layout.addWidget(self.model_pub_ver)
        # model reference
        model_ref_btn = QPushButton('Model Reference')
        model_ref_btn.clicked.connect(self.modelRefBtn)
        # model reference update
        model_ref_update_btn = QPushButton('Model Update')
        model_ref_update_btn.clicked.connect(self.modelRefUpdateBtn)
        #
        middle_layout = QHBoxLayout()
        middle_layout.addLayout(middle_name_layout)
        middle_layout.addLayout(middle_ver_layout)
        middle_name_grp = QGroupBox('Model')
        middle_name_grp.setLayout(middle_layout)
        #
        model_ref_layout = QVBoxLayout()
        model_ref_layout.addWidget(middle_name_grp)
        model_ref_layout.addWidget(model_ref_btn)
        model_ref_layout.addWidget(model_ref_update_btn)

        # column1 layout
        column1_layout = QVBoxLayout()
        #
        column1_row1_layout = QHBoxLayout()
        column1_row1_layout.addWidget(episode_grp)
        column1_row1_layout.addWidget(asset_type_grp)
        column1_row1_layout.addWidget(asset_name_grp)
        column1_row1_layout.addLayout(model_ref_layout)
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

        self.setWindowTitle('Lookdev')
        self.show()

        cmds.window(self.window_name, e=True, w=835)



LookdevUI()