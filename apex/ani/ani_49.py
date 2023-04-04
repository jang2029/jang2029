
# maya 2022
# mayapy 3.7.7
toolVersion = 'ani_049.py'
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

import os, shutil, stat, datetime
import sys
import csv
import re
import json

cmds.loadPlugin( 'AbcExport.mll' )
cmds.loadPlugin( 'AbcImport.mll' )
cmds.loadPlugin( 'atomImportExport.mll' )
cmds.loadPlugin( 'fbxmaya.mll' )
cmds.loadPlugin( 'gameFbxExporter.mll' )
cmds.loadPlugin( 'Type.mll' )

# PROJ_DRIVE = os.getenv('PROJ_DRIVE')

PROJ_DRIVE = r'P:'

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




    ########################## SET PROJETC PATH #######################

    def getAssetPath(self, prj):
        
        proj = self.proj_list.currentText()
        current_ep = self.episode_list.currentItem().text()

        if prj == 'TGR':
            asset_path = f'{PROJ_DRIVE}/{proj}/assets/3D'

        if prj == 'projects':
            asset_path = f'{PROJ_DRIVE}/{proj}/{current_ep}/assets/3D'

        return asset_path
    
            
    def getEpiPath(self, prj):
        
        proj = self.proj_list.currentText()

        if prj == 'TGR':
            EPipath = f'{PROJ_DRIVE}/{proj}/sequences'

        if prj == 'projects':
            EPipath = f'{PROJ_DRIVE}/{proj}'
        
                
        return EPipath


    def getShotPath(self, prj):

        current_ep   = self.episode_list.currentItem().text()
        proj = self.proj_list.currentText()

        if prj == 'TGR':
            shotPath = f'{PROJ_DRIVE}/{proj}/sequences/{current_ep}'

        if prj == 'projects':
            shotPath = f'{PROJ_DRIVE}/{proj}/{current_ep}/sequences'

        return shotPath

    ########################### END ##################################



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
        msgBox.setStyleSheet("color: rgb(255, 0, 0);")
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

        

    def rename_refNode(self):

        #################################################################
        ###########   rename referenceNode Name & Namespace   ###########
        #################################################################

        list = []
        ref_list = mel.eval('ls -type reference')

        for i in ref_list:
                if not 'Fx' in i and not 'shared' in i:
                        if cmds.referenceQuery( i, isLoaded = True ):            
                            list.append(i)

        print (list)


        for i in list:        
                refFile = cmds.referenceQuery( i,filename=True)
                name = cmds.referenceQuery( i,filename=True, shortName=True ).split('.')[0]
                cmds.file( refFile, e=1, namespace=name)
                cmds.lockNode( i, lock=False)
                cmds.rename( i, name+'RN' )
        list = []
        
        ########################    END    ##########################

    def saveCurrentENV(self):

        proj         =  self.proj_list.currentText()
        ep           =  self.episode_list.currentRow()
        asset_type   =  self.asset_type.currentRow()
        asset_name   =  self.asset_name.currentRow()
        shot_name    =  self.shot_list.currentRow()
        middle_name  =  self.middle_list.currentRow()
        rig_pub_ver  =  self.rig_pub_ver.currentRow()
        pub_rig      =  self.pub_rig.currentRow()
        layoutWipVer =  self.layoutWip_list.currentRow()
        layoutPubVer =  self.layoutPub_list.currentRow()
        aniWipVer    =  self.aniWip_list.currentRow()
        aniPubVer    =  self.aniPub_list.currentRow()

        env_docs = {
                    'project': proj,          'episode': ep,
                    'asset_type': asset_type, 'asset_name': asset_name,
                    'shot_name': shot_name, 'middle_name': middle_name, 'rig_pub_ver': rig_pub_ver, 'pub_rig' : pub_rig,
                    'layoutWipVer':layoutWipVer, 'layoutPubVer':layoutPubVer,
                    'aniWipVer':aniWipVer, 'aniPubVer':aniPubVer
                    }

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
        self.shot_list.setCurrentRow(env_docs['shot_name'])
        self.middle_list.setCurrentRow(env_docs['middle_name'])
        self.rig_pub_ver.setCurrentRow(env_docs['rig_pub_ver'])
        self.pub_rig.setCurrentRow(env_docs['pub_rig'])
        self.layoutWip_list.setCurrentRow(env_docs['layoutWipVer'])
        self.layoutPub_list.setCurrentRow(env_docs['layoutPubVer'])
        self.aniWip_list.setCurrentRow(env_docs['aniWipVer'])
        self.aniPub_list.setCurrentRow(env_docs['aniPubVer'])

    def readAssetCSV(self):
        ###########################
        # asset_list.csv 자동만들기#
        ###########################
        proj = self.proj_list.currentText()
        asset_path = self.getAssetPath(proj)
        csv_path = f'{asset_path}/asset_list.csv'
        
        

        print (csv_path)

        bgPath = f'{asset_path}/bg'
        characterPath = f'{asset_path}/character'
        propPath = f'{asset_path}/prop'
        bgpropPath = f'{asset_path}/bgprop'
        fxPath = f'{asset_path}/fx'

        if not os.path.isdir(bgPath): os.makedirs(bgPath)
        if not os.path.isdir(characterPath): os.makedirs(characterPath)
        if not os.path.isdir(propPath): os.makedirs(propPath)
        if not os.path.isdir(bgpropPath): os.makedirs(bgpropPath)
        if not os.path.isdir(fxPath): os.makedirs(fxPath)

        bgDirectoryList = os.listdir(bgPath)
        characterDirectoryList = os.listdir(characterPath)
        propDirectoryList = os.listdir(propPath)
        bgpropDirectoryList = os.listdir(bgpropPath)
        fxDirectoryList = os.listdir(fxPath)

        bgList = [a for a in bgDirectoryList if os.path.isdir((bgPath+'\\'+a))]
        characterList = [a for a in characterDirectoryList if os.path.isdir((characterPath+'\\'+a))]
        propList = [a for a in propDirectoryList if os.path.isdir((propPath+'\\'+a))]
        bgpropList = [a for a in bgpropDirectoryList if os.path.isdir((bgpropPath+'\\'+a))]
        fxList = [a for a in fxDirectoryList if os.path.isdir((fxPath+'\\'+a))]

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

        for i in fxList:
            wr.writerow(['fx',i])

       
        
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
        
        self.episode_list.clear()

        proj = self.proj_list.currentText()
        ep_path = self.getEpiPath(proj)

        if os.path.isdir(ep_path):
            for ep_name in sorted(os.listdir(ep_path)):
                if os.path.isdir(f'{ep_path}/{ep_name}'):
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
        if not os.path.isdir(department_dir):
            os.makedirs(department_dir)
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

    def getRigPub(self):

        self.pub_rig.clear()

        proj = self.proj_list.currentText()
        asset_path = self.getAssetPath(proj)
        asset_type = self.asset_type.currentItem().text()
        asset_name = self.asset_name.currentItem().text()
        middle_name = self.middle_list.currentItem().text()
        rig_pubVer = self.rig_pub_ver.currentItem().text()

        rig_pubPath = f'{asset_path}/{asset_type}/{asset_name}/rig/output/rig/{middle_name}/{rig_pubVer}/maya/'
        
        
        if not os.path.isdir(rig_pubPath):
            os.makedirs(rig_pubPath)

        print('rig_pubPath:'+rig_pubPath)

       
        for file_name in os.listdir(rig_pubPath):
            if os.path.splitext(file_name)[1] == '.mb':
                self.pub_rig.addItem(file_name)



    def getDepartmentDir(self, depart=None):

        """
        depart:
            mod, tex, lookdev, rig
        """
        
        proj = self.proj_list.currentText()
        asset_path = self.getAssetPath(proj)

        asset_type = self.asset_type.currentItem().text()
        asset_name = self.asset_name.currentItem().text()


        department_dir = f'{asset_path}/{asset_type}/{asset_name}'
        department_dir = f'{department_dir}/{depart}'

        return department_dir



    def getShotList(self):

        self.shot_list.clear()
        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)

        for shot_name in sorted(os.listdir(shot_path)):
            if os.path.isdir(f'{shot_path}/{shot_name}'):
                self.shot_list.addItem(shot_name)

    def getLayoutWip(self):

        self.layoutWip_list.clear()

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        
        layoutWip_path = f'{shot_path}/{currentShot}/layout/work/maya/scene'

        if not os.path.isdir(layoutWip_path):
            os.makedirs(layoutWip_path)

        for file_name in sorted(os.listdir(layoutWip_path)):
            if os.path.isfile(f'{layoutWip_path}/{file_name}'):
                if os.path.splitext(file_name)[1] == '.mb':
                    self.layoutWip_list.addItem(file_name)

    def getLayoutPub(self):

        self.layoutPub_list.clear()

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        
        layoutPub_path = f'{shot_path}/{currentShot}/layout/output/maya/scene'

        
        if not os.path.isdir(layoutPub_path):
            os.makedirs(layoutPub_path)

        print('layoutPub_path:'+layoutPub_path)

        for version in sorted(os.listdir(layoutPub_path)):
            
            for file_name in os.listdir(f'{layoutPub_path}/{version}'):
                if os.path.isfile(f'{layoutPub_path}/{version}/{file_name}'):
                    if os.path.splitext(file_name)[1] == '.mb':
                        self.layoutPub_list.addItem(file_name)

    def getAniWip(self):

        self.aniWip_list.clear()

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        aniWip_path = f'{shot_path}/{currentShot}/animation/work/maya/scene'

        if not os.path.isdir(aniWip_path):
            os.makedirs(aniWip_path)

        for file_name in sorted(os.listdir(aniWip_path)):
            if os.path.isfile(f'{aniWip_path}/{file_name}'):
                if os.path.splitext(file_name)[1] == '.mb':
                    self.aniWip_list.addItem(file_name)

    def getAniPub(self):

        self.aniPub_list.clear()

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
            
        aniPub_path = f'{shot_path}/{currentShot}/animation/output/maya/showcase_animation'
            
        if not os.path.isdir(aniPub_path):
            os.makedirs(aniPub_path)

        print('aniPub_path:'+aniPub_path)
        for version in sorted(os.listdir(aniPub_path)):
            for file_name in os.listdir(f'{aniPub_path}/{version}'):
                if os.path.isfile(f'{aniPub_path}/{version}/{file_name}'):
                    if os.path.splitext(file_name)[1] == '.mb':
                        self.aniPub_list.addItem(file_name)







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
        if not os.path.isdir(pub_dir):
            os.makedirs(pub_dir)
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
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        print ('save_dir = ' + save_dir)


        return save_dir

    def getRigPubFile(self, save_version=None):


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
        pub_file = self.pub_rig.currentItem().text()
        pub_dir = self.getRigPubDir() + '/'+ selected_version + '/maya'
        
        print ('pub_file = '+pub_file)
        print ('pub_dir = '+pub_dir)
        pub_path = f'{pub_dir}/{pub_file}'
        namespace = f'{pub_file.split(".")[0]}'
        print (pub_path)

        cmds.file(pub_path, ignoreVersion = True, r=True, gl=True, mnc=False, ns=namespace)
        

    def assetRepBtn(self):

        selname = {}

        if QMessageBox.No == self.confirmMessage('Do you want to replace this Asset?'):
            return 0
        
        selname = cmds.ls(sl=True)

        if len(selname) == 0:
            self.errorMessage('Select Target ref Node!!')
            return 0
        else:
            selname = cmds.ls(sl=True)[0]

        refNode = cmds.ls(type = 'reference')
        pub_dir = self.getRigPubDir()

        selVer     = self.rig_pub_ver.currentItem().text()
        sourceFile = self.pub_rig.currentItem().text()

        sourceFile = f'{pub_dir}/{selVer}/maya/{sourceFile}'
        command = 'file -loadReference '
        command += '"'+ selname + '"'+' -options "v=0;" '
        command += '"'+ sourceFile + '"'
        print ('sourceFile : '+sourceFile)
        print ('selname : '+selname)
        print ('command'+command)
        
        if selname in refNode:
            mel.eval(command)
        else:
            self.errorMessage('Select Target ref Node!!')
            return 0
    

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

    def layoutOpenWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.layoutWip_list.currentItem().text()
        wip_file     = f'{shot_path}/{currentShot}/layout/work/maya/scene/{selected_file}'
        print ('wip_file = '+wip_file)
        cmds.file(wip_file, o=True, f=True)

    def layoutSaveWIPBtn(self):

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        wip_path = f'{shot_path}/{currentShot}/layout/work/maya/scene'
        file_list = os.listdir(wip_path)
        mb_list=[file for file in file_list if file.endswith('.mb')]

        if len(mb_list) == 0:
            filename = f'{currentShot}_layout_v001'
        else :
            version = mb_list[-1]
            version = version.split('.')[0]
            version = 'v'+str(int(version[-3:])+1).zfill(3)
            filename = currentShot + '_layout_'
            filename = filename + version

        wip_path = f'{wip_path}/{filename}'

        print ('wip_path : '+wip_path)
        self.mayaCleanup()
        cmds.file(rn=wip_path)
        cmds.file(s=True, f=True)

        self.getLayoutWip()

    def layoutWipOpenFileBrowser(self):

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        wip_file     = f'{shot_path}/{currentShot}/layout/work/maya/scene'
        os.startfile(wip_file)

    def layoutOpenPubBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.layoutPub_list.currentItem().text()
        version = selected_file.split('.')[0]
        version = version.split('_')[-1]

  
        wip_file     = f'{shot_path}/{currentShot}/layout/output/maya/scene/{version}/{selected_file}'
        print ('wip_file = '+wip_file)
        cmds.file(wip_file, o=True, f=True)

    def layoutSavePubBtn(self):

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        raw_name, extension = os.path.splitext(filename)
        version = raw_name.split('_')[-1]

        pub_path = f'{shot_path}/{currentShot}/layout/output/maya/scene'
                
        filename = f'{currentShot}_layout_'
        filename = filename + version

        pub_path = f'{pub_path}/{version}'
        if not os.path.isdir(pub_path):
            os.makedirs(pub_path)

        pub_file = f'{pub_path}/{filename}'
        self.mayaCleanup()
        cmds.file(rn=pub_file)
        cmds.file(s=True, f=True)

        self.getLayoutPub()

    def layoutPubOpenFileBrowser(self):
        
        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.layoutPub_list.currentItem().text()
        version = selected_file.split('.')[0]
        version = version.split('_')[-1]
        pub_file     = f'{shot_path}/{currentShot}/layout/output/maya/scene/{version}'
        os.startfile(pub_file)

    def aniWipOpenFileBrowser(self):

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        wip_file     = f'{shot_path}/{currentShot}/animation/work/maya/scene'
        os.startfile(wip_file)

    def aniPubOpenFileBrowser(self):

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.aniPub_list.currentItem().text()
        version = selected_file.split('.')[0]
        version = version.split('_')[-1]
        pub_file     = f'{shot_path}/{currentShot}/animation/output/maya/showcase_animation/{version}'
        os.startfile(pub_file)

    def aniOpenWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.aniWip_list.currentItem().text()
        ani_file     = f'{shot_path}/{currentShot}/animation/work/maya/scene/{selected_file}'
        print ('ani_file = '+ ani_file)
        cmds.file(ani_file, o=True, f=True)

    def aniSaveWIPBtn(self):

        self.rename_refNode()        

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        wip_path = f'{shot_path}/{currentShot}/animation/work/maya/scene'
        file_list = os.listdir(wip_path)
        mb_list=[file for file in file_list if file.endswith('.mb')]

        if len(mb_list) == 0:
            filename = f'{currentShot}_animation_v001'
        else :
            version = mb_list[-1]
            version = version.split('.')[0]
            version = 'v'+str(int(version[-3:])+1).zfill(3)
            filename = currentShot + '_animation_'
            filename = filename + version

        wip_path = f'{wip_path}/{filename}'

        print ('wip_path : '+wip_path)
        self.mayaCleanup()
        cmds.file(rn=wip_path)
        cmds.file(s=True, f=True)

        self.getAniWip()



    def aniSavePubBtn(self):

        
        mel.eval('animLayer -edit -lock 0 BaseAnimation')
        self.rename_refNode()
        cmds.file(s=True, f=True)

        cmds.cycleCheck(evaluation= False)
        proj = self.proj_list.currentText()
        asset_path = self.getAssetPath(proj)
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        csv_path = f'{asset_path}/asset_list.csv'

        startFrame = cmds.playbackOptions( q=True,min=True )
        endFrame  = cmds.playbackOptions( q=True,max=True )
        pub_path = f'{shot_path}/{currentShot}/animation/output/maya/showcase_animation'
        if not os.path.isdir(pub_path):
            os.makedirs(pub_path)

        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        raw_name, extension = os.path.splitext(filename)
        version = raw_name.split('_')[-1]
        pub_path = f'{pub_path}/{version}'



        if not os.path.isdir(pub_path):
            os.makedirs(pub_path)

        pub_file = f'{pub_path}/{filename}'
        if os.path.isfile(pub_file):
            self.errorMessage('Pub version Exist!!')
            return 0




        self.mayaCleanup()
        cmds.file(rn=pub_file)
        cmds.file(s=True, f=True)

        self.getAniPub()


        ##############################################
        ####         make assetList.csv          #####
        ##############################################

        ref_list = mel.eval('ls -type reference')
        asset_list = []
        for i in ref_list:
            if not 'shared' in i:         
                if cmds.referenceQuery( i, isLoaded = True ):
                    asset_list.append(i)

        scene_csv = f'{pub_path}/{filename}.csv'
        assets = {}
        if os.path.isfile(csv_path):
            with open(csv_path) as f:
                data = csv.reader(f)
                for asset_type, asset_name in data:

                    if asset_type not in assets:
                        assets[asset_type] = []

                    assets[asset_type].append(asset_name)
        else:
            asset_type.clear()
            asset_name.clear()

        f = open(scene_csv,'w', newline='')
        wr = csv.writer(f)
        for i in asset_list:
            for key in assets.keys():
                for value in assets.get(key):
                    if value.lower() == (i.split('_')[0]).lower():
                        print (key,i)
                        wr.writerow([key,i])
        wr.writerow(['startFrame',startFrame])
        wr.writerow(['endFrame',endFrame])
        f.close()

        #################################################
        #####             BAKE abc cache            #####
        #################################################


                
        if os.path.isfile(scene_csv):
            with open(scene_csv) as f:
                data = csv.reader(f)
                for asset_type, asset_name in data:


                    if not 'Fx' in asset_name:


                        if asset_type == 'character' or asset_type == 'prop':
                            
                            asset_shortName = asset_name.split('_')[0]            
                            print ('asset_shortName = ' + asset_shortName)
                            item = f'{asset_shortName}*:bakeSet'
                            bakeSet =cmds.ls(item, type='objectSet')
                                        
                            if len(bakeSet) == 1:          
                                
                                cmds.select(item)

                                selectedObj = cmds.ls(selection = True, l=True)
                                bakeObj = ' -root '.join(selectedObj)
                                abcName = f'{currentShot}_animation_{asset_type}_{asset_shortName}_{version}.abc'
                                abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{asset_shortName}/{version}/alembic/'
                                if not os.path.isdir(abcPath):
                                        os.makedirs(abcPath)
                                            
                                
                                command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
                                mel.eval(command)
                                        
                            if len(bakeSet) > 1:
                                item = cmds.referenceQuery(asset_name,nodes=True)
                                for i in item:
                                    if 'bakeSet' in i:
                                        print (i)
                                        cmds.select(i)
                                print ('i= '+i)
                                selectedObj = cmds.ls(selection = True, l=True)
                                bakeObj = ' -root '.join(selectedObj)
                                
                                abcName = f'{currentShot}_animation_{asset_type}_{asset_name}_{version}.abc'
                                abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{asset_name}/{version}/alembic/'
                                if not os.path.isdir(abcPath):
                                    os.makedirs(abcPath)
                                
                                command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
                                mel.eval(command)

                            if len(bakeSet) == 0:
                                
                                print(f'{item} Error!!')
                                continue

                    if 'bg' == asset_type:

                        list = []
                        item = asset_name.split('_')[0]

                        atomName = f'{currentShot}_animation_{asset_type}_{item}_{version}.atom'
                        atomPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{item}/{version}/atom/'
                        atomName = '"'+atomPath+atomName+'"'
                        mapfile =  f'{atomPath}/{currentShot}_animation_{asset_type}_{item}_{version}.map'
                        
                        item = cmds.referenceQuery(asset_name,nodes=True,dagPath=True)
                        count = 0
                        for i in item:
                                                                             
                            if cmds.objectType(i) == 'nurbsCurve':
                                count = count + 1
                                
                                list.append(i)

                        if count != 0:
                            if not os.path.isdir(atomPath):
                                os.makedirs(atomPath)
                            list = cmds.listRelatives(list, parent = True)
                            f = open(mapfile, 'w')
                            for i in list:
                                data = '"'+i+'"\n'
                                f.write(data)
                            f.close()
                            cmds.select(list)                            
                            command = f'file -force -options "precision=8;statics=1;baked=1;sdk=0;constraint=0;animLayers=0;selected=selectedOnly;whichRange=2;range={startFrame}:{endFrame};controlPoints=0;useChannelBox=2;options=keys;" -ch 1 -typ "atomExport" -es {atomName};'
                            mel.eval(command)

                    if 'Fx' in asset_name:

                        list = []
                        item = asset_name.split('_')[0]
                        fxitem = asset_name.split(':')[-1]


                        atomName = f'{currentShot}_animation_{item}_{fxitem}_{version}.atom'
                        atomPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_Fx_{item}_{fxitem}/{version}/atom/'
                        atomName = '"'+atomPath+atomName+'"'
                        mapfile =  f'{atomPath}/{currentShot}_animation_{asset_type}_{item}_{version}.map'

                        if not os.path.isdir(atomPath):
                            os.makedirs(atomPath)

                        item = cmds.referenceQuery(asset_name,nodes=True,dagPath=True)

                        for i in item:
                            if cmds.objectType(i) == 'nurbsCurve':
                                list.append(i)

                        list = cmds.listRelatives(list, parent = True)

                        f = open(mapfile, 'w')
                        for i in list:
                            data = '"'+i+'"\n'
                            f.write(data)
                        f.close()

                        cmds.select(list)
                        command = f'file -force -options "precision=8;statics=1;baked=1;sdk=0;constraint=0;animLayers=0;selected=selectedOnly;whichRange=2;range={startFrame}:{endFrame};controlPoints=0;useChannelBox=2;options=keys;" -ch 1 -typ "atomExport" -es {atomName};'
                        mel.eval(command)

                        
        if cmds.objExists('ETC|BAKE'):

            cmds.select('ETC|BAKE')
            selectedObj = cmds.ls(selection = True, l=True)
            bakeObj = ' -root '.join(selectedObj)
            abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_abcETC/{version}/alembic/'
            if not os.path.isdir(abcPath):
                os.makedirs(abcPath)
            abcName = f'{currentShot}_animation_ETC_{version}.abc'
                        
            command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
            mel.eval(command)
        
        if cmds.objExists('BG'):
            cmds.select('BG')
            selectedObj = cmds.ls(selection = True, l=True)
            bakeObj = ' -root '.join(selectedObj)
            abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_abcBG/{version}/alembic/'
            if not os.path.isdir(abcPath):
                os.makedirs(abcPath)
            abcName = f'{currentShot}_animation_BG_{version}.abc'
            
            command = f'AbcExport -j "-frameRange 1 1 -ro -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
            mel.eval(command)

        if cmds.objExists('BGPROP'):
            cmds.select('BGPROP')
            selectedObj = cmds.ls(selection = True, l=True)
            bakeObj = ' -root '.join(selectedObj)
            abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_abcBGPROP/{version}/alembic/'
            if not os.path.isdir(abcPath):
                os.makedirs(abcPath)
            abcName = f'{currentShot}_animation_BGPROP_{version}.abc'
            
            command = f'AbcExport -j "-frameRange 1 1 -ro -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
            mel.eval(command)

        #################################################
        #####             Export Camera             #####
        #################################################
        
        cameras = cmds.ls(type=('camera'), l=True) or []

        camName = [s for s in cameras if '_cam' in s]
        camName = camName[0].split('|')
        camName = camName[-2]

        cmds.select(camName)
        selname = cmds.ls(sl=True)
        camName = selname[0] + '_camExp'
        cmds.duplicate(rr=True, n = camName)
        cmds.setAttr(camName+'.tx', lock=False )
        cmds.setAttr(camName+'.ty', lock=False )
        cmds.setAttr(camName+'.tz', lock=False )
        cmds.setAttr(camName+'.rx', lock=False )
        cmds.setAttr(camName+'.ry', lock=False )
        cmds.setAttr(camName+'.rz', lock=False )
        cmds.setAttr(camName+'.sx', lock=False )
        cmds.setAttr(camName+'.sy', lock=False )
        cmds.setAttr(camName+'.sz', lock=False )
        cmds.parent(camName, world=True)


        cmds.parentConstraint( selname, camName, mo = True )
        cmds.select( camName )


        selShape = (selname[0])+'Shape'
        camShape = (camName)+'Shape'

        cmds.setAttr(camShape + '.cameraAperture', lock=0)
        cmds.connectAttr(selShape + '.cameraAperture', camShape + '.cameraAperture')
        cmds.setAttr(camShape + '.focalLength', lock=0)
        cmds.connectAttr(selShape + '.focalLength', camShape + '.focalLength')
        cmds.setAttr(camShape + '.lensSqueezeRatio', lock=0)
        cmds.connectAttr(selShape + '.lensSqueezeRatio', camShape + '.lensSqueezeRatio')
        cmds.setAttr(camShape + '.fStop', lock=0)
        cmds.connectAttr(selShape + '.fStop', camShape + '.fStop')
        cmds.setAttr(camShape + '.focusDistance', lock=0)
        cmds.connectAttr(selShape + '.focusDistance', camShape + '.focusDistance')
        cmds.setAttr(camShape + '.shutterAngle', lock=0)
        cmds.connectAttr(selShape + '.shutterAngle', camShape + '.shutterAngle')

        start = cmds.playbackOptions(q=1,min=1)
        end = cmds.playbackOptions(q=1,max=1)
        cmds.bakeResults(sm=True, t=(start,end))
        cmds.delete(cn=True)
        cmds.select( camName )

        path = f'{shot_path}/{currentShot}/animation/output/camcache/animation_renderCam/{version}/fbx'
        if not os.path.isdir(path):
            os.makedirs(path)
        path = f'{shot_path}/{currentShot}/animation/output/camcache/animation_renderCam/{version}/fbx/{currentShot}_animation_renderCam_{version}'
        cmds.file (path, force = True, options = 'v = 0', type ='FBX export', exportSelected = True)
        cmds.delete(camName)




        cameras = cmds.ls(type=('camera'), l=True) or []
        camName = [s for s in cameras if '_cam' in s]
        camName = camName[0].split('|')
        camName = camName[-2]


        cmds.select(camName)

        path = f'{shot_path}/{currentShot}/animation/output/camcache/animation_renderCam/{version}/alembic'
        if not os.path.isdir(path):
                os.makedirs(path)
        path = f'{shot_path}/{currentShot}/animation/output/camcache/animation_renderCam/{version}/alembic/{currentShot}_animation_renderCam_{version}.abc'
        
        command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {camName} -file {path}";'
        mel.eval(command)
        
            




    def aniOpenPubBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open the file?'):
            return 0

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.aniPub_list.currentItem().text()
        version = selected_file.split('.')[0]
        version = version.split('_')[-1]

  
        pub_file     = f'{shot_path}/{currentShot}/animation/output/maya/showcase_animation/{version}/{selected_file}'
        print ('pub_file = '+pub_file)
        cmds.file(pub_file, o=True, f=True)


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
            command = f'AbcExport -j "-frameRange 1 1 -ro -stripNamespaces -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {selectGroup[0]} -file {pub_abc_path}";'
            mel.eval(command)

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

        selected_asset = self.asset_name.currentItem().text()

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

                node = cmds.ls(obj)
                print (node)
                if len(node) > 1:
                    for i in node:
                        if selected_asset in i:
                            cmds.select(i)
                else:
                    cmds.select(node[0])
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
        os.startfile(modelPub_dir)


    def openWIPFileBrowser(self):

        wip_dir = self.getSaveDir('work') + '/maya/scenes/increments'
        wip_dir = wip_dir.replace('/', '\\')
        print('wip_dir = '+ wip_dir)
        os.startfile(wip_dir)

    # semi common function
    def openPubFileBrowser(self):

        pub_dir = self.getSaveDir('output') + '/shadegeo/shade_main/'+ self.publish_version.currentItem().text() + '/maya'
        print ('pub_dir : '+pub_dir)
        pub_dir = pub_dir.replace('/', '\\')
        os.startfile(pub_dir)

        
    def closeEvent(self, event):

        self.saveCurrentENV()
        

    def initUI(self):

        # project list
        self.proj_list = QComboBox()
        self.getProjectList()
        self.proj_list.currentIndexChanged.connect(self.getEpisodeList)

        # episode list
        self.episode_list = QListWidget()
        self.episode_list.setMinimumWidth(130)
        self.episode_list.currentItemChanged.connect(self.getAssetType)
        self.episode_list.currentItemChanged.connect(self.getShotList)
        episode_layout = QVBoxLayout()
        episode_layout.addWidget(self.episode_list)
        episode_grp = QGroupBox('Episode')
        episode_grp.setLayout(episode_layout)

        # shot list
        
        self.shot_list = QListWidget()
        self.shot_list.setMinimumWidth(130)
        self.shot_list.currentItemChanged.connect(self.getLayoutWip)
        self.shot_list.currentItemChanged.connect(self.getLayoutPub)
        self.shot_list.currentItemChanged.connect(self.getAniWip)
        self.shot_list.currentItemChanged.connect(self.getAniPub)
        #PlayBlaster_btn = QPushButton('PlayBlaster')
        #PlayBlaster_btn.clicked.connect(self.playblasterBtn)
        shot_layout = QVBoxLayout()
        shot_layout.addWidget(self.shot_list)
        #shot_layout.addWidget(PlayBlaster_btn)
        shot_grp = QGroupBox('Shot List')
        shot_grp.setLayout(shot_layout)
        




        ## layout list ##

        # layout wip
        layoutWipOpen_btn = QPushButton('Open WIP')
        layoutWipSave_btn = QPushButton('Save WIP')
        layoutWipOpen_btn.clicked.connect(self.layoutOpenWIPBtn)
        layoutWipSave_btn.clicked.connect(self.layoutSaveWIPBtn)
        layoutWip_lable = QLabel('Layout Wip')
        self.layoutWip_list = QListWidget()
        self.layoutWip_list.itemDoubleClicked.connect(self.layoutWipOpenFileBrowser)
        layoutWip_layout = QVBoxLayout()
        layoutWip_layout.addWidget(layoutWip_lable)
        layoutWip_layout.addWidget(self.layoutWip_list)
        layoutWip_layout.addWidget(layoutWipOpen_btn)
        layoutWip_layout.addWidget(layoutWipSave_btn)

        # layout pub
        
        layoutPubOpen_btn = QPushButton('Open Pub')
        layoutPubSave_btn = QPushButton('Publish')
        layoutPubOpen_btn.clicked.connect(self.layoutOpenPubBtn)
        layoutPubSave_btn.clicked.connect(self.layoutSavePubBtn)
        layoutPub_lable = QLabel('Layout Pub')
        self.layoutPub_list = QListWidget()
        self.layoutPub_list.itemDoubleClicked.connect(self.layoutPubOpenFileBrowser)
        layoutPub_layout = QVBoxLayout()
        layoutPub_layout.addWidget(layoutPub_lable)
        layoutPub_layout.addWidget(self.layoutPub_list)
        layoutPub_layout.addWidget(layoutPubOpen_btn)
        layoutPub_layout.addWidget(layoutPubSave_btn)

        # layout_list 
        layoutList_layout  = QHBoxLayout()
        layoutList_layout.addLayout(layoutWip_layout)
        layoutList_layout.addLayout(layoutPub_layout)
        layoutList_grp = QGroupBox('Layout List')
        layoutList_grp.setLayout(layoutList_layout)


        ## animation list ##

        # ani wip
        aniWipOpen_btn = QPushButton('Open WIP')
        aniWipSave_btn = QPushButton('Save WIP')
        aniWipOpen_btn.clicked.connect(self.aniOpenWIPBtn)
        aniWipSave_btn.clicked.connect(self.aniSaveWIPBtn)
        aniWip_lable = QLabel('Ani Wip')
        self.aniWip_list = QListWidget()
        self.aniWip_list.itemDoubleClicked.connect(self.aniWipOpenFileBrowser)
        aniWip_layout = QVBoxLayout()
        aniWip_layout.addWidget(aniWip_lable)
        aniWip_layout.addWidget(self.aniWip_list)
        aniWip_layout.addWidget(aniWipOpen_btn)
        aniWip_layout.addWidget(aniWipSave_btn)        
        # ani pub
        
        aniPubOpen_btn = QPushButton('Open Pub')
        aniPubSave_btn = QPushButton('Publish')
        aniPubOpen_btn.clicked.connect(self.aniOpenPubBtn)
        aniPubSave_btn.clicked.connect(self.aniSavePubBtn)
        aniPub_lable = QLabel('Ani Pub')
        self.aniPub_list = QListWidget()
        self.aniPub_list.itemDoubleClicked.connect(self.aniPubOpenFileBrowser)
        aniPub_layout = QVBoxLayout()
        aniPub_layout.addWidget(aniPub_lable)
        aniPub_layout.addWidget(self.aniPub_list)
        aniPub_layout.addWidget(aniPubOpen_btn)
        aniPub_layout.addWidget(aniPubSave_btn)
        # ani_list 
        aniList_layout  = QHBoxLayout()
        aniList_layout.addLayout(aniWip_layout)
        aniList_layout.addLayout(aniPub_layout)
        aniList_grp = QGroupBox('Animation List')
        aniList_grp.setLayout(aniList_layout)




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
        middle_ver_label = QLabel('Ver')
        self.rig_pub_ver = QListWidget()
        self.rig_pub_ver.setMinimumWidth(40)
        self.rig_pub_ver.currentItemChanged.connect(self.getRigPub)
        middle_ver_layout = QVBoxLayout()
        middle_ver_layout.addWidget(middle_ver_label)
        middle_ver_layout.addWidget(self.rig_pub_ver)

        # asset pub RIG
        pub_rig_label = QLabel('pub RIG')
        self.pub_rig = QListWidget()
        self.pub_rig.setMinimumWidth(160)
        self.pub_rig.itemDoubleClicked.connect(self.openModelPubFileBrowser)
        pub_rig_layout = QVBoxLayout()
        pub_rig_layout.addWidget(pub_rig_label)
        pub_rig_layout.addWidget(self.pub_rig)

        # asset reference import
        Asset_ref_btn = QPushButton('Asset Ref import')
        Asset_ref_btn.clicked.connect(self.assetRefBtn)

        # asset replace
        Asset_rep_btn = QPushButton('Asset replace')
        Asset_rep_btn.clicked.connect(self.assetRepBtn)
       
        #
        middle_layout = QHBoxLayout()
        middle_layout.addLayout(middle_name_layout)
        middle_layout.addLayout(middle_ver_layout)
        middle_layout.addLayout(pub_rig_layout)
        middle_name_grp = QGroupBox('Rig')
        middle_name_grp.setLayout(middle_layout)
        #
        asset_ref_layout = QVBoxLayout()
        asset_ref_layout.addWidget(middle_name_grp)
        asset_ref_layout.addWidget(Asset_ref_btn)
        asset_ref_layout.addWidget(Asset_rep_btn)



        # version
        

        # wip version list
        self.save_wip_version = QListWidget()
        self.save_wip_version.setMinimumWidth(80)
        self.save_wip_version.itemDoubleClicked.connect(self.openWIPFileBrowser)
        save_wip_version_layout = QVBoxLayout()
        save_wip_version_layout.addWidget(self.save_wip_version)
        save_wip_version_grp = QGroupBox('WIP Version')
        save_wip_version_grp.setLayout(save_wip_version_layout)
        # publish version list
        self.publish_version = QListWidget()
        self.publish_version.setMinimumWidth(80)
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
        column2_layout_grp = QGroupBox('Look Dev')
        column2_layout_grp.setLayout(column2_layout)

        # column1 layout
        column1_layout = QVBoxLayout()
        #
        column1_row1_layout = QHBoxLayout()
        column1_row1_layout.addWidget(episode_grp)
        column1_row1_layout.addWidget(asset_type_grp)
        column1_row1_layout.addWidget(asset_name_grp)
        column1_row1_layout.addLayout(asset_ref_layout)
        column1_row1_layout.addWidget(column2_layout_grp) # lookdevUI      
        #
        column1_layout.addWidget(self.proj_list)
        column1_layout.addLayout(column1_row1_layout)



        # column3 layout
        column3_layout = QHBoxLayout()
        column3_layout.addWidget(shot_grp)
        column3_layout.addWidget(layoutList_grp)
        column3_layout.addWidget(aniList_grp)




        # main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(column1_layout)
        main_layout.addLayout(column3_layout)
        self.setLayout(main_layout)

        self.setWindowTitle(f'AniTool [version : {toolVersion} ]')
        self.show()

        cmds.window(self.window_name, e=True, w=835)



AniToolUI()