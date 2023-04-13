
# maya 2022
# mayapy 3.7.7
toolVersion = 'pipline_19.py'
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

import os, shutil, stat, datetime
#import sys
import csv
import re
import json

cmds.loadPlugin( 'AbcExport.mll' )
cmds.loadPlugin( 'AbcImport.mll' )
cmds.loadPlugin( 'atomImportExport.mll' )
cmds.loadPlugin( 'fbxmaya.mll' )
cmds.loadPlugin( 'gameFbxExporter.mll' )
cmds.loadPlugin( 'Type.mll' )
cmds.loadPlugin( 'MayaScanner.py' )
cmds.loadPlugin( 'MayaScannerCB.py' )
# PROJ_DRIVE = os.getenv('PROJ_DRIVE')

PROJ_DRIVE = r'P:'

def getMayaMainWindow():

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

    return mayaMainWindow

class piplineToolUI(QWidget):

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




    ########################## SET PROJETC  #######################

    def setCamera(self, prj):

        if prj == 'TGR':
            
            cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
            cmds.setAttr("defaultResolution.aspectLock", 0)
            cmds.setAttr("defaultResolution.width", 1920)
            cmds.setAttr("defaultResolution.height", 1200)
            cmds.setAttr("defaultResolution.deviceAspectRatio", 1.777)
            cmds.setAttr("defaultResolution.pixelAspect", 1)
            cmds.setAttr("defaultResolution.aspectLock", 1)

        if prj == 'projects':
            
            cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")
            cmds.setAttr("defaultResolution.aspectLock", 0)
            cmds.setAttr("defaultResolution.width", 2560)
            cmds.setAttr("defaultResolution.height", 1200)
            cmds.setAttr("defaultResolution.deviceAspectRatio", 2.133)
            cmds.setAttr("defaultResolution.pixelAspect", 1)
            cmds.setAttr("defaultResolution.aspectLock", 1)


    def getAssetPath(self, prj):

        proj = self.proj_list.currentText()
        current_ep = self.episode_list.currentItem().text()

        if prj == 'TGR':
            asset_path = f'{PROJ_DRIVE}/{proj}/assets/3D'

        if prj == 'projects':
            asset_path = f'{PROJ_DRIVE}/{proj}/{current_ep}/assets/3D'

        if prj == 'SBB':
            asset_path = f'{PROJ_DRIVE}/{proj}/{current_ep}/assets/3D'

        if prj == 'DEFT':
            asset_path = f'{PROJ_DRIVE}/{proj}/{current_ep}/assets/3D'

        return asset_path


    def getEpiPath(self, prj):

        proj = self.proj_list.currentText()

        if prj == 'TGR':
            EPipath = f'{PROJ_DRIVE}/{proj}/sequences'

        if prj == 'projects':
            EPipath = f'{PROJ_DRIVE}/{proj}'

        if prj == 'SBB':
            EPipath = f'{PROJ_DRIVE}/{proj}'

        if prj == 'DEFT':
            EPipath = f'{PROJ_DRIVE}/{proj}'

        return EPipath


    def getShotPath(self, prj):

        current_ep   = self.episode_list.currentItem().text()
        proj = self.proj_list.currentText()

        if prj == 'TGR':
            shotPath = f'{PROJ_DRIVE}/{proj}/sequences/{current_ep}'

        if prj == 'projects':
            shotPath = f'{PROJ_DRIVE}/{proj}/{current_ep}/sequences'
        
        if prj == 'SBB':
            shotPath = f'{PROJ_DRIVE}/{proj}/{current_ep}/sequences'
        
        if prj == 'DEFT':
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
        msgBox.setStyleSheet("color: rgb(246, 118, 78);")
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

        # delete China Virus

        script = cmds.ls(type='script')

        for i in script:
            if 'breed_gene' in i or 'vaccine_gene' in i:   
                cmds.delete(i)

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
                ver = 'a' + cmds.referenceQuery( i,filename=True, shortName=True ).split('{')[-1].split('}')[0]    
            
            if not ns == ':' and not name+ver == ns.split(':')[-1]:
                mel.eval(f'file -e -namespace "{name}{ver}" -referenceNode "{i}" "{cmds.referenceQuery( i,filename=True)}";')
                cmds.lockNode( i, lock=False)
                cmds.rename( i, name+'RN' )
            if not ns == ':' and name+ver == ns.split(':')[-1]:
                mel.eval(f'file -referenceNode "{i}" "{pathName}";')
                cmds.lockNode( i, lock=False)
                cmds.rename( i, name+'RN' )

        list.clear()
        ref_list.clear()

        
    

        
        ########################    END    ##########################

    def saveCurrentENV(self):

        proj         =  self.proj_list.currentText()
        ep           =  self.episode_list.currentRow()
        asset_type   =  self.asset_type.currentRow()
        asset_name   =  self.asset_name.currentRow()
        shot_name    =  self.shot_list.currentRow()        
        LookDevWipVer = self.LookDevWip_version.currentRow()
        LookDevPubVer = self.LookDevPub_version.currentRow()
        rigMiddle_name  =  self.rigMiddle_list.currentRow()
        rigWipVer = self.rig_Wip_ver.currentRow()
        wipRig = self.wip_rig.currentRow()
        rigPubVer  =  self.rig_Pub_ver.currentRow()
        pubRig      =  self.pub_rig.currentRow()
        layoutWipVer =  self.layoutWip_list.currentRow()
        layoutPubVer =  self.layoutPub_list.currentRow()
        aniWipVer    =  self.aniWip_list.currentRow()
        aniPubVer    =  self.aniPub_list.currentRow()
        lightWipVer    =  self.lightWip_list.currentRow()
        lightPubVer    =  self.lightPub_list.currentRow()

        env_docs = {
                    'project': proj,          'episode': ep,
                    'asset_type': asset_type, 'asset_name': asset_name,
                    'shot_name': shot_name,                    
                    'LookDevWipVer': LookDevWipVer, 'LookDevPubVer': LookDevPubVer,
                    'rigMiddle_name': rigMiddle_name, 'rigPubVer': rigPubVer, 'pubRig' : pubRig, 'rigWipVer': rigWipVer, 'wipRig': wipRig,
                    'layoutWipVer':layoutWipVer, 'layoutPubVer':layoutPubVer,
                    'aniWipVer':aniWipVer, 'aniPubVer':aniPubVer,
                    'lightWipVer':lightWipVer, 'lightPubVer':lightPubVer,
                    }

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_Tool.json'

        with open(env_path, 'w') as f:
            data = json.dumps(env_docs, indent=4, separators=(',',':'), sort_keys=True)
            f.write(data)


    def openCurrentENV(self):

        tmp_dir = os.getenv('TMP').replace('\\', '/')
        env_path = f'{tmp_dir}/pipeline_Tool.json'

        with open(env_path) as f:
            env_docs = json.load(f)

        self.proj_list.setCurrentText(env_docs['project'])
        self.episode_list.setCurrentRow(env_docs['episode'])
        self.asset_type.setCurrentRow(env_docs['asset_type'])
        self.asset_name.setCurrentRow(env_docs['asset_name'])
        self.LookDevWip_version.setCurrentRow(env_docs['LookDevWipVer'])
        self.LookDevPub_version.setCurrentRow(env_docs['LookDevPubVer'])
        self.shot_list.setCurrentRow(env_docs['shot_name'])
        self.rigMiddle_list.setCurrentRow(env_docs['rigMiddle_name'])
        self.rig_Wip_ver.setCurrentRow(env_docs['rigWipVer'])
        self.wip_rig.setCurrentRow(env_docs['wipRig'])
        self.rig_Pub_ver.setCurrentRow(env_docs['rigPubVer'])
        self.pub_rig.setCurrentRow(env_docs['pubRig'])
        self.layoutWip_list.setCurrentRow(env_docs['layoutWipVer'])
        self.layoutPub_list.setCurrentRow(env_docs['layoutPubVer'])
        self.aniWip_list.setCurrentRow(env_docs['aniWipVer'])
        self.aniPub_list.setCurrentRow(env_docs['aniPubVer'])
        self.lightWip_list.setCurrentRow(env_docs['lightWipVer'])
        self.lightPub_list.setCurrentRow(env_docs['lightPubVer'])

    def readAssetCSV(self):
        ###########################
        # asset_list.csv AutoCreat#
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
        # asset_list.csv Read     #
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

    def getRigMiddleName(self):

        department_dir = self.getDepartmentDir('rig/output/rig')
        if not os.path.isdir(department_dir):
            os.makedirs(department_dir)
        self.rigMiddle_list.clear()
        if os.path.isdir(department_dir):
            middle_names = os.listdir(department_dir)
            if 'rig_main' in middle_names:
                middle_names.pop(middle_names.index('rig_main'))
                self.rigMiddle_list.addItem('rig_main')
            for middle_name in sorted(middle_names):
                self.rigMiddle_list.addItem(middle_name)
        else:
            self.rigMiddle_list.addItem('rig_main')

        self.getLookDevVersion()


    def getRigWipName(self):
        self.wip_rig.clear()

        proj = self.proj_list.currentText()
        asset_path = self.getAssetPath(proj)
        asset_type = self.asset_type.currentItem().text()
        asset_name = self.asset_name.currentItem().text()
        middle_name = self.rigMiddle_list.currentItem().text()
        rig_pubVer = self.rig_Wip_ver.currentItem().text()

        rig_wipPath = f'{asset_path}/{asset_type}/{asset_name}/rig/work/rig/{middle_name}/{rig_pubVer}/maya/'
        
        
        if not os.path.isdir(rig_wipPath):
            os.makedirs(rig_wipPath)

        print('rig_wipPath:'+rig_wipPath)

       
        for file_name in os.listdir(rig_wipPath):
            if os.path.splitext(file_name)[1] == '.mb':
                self.wip_rig.addItem(file_name)

    
    def getRigPubName(self):

        self.pub_rig.clear()

        proj = self.proj_list.currentText()
        asset_path = self.getAssetPath(proj)
        asset_type = self.asset_type.currentItem().text()
        asset_name = self.asset_name.currentItem().text()
        middle_name = self.rigMiddle_list.currentItem().text()
        rig_pubVer = self.rig_Pub_ver.currentItem().text()

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
            model, rig, shade, texture 
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

        if not os.path.isdir(shot_path):
            os.makedirs(shot_path)

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




    def getlightWip(self):

        self.lightWip_list.clear()

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        print(f'currentShot = {currentShot}')

        lightWip_path = f'{shot_path}/{currentShot}/lit/work/maya/scene'

        if not os.path.isdir(lightWip_path):
            os.makedirs(lightWip_path)

        for file_name in sorted(os.listdir(lightWip_path)):
            if os.path.isfile(f'{lightWip_path}/{file_name}'):
                if os.path.splitext(file_name)[1] == '.mb':
                    self.lightWip_list.addItem(file_name)
        


    def getlightPub(self):

        self.lightPub_list.clear()

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
            
        lightPub_path = f'{shot_path}/{currentShot}/lit/output/exr'
            
        if not os.path.isdir(lightPub_path):
            os.makedirs(lightPub_path)

        print('lightPub_path:'+lightPub_path)
        for version in sorted(os.listdir(lightPub_path)):
            for file_name in os.listdir(f'{lightPub_path}/{version}/workfile'):
                if os.path.isfile(f'{lightPub_path}/{version}/workfile/{file_name}'):
                    if os.path.splitext(file_name)[1] == '.mb':
                        self.lightPub_list.addItem(file_name)



    # semi common
    def getLookDevSaveDir(self, save_type=None):

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


    def getLookDevVersion(self):
        # lookdev VersionList
        self.LookDevWip_version.clear()
        wip_dir = self.getLookDevSaveDir('work') + '/maya/scenes/increments'
        if os.path.isdir(wip_dir):
            for wip_file in sorted(os.listdir(wip_dir)):
                re_match = re.search('_(v\d{3}).mb$', wip_file)
                if re_match:
                    self.LookDevWip_version.addItem(re_match.group(1))

        self.LookDevPub_version.clear()
        pub_dir = self.getLookDevSaveDir('output') + '/shadegeo/shade_main'
        if os.path.isdir(pub_dir):
            for pub_file in sorted(os.listdir(pub_dir)):
                pub_file = pub_dir+'/'+ pub_file+'/maya'
                pub_file = os.listdir(pub_file)
                for i in pub_file:
                    re_match = re.search('_(v\d{3}).mb$', i)
                    if re_match:
                        self.LookDevPub_version.addItem(re_match.group(1))

    # semi common
    def getLookDevSaveFile(self, save_version=None, save_ext=None):


        asset_name = self.asset_name.currentItem().text()

        save_file = f'{asset_name}_shade_main'
        save_file = f'{save_file}_{save_version}.{save_ext}'

        return save_file

    ###################
    # common function #
    ###################

    def getRigWipVersion(self):
        
        self.rig_Wip_ver.clear()

        Wip_dir = self.getRigWipDir()
        if not os.path.isdir(Wip_dir):
            os.makedirs(Wip_dir)
        #  Rig Wip Path
        print('Wip_dir = ' + Wip_dir)

        if os.path.isdir(Wip_dir):
            for Wip_file in sorted(os.listdir(Wip_dir)):
                Wip_file = Wip_dir+'/'+ Wip_file+'/maya/'
                try:
                    Wip_file = os.listdir(Wip_file)
                except:
                    continue
                Wip_file = [file for file in Wip_file if file.endswith(".mb") or file.endswith(".ma")]
                re_match = re.search('_(v\d{3})', Wip_file[0])
                if re_match:
                    self.rig_Wip_ver.addItem(re_match.group(1))


    def getRigPubVersion(self):

        self.rig_Pub_ver.clear()

        pub_dir = self.getRigPubDir()
        if not os.path.isdir(pub_dir):
            os.makedirs(pub_dir)
        #  Rig pub Path
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
                    self.rig_Pub_ver.addItem(re_match.group(1))

    
    def getRigPubDir(self):

        """
        depart:
            model, texture, shade, rig
        """

        department_dir = self.getDepartmentDir('rig')

        middle_name = self.rigMiddle_list.currentItem().text()
        
        save_dir = f'{department_dir}/output/rig/{middle_name}'
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        print ('save_dir = ' + save_dir)
        return save_dir

    def getRigWipDir(self):

        """
        depart:
            model, texture, shade, rig
        """

        department_dir = self.getDepartmentDir('rig')

        middle_name = self.rigMiddle_list.currentItem().text()
        
        save_dir = f'{department_dir}/work/rig/{middle_name}'
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)

        print ('save_dir = ' + save_dir)
        return save_dir
    
    def getRigSaveDir(self, save_type=None):

        """
        save_type:
            work, output
        """
        
        department_dir = self.getDepartmentDir('rig')        
        save_dir = f'{department_dir}/{save_type}'

        return save_dir
    
    def getRigPubFile(self, save_version=None):


        asset_name = self.asset_name.currentItem().text()
        middle_name = self.rigMiddle_list.currentItem().text()

        save_file = f'{asset_name}_{middle_name}'
        save_file = f'{save_file}_{save_version}'
        print ('save_file = '+save_file)
        return save_file

    def assetRefBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0

        asset_type = self.asset_type.currentItem().text()
        selected_version = self.rig_Pub_ver.currentItem().text()
        pub_file = self.pub_rig.currentItem().text()
        pub_dir = self.getRigPubDir() + '/'+ selected_version + '/maya'
        
        print ('pub_file = '+pub_file)
        print ('pub_dir = '+pub_dir)
        pub_path = f'{pub_dir}/{pub_file}'
        namespace = f'{pub_file.split(".")[0]}'
        print (pub_path)

        before = set(cmds.ls(type='transform', long =True))
        cmds.file(pub_path, ignoreVersion = True, r=True, gl=True, mnc=False, ns=namespace)
        
        after = set(cmds.ls(type='transform', long =True))
        imported = after - before

        print ('recentItem = ' + str(imported))

        item =[]
        for i in imported:
            if i.count('|') == 1:
                item.append(i)

        print (item)
        if asset_type == 'character':
            if not cmds.objExists('CH'):
                cmds.group(em=True, name='CH' )
            cmds.parent(item, 'CH')

        if asset_type == 'bg':
            if not cmds.objExists('BG'):
                cmds.group(em=True, name='BG' )
            cmds.parent(item, 'BG')
        
        if asset_type == 'prop':
            if not cmds.objExists('PROP'):
                cmds.group(em=True, name='PROP' )
            cmds.parent(item, 'PROP')
        
        if asset_type == 'fx':
            if not cmds.objExists('FX'):
                cmds.group(em=True, name='FX' )
            cmds.parent(item, 'FX')
        item =[]

        self.rename_refNode()
        self.rename_refNode()




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

        selVer     = self.rig_Pub_ver.currentItem().text()
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
            self.rename_refNode()
            self.rename_refNode()
        else:
            self.errorMessage('Select Target ref Node!!')
            return 0
    

    def openLookDevWipBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0

        wip_dir = self.getLookDevSaveDir('work') + '/maya/scenes/increments'
        selected_version = self.LookDevWip_version.currentItem().text()
        wip_file = self.getLookDevSaveFile(selected_version, 'mb')
        wip_path = f'{wip_dir}/{wip_file}'

        cmds.file(wip_path, o=True, f=True)
        
    def openLookDevPubBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0

        
        selected_version = self.LookDevPub_version.currentItem().text()
        pub_dir = self.getLookDevSaveDir('output') + '/shadegeo/shade_main/' + selected_version + '/maya/'
        pub_file = self.getLookDevSaveFile(selected_version, 'mb')
        pub_path = f'{pub_dir}/{pub_file}'

        cmds.file(pub_path, o=True, f=True)

    def layoutOpenWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0
        
        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.layoutWip_list.currentItem().text()
        wip_file     = f'{shot_path}/{currentShot}/layout/work/maya/scene/{selected_file}'
        print ('wip_file = '+wip_file)
        cmds.file(wip_file, o=True, f=True)
        self.rename_refNode()
        self.rename_refNode()


    def layoutSaveWIPBtn(self):

        self.rename_refNode()
        self.rename_refNode()
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

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
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
        self.rename_refNode()
        self.rename_refNode()

    def layoutSavePubBtn(self):

        self.rename_refNode()       
        self.rename_refNode() 
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

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.aniWip_list.currentItem().text()
        ani_file     = f'{shot_path}/{currentShot}/animation/work/maya/scene/{selected_file}'
        print ('ani_file = '+ ani_file)
        cmds.file(ani_file, o=True, f=True)
        self.rename_refNode()
        self.rename_refNode()

    def aniSaveWIPBtn(self):

        self.rename_refNode()
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
        if not cmds.ogs(pause=True, query=True):
            cmds.ogs(pause = True)
        
        try:
            mel.eval('animLayer -edit -lock 0 BaseAnimation')
        except:
            print('no anim layer')

        self.rename_refNode()
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
                            list = []
                            refList = mel.eval('ls -type reference')

                            for i in refList:
                                if asset_shortName in i and not 'Fx' in i and not 'shared' in i:
                                    list.append(i)


                            if len(list) == 1:
                                refNode = cmds.referenceQuery( asset_name,nodes=True )
                                print(refNode)
                                for i in refNode:
                                    if 'bakeSet' in i:
                                        cmds.select(i)

                                selectedObj = cmds.ls(selection = True, l=True)
                                bakeObj = ' -root '.join(selectedObj)
                                abcName = f'{currentShot}_animation_{asset_type}_{asset_shortName}_{version}.abc'
                                abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{asset_shortName}/{version}/alembic/'
                                if not os.path.isdir(abcPath):
                                        os.makedirs(abcPath)
                                            
                                
                                command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
                                mel.eval(command)
                                        
                            if len(list) > 1:
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
                                
                                command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
                                mel.eval(command)

                            if len(list) == 0:
                                
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
                                
                                list.append(cmds.ls(i, long=True)[0])

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
                        
            command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -ro -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
            
            mel.eval(command)
        
        if cmds.objExists('BG'):
            cmds.select('BG')
            selectedObj = cmds.ls(selection = True, l=True)
            bakeObj = ' -root '.join(selectedObj)
            abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_abcBG/{version}/alembic/'
            if not os.path.isdir(abcPath):
                os.makedirs(abcPath)
            abcName = f'{currentShot}_animation_BG_{version}.abc'
            
            command = f'AbcExport -j "-frameRange 1 1 -ro -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
            mel.eval(command)

        if cmds.objExists('BGPROP'):
            cmds.select('BGPROP')
            selectedObj = cmds.ls(selection = True, l=True)
            bakeObj = ' -root '.join(selectedObj)
            abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_abcBGPROP/{version}/alembic/'
            if not os.path.isdir(abcPath):
                os.makedirs(abcPath)
            abcName = f'{currentShot}_animation_BGPROP_{version}.abc'
            
            command = f'AbcExport -j "-frameRange 1 1 -ro -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {bakeObj} -file {abcPath}{abcName}";'
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
        
        command = f'AbcExport -j "-frameRange {startFrame} {endFrame} -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {camName} -file {path}";'
        
        mel.eval(command)

        if cmds.ogs(pause=True, query=True):
            cmds.ogs(pause = True)
        self.confirmMessage('Publishing is completed!!')





    def aniOpenPubBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
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
        self.rename_refNode()
        self.rename_refNode()

    def lightOpenWIPBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.lightWip_list.currentItem().text()
        light_file     = f'{shot_path}/{currentShot}/lit/work/maya/scene/{selected_file}'
        print ('light_file = '+ light_file)
        cmds.file(light_file, o=True, f=True)

    def lightSaveWIPBtn(self):

        
        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        wip_path = f'{shot_path}/{currentShot}/lit/work/maya/scene'
        file_list = os.listdir(wip_path)
        mb_list=[file for file in file_list if file.endswith('.mb')]

        if len(mb_list) == 0:
            filename = f'{currentShot}_lit_v001'
        else :
            list = []
            for i in mb_list:    
                print(i)
                if f'{currentShot}_lit_v' in i:
                    list.append(i)
            mb_list = list
            version = mb_list[-1]
            pattern = '_v([0-9]+)'
            version = 'v'+str(int(re.search(pattern, version).group(1))+1).zfill(3)
            filename = currentShot + '_lit_'
            filename = filename + version

        wip_path = f'{wip_path}/{filename}'

        print ('wip_path : '+wip_path)
        self.mayaCleanup()
        cmds.file(rn=wip_path)
        cmds.file(s=True, f=True)

        self.getlightWip()

    def lightWipOpenFileBrowser(self):

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()

        wip_file     = f'{shot_path}/{currentShot}/lit/work/maya/scene'
        os.startfile(wip_file)

    def lightOpenPubBtn(self):
        
        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.lightPub_list.currentItem().text()
        version = selected_file.split('.')[0]
        version = version.split('_')[-1]

        pub_file = f'{shot_path}/{currentShot}/lit/output/exr/{selected_file.split(".")[0]}/workfile/{selected_file}'
        print ('pub_file = '+pub_file)
        cmds.file(pub_file, o=True, f=True)


    def lightSavePubBtn(self):

        
        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        raw_name, extension = os.path.splitext(filename)
        pattern = '_v([0-9]+)'
        version = 'v'+str(re.search(pattern, raw_name).group(1))
        
                
        filename = f'{currentShot}_lit_'
        filename = filename + version

        pub_path = f'{shot_path}/{currentShot}/lit/output/exr/{filename}/workfile/'

        if not os.path.isdir(pub_path):
            os.makedirs(pub_path)
        
        pub_file = f'{pub_path}/{filename}'

        if os.path.isfile(pub_file+'.mb'):

            self.errorMessage('!! Pub version does already Exist !!')
            return 0
        
        self.mayaCleanup()
        cmds.file(rn=pub_file)
        cmds.file(s=True, f=True)

        self.getlightPub()



    def lightCollectBtn(self):

        try:
            filename = self.aniPub_list.currentItem().text()
        except:
            self.errorMessage(f'!! Select Ani Pub !!')
            return 0
        
        if QMessageBox.No == self.confirmMessage('Do you want to Collect New Scene?'):
            return 0
        
        cmds.file(new=True, f=True)
        proj = self.proj_list.currentText()
        asset_path = self.getAssetPath(proj)
        shot_path = self.getShotPath(proj)
        
        currentShot  = filename.split('_animation')[0]
        version = (filename.split('.')[0]).split('_')[-1]
        
        pub_path = f'{shot_path}/{currentShot}/animation/output/maya/showcase_animation/{version}'
        scene_csv = f'{pub_path}/{filename}.csv'

        if not os.path.isfile(scene_csv):
            self.errorMessage(f'!! {scene_csv} does Not Exist !!')
            return 0

        self.setCamera(proj)
        
        camPath = f'{shot_path}/{currentShot}/animation/output/camcache/animation_renderCam/{version}/alembic'
        if os.path.isdir(camPath) and os.listdir(camPath):
            file_list = os.listdir(camPath)
            camFile = [s for s in file_list if 'renderCam' in s]
        else:            
            self.errorMessage('!! there is No camera !!')
            return 0
           


        if not cmds.objExists('CAM'):
            cmds.group(em=True, name='CAM' )
        command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|CAM" "{camPath}/{camFile[0]}";'
        print( 'cam command = '+ command)
        mel.eval(command)



        with open(scene_csv) as f:
            data = csv.reader(f)
            for asset_type, asset_name in data:
                if not 'Fx' in asset_name:
                    if asset_type == 'character' or asset_type == 'prop':
                        assetNumber=0
                        groupName = asset_name.split('_')[0]
                        with open(scene_csv) as f:
                            data = csv.reader(f)
                            for count_type, count_name in data:
                                if groupName in count_name and 'Fx' not in count_name :
                                    assetNumber =assetNumber+ 1


                        
                        print ('groupName = '+' '+asset_type+' '+groupName)
                        print ('assetNumber = '+ str(assetNumber))
                        if assetNumber == 1 :

                            if asset_type == 'character':
                                if not cmds.objExists('CH'):
                                    cmds.group(em=True, name='CH' )
                                cmds.group(em=True, parent='CH', name=groupName )
                                abcName = f'{currentShot}_animation_{asset_type}_{groupName}_{version}.abc'
                                abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{groupName}/{version}/alembic/'
                                command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|CH|{groupName}" "{abcPath}{abcName}";'
                                mel.eval(command)

                            if asset_type == 'prop':
                                if not cmds.objExists('PROP'):
                                    cmds.group(em=True, name='PROP' )
                                cmds.group(em=True, parent='PROP', name=groupName )
                                abcName = f'{currentShot}_animation_{asset_type}_{groupName}_{version}.abc'
                                abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{groupName}/{version}/alembic/'
                                command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|PROP|{groupName}" "{abcPath}{abcName}";'
                                mel.eval(command)

                        if assetNumber > 1 :

                            if asset_type == 'character':
                                if not cmds.objExists('CH'):
                                    cmds.group(em=True, name='CH' )
                                cmds.group(em=True, parent='CH', name=asset_name )


                                abcName = f'{currentShot}_animation_{asset_type}_{asset_name}_{version}.abc'
                                abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{asset_name}/{version}/alembic/'
                                command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|CH|{asset_name}" "{abcPath}{abcName}";'
                                print ('command = '+ command)
                                mel.eval(command)
                            
                            if asset_type == 'prop':
                                if not cmds.objExists('PROP'):
                                    cmds.group(em=True, name='PROP' )
                                cmds.group(em=True, parent='PROP', name=asset_name )

                                
                                abcName = f'{currentShot}_animation_{asset_type}_{asset_name}_{version}.abc'
                                abcPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{asset_name}/{version}/alembic/'
                                print('abcName = '+asset_name)
                                print('abcName = '+abcName)
                                print('abcPathe = '+abcPath)
                                command = f'AbcImport -mode import -fitTimeRange -setToStartFrame -reparent "|PROP|{asset_name}" "{abcPath}{abcName}";'
                                mel.eval(command)
                if 'bg' == asset_type:
                    list = []
                    item = asset_name.split('_')[0]

                    atomName = f'{currentShot}_animation_{asset_type}_{item}_{version}.atom'
                    atomPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_{asset_type}_{item}/{version}/atom'
                    atomName = '"'+atomPath + '/' + atomName+'"'
                    mapfile =  f'{atomPath}/{currentShot}_animation_{asset_type}_{item}_{version}.map'


                    assetPath = f'{asset_path}/{asset_type}/{item}/rig/output/rig/rig_main'
                    assetVer = [ name for name in os.listdir(assetPath) if os.path.isdir(os.path.join(assetPath, name)) ][-1]
                    assetFile = f'{item}_rig_main_{assetVer}'
                    cmds.file(f'{assetPath}/{assetVer}/maya/{assetFile}.mb', ignoreVersion = True, r=True, gl=True, mnc=False, ns=assetFile)
                    
                    ref_list = mel.eval('ls -type reference')

                    for i in ref_list:
                        if assetFile in i:
                            refNode = i

                    refMember = cmds.referenceQuery(refNode,nodes=True,dagPath=True)
                    for i in refMember:
                        if cmds.objectType(i) == 'nurbsCurve':
                            list.append(i)
                    list = cmds.listRelatives(list, parent = True)
                    print ('list = ' + str(list))

                    if list:
                        with open(mapfile , 'r') as f:
                            line = f.readlines()
                        print (line)

                        with open(mapfile , 'w') as f:
                            for i in line:
                                for o in list:
                                    if o.split(':')[-1] in i:
                                        data = (i.split('\n')[0]).split(' ')[0] + ' ' + '"'+ o + '"' + '\n'
                                        f.write(data)
                        f.close()
                        cmds.select(list)

                        command = f'file -import -type "atomImport" -ra true -options ";;targetTime=3;option=scaleReplace;match=mapFile;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile={mapfile};" {atomName};'
                        mel.eval(command)

                    topNode = cmds.ls(assemblies=True)
                    for i in topNode:
                        if refNode.split('RN')[0] in i:
                            bgGrp = i
                    print(bgGrp)
                    if not cmds.objExists('BG'):
                        cmds.group(em=True, name='BG' )
                    cmds.parent( bgGrp , 'BG' )


                if 'Fx' in asset_name:
                    list = []
                    item = asset_name.split('_')[0]
                    fxitem = asset_name.split(':')[-1]


                    atomName = f'{currentShot}_animation_{item}_{fxitem}_{version}.atom'
                    atomPath = f'{shot_path}/{currentShot}/animation/output/animcache/animation_Fx_{item}_{fxitem}/{version}/atom/'
                    atomName = '"'+atomPath+atomName+'"'
                    mapfile =  f'{atomPath}/{currentShot}_animation_{asset_type}_{item}_{version}.map'

                    assetPath = f'{asset_path}/fx/{fxitem.split("_")[0]}/rig/output/rig/rig_main'
                    assetVer = [ name for name in os.listdir(assetPath) if os.path.isdir(os.path.join(assetPath, name)) ][-1]
                    assetFile = f'{fxitem.split("RN")[0][:-5]}_{assetVer}'
                    cmds.file(f'{assetPath}/{assetVer}/maya/{assetFile}.mb', ignoreVersion = True, r=True, gl=True, mnc=False, ns=assetFile)


                    ref_list = mel.eval('ls -type reference')

                    for i in ref_list:
                        if assetFile in i:
                            refNode = i

                    refMember = cmds.referenceQuery(refNode,nodes=True,dagPath=True)

                    for i in refMember:
                        if cmds.objectType(i) == 'nurbsCurve':
                            list.append(i)
                    list = cmds.listRelatives(list, parent = True)
                    print ('list = ' + str(list))

                    with open(mapfile , 'r') as f:
                        line = f.readlines()
                    print (line)

                    with open(mapfile , 'w') as f:
                        for i in line:
                            for o in list:
                                if o.split(':')[-1] in i:
                                    data = (i.split('\n')[0]).split(' ')[0] + ' ' + '"'+ o + '"' + '\n'
                                    f.write(data)
                    f.close()

                    topNode = cmds.ls(assemblies=True)
                    for i in topNode:
                        if refNode.split('RN')[0][:-5] in i:
                            fxGrp = i
                    print(fxGrp)
                    if not cmds.objExists('FX'):
                        cmds.group(em=True, name='FX' )
                    cmds.parent( fxGrp , 'FX' )

                    cmds.select(list)
                    command = f'file -import -type "atomImport" -ra true -options ";;targetTime=3;option=scaleReplace;match=mapFile;;selected=selectedOnly;search=;replace=;prefix=;suffix=;mapFile={mapfile};" {atomName};'
                    mel.eval(command)

        meshShape = cmds.ls( type='mesh', long = True)
        for i in meshShape:
            if ('Deformed' in i) and (i.split('|')[-1].split('Shape')[-1] != ''):                
                cmds.rename(i, i.split('|')[-1].replace('Deformed', ''))
                print (f"{i} renamed to {i.split('|')[-1].replace('Deformed', '')}")

        self.confirmMessage('Scene Collecting is completed!!')




    def lightPubOpenFileBrowser(self):

        proj = self.proj_list.currentText()
        shot_path = self.getShotPath(proj)
        currentShot  = self.shot_list.currentItem().text()
        selected_file= self.lightPub_list.currentItem().text()
        version = selected_file.split('.')[0]
        version = version.split('_')[-1]
        pub_file     = f'{shot_path}/{currentShot}/lit/output/exr/{selected_file.split(".")[0]}/workfile'
        os.startfile(pub_file)


    def saveLookDevWipBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save this file?'):
            return 0

        # make WIP maya dir
        wip_maya_dir = self.getLookDevSaveDir('work') + '/maya/scenes/increments'
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)
        
        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)
        wip_version = f'v{str(version_num).zfill(3)}'
        wip_maya_file = self.getLookDevSaveFile(wip_version, 'mb')
        wip_maya_path = f'{wip_maya_dir}/{wip_maya_file}'
        wip_texture_dir = wip_maya_dir+'/textures/'+wip_version+'/subs'
        if not os.path.isdir(wip_texture_dir):
            os.makedirs(wip_texture_dir)


        # save file

        self.mayaCleanup()
        cmds.file(rn=wip_maya_path)
        cmds.file(s=True, f=True)

        # update version list
        self.getLookDevVersion()

    def savelookDevPubBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save this file?'):
            return 0

        # save WIP
        # make WIP maya dir
        wip_maya_dir = self.getLookDevSaveDir('work') + '/maya/scenes/increments'
        if not os.path.isdir(wip_maya_dir):
            os.makedirs(wip_maya_dir)
        # make WIP save path
        version_num = self.getSaveVersion(wip_maya_dir)-1
        print('version_num = '+str(version_num))
        wip_version = f'v{str(version_num).zfill(3)}'

        print('wip_version = '+ wip_version)
        pub_maya_file = self.getLookDevSaveFile(wip_version, 'mb')
        pub_maya_path = self.getLookDevSaveDir('output') + '/shadegeo/shade_main/' + wip_version + '/maya'
        if not os.path.isdir(pub_maya_path):
            os.makedirs(pub_maya_path)
        else:
            self.errorMessage('!! Pub version does already Exist !!')
            return 0

        pub_maya_path = f'{pub_maya_path}/{pub_maya_file}'

        print ('wip_maya_file = ' + pub_maya_file)
        print ('pub_maya_path = ' + pub_maya_path)

        # save file
        self.mayaCleanup()
        cmds.file(rn=pub_maya_path)
        cmds.file(s=True, f=True)

        # make Publish dir
        pub_maya_dir = self.getLookDevSaveDir('output') + '/shadegeo/shade_main/' + wip_version + '/maya'
        
        if not os.path.isdir(pub_maya_dir):
            os.makedirs(pub_maya_dir)

        pub_json_dir = self.getLookDevSaveDir('output') + '/shadegeo/shade_main' + '/' + wip_version + '/maya'
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

            cmds.select(mat_list[0], r=True)
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

            pub_abc_path = self.getLookDevSaveDir('output') + '/shadegeo/shade_main' + '/' + wip_version + '/alembic'
            
            pub_abc_file = self.getLookDevSaveFile(wip_version, 'abc')

            # make publish alembic dir

            if not os.path.isdir(pub_abc_path):
                os.makedirs(pub_abc_path)
            pub_abc_path = pub_abc_path+'/'+pub_abc_file
            
            print ('pub_abc_path : ' + pub_abc_path)

            

            # select group

            
            item = [ i for i in cmds.ls(assemblies = True) if (cmds.listRelatives(i, s=True)) == None]
            print ('item = ' + str(item))
            cmds.select ( item )


            # export alembic selected group
            selectGroup = cmds.ls(sl=1,sn=True)
            command = f'AbcExport -j "-frameRange 1 1 -ro -uvWrite -writeColorSets -writeFaceSets -wholeFrameGeo -worldSpace -writeVisibility -eulerFilter -autoSubd -writeUVSets -dataFormat ogawa -root {selectGroup[0]} -file {pub_abc_path}";'
            mel.eval(command)

        else:
            print('DO not make ABC')



        # Copy Texture Files
        pub_texture_path = self.getLookDevSaveDir('output') + '/shadegeo/shade_main' + '/' + wip_version + '/maya/textures'
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
                    print(newName+' DELETE')
                    os.chmod( newName, stat.S_IWRITE )
                    os.remove(newName)
                
                shutil.copy(i, newName)
                
                
        # Copy Texture File Path
        fileNodes = cmds.ls(type='file')
        print (fileNodes)
        for fileNode in fileNodes:
            orgPath = cmds.getAttr(fileNode+'.fileTextureName')
            print (orgPath)
            
            texture_name = re.split('/', orgPath)[-1]
            
            newName = (pub_texture_path + '/'+ texture_name)
            cmds.setAttr(fileNode+'.fileTextureName', newName, type ='string' )

        aifileNodes = cmds.ls(type='aiImage')
        print (aifileNodes)
        for fileNode in aifileNodes:
            orgPath = cmds.getAttr(fileNode+'.filename')
            print (orgPath)
            
            texture_name = re.split('/', orgPath)[-1]
            
            newName = (pub_texture_path + '/'+ texture_name)
            cmds.setAttr(fileNode+'.filename', newName, type ='string' )
            shutil.copy(orgPath, newName)



        # export shader
        cmds.select([se for se in cmds.ls(typ='shadingEngine') if not re.search('^init', se)], ne=True, r=True)
        cmds.file(pub_mayaSD_file, op='v=0;', typ='mayaBinary', pr=True, es=True)
        cmds.select(cl=True)

        # save file
        self.mayaCleanup()
        cmds.file(s=True, f=True)

        # update version
        self.getLookDevVersion()

    def assignShaderBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to assign shader?'):
            return 0

        selectedList = cmds.listRelatives(cmds.ls(sl=True), allDescendents = True, fullPath = True)

        selected = cmds.ls(sl=True)
        if ':' in selected[0]:
            namespace = re.search('^[^:]*', selected[0]).group()
        else:
            print('namespace is not exist')
            namespace = ''

        # load shader json
        selected_version = self.LookDevPub_version.currentItem().text()
        pub_dir = self.getLookDevSaveDir('output') + '/shadegeo/shade_main/' + selected_version + '/maya'
        print ('json:pub_dir = '+pub_dir)
        
        pub_file = self.getLookDevSaveFile(selected_version, 'json')
        print ('json:pub_file = '+pub_file)
        json_path = f'{pub_dir}/{pub_file}'
        print ('json:son_path = '+json_path)
        #
        with open(json_path) as f:
            shader_dict = json.load(f)

        # import shader without namespace
        selected_version = self.LookDevPub_version.currentItem().text()
        shader_pub_dir = self.getLookDevSaveDir('output') + '/shadegeo/shade_main/' + selected_version + '/maya'
        shader_pub_file = self.getLookDevSaveFile(selected_version, 'mb')
        shader_pub_file = shader_pub_file.split('.')
        shader_pub_file = shader_pub_file[0]+'_SD.mb'
        shader_pub_path = f'{shader_pub_dir}/{shader_pub_file}'
        print('shader:shader_pub_path = '+shader_pub_path )
        cmds.file(shader_pub_path, i=True, typ='mayaBinary', iv=True, namespace=':', mnc=False, op="v=0;p=17;f=0", pr=True, itr='combine')

        # assign shader


        # surface shader


        for sg in shader_dict['surface']:
            mat = shader_dict['surface'][sg]['materials'][0]
            mat = cmds.ls(mat+'*')[-1]

            for obj in shader_dict['surface'][sg]['objects']:
                              

                if namespace :      
                    node = cmds.ls(namespace+':'+obj, long = True)    
                    print(node)
                else:
                    node = cmds.ls(obj, long = True)    
                    print(node)

                print ('node = ' + str(node))

                if len(node) >= 1:

                    for i in node:

                        if i in selectedList:
                            cmds.select(i)
                            cmds.hyperShade(a=mat)
                        else:
                            if '.f[' in i:
                                cmds.select(i)
                                cmds.hyperShade(a=mat)
                else:        
                    
                    print('NEXT')
                
                cmds.select(cl=True)




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
                    obj = f'{obj}'
                else:
                    obj_arr = []
                    for split_ele in obj_split:
                        split_ele = f'{split_ele}'
                        obj_arr.append(split_ele)
                    obj = '|'.join(obj_arr)

                if cmds.objExists(obj):
                    cmds.sets(obj, add=dis)

        
        cmds.select(cl=True)

    # common function

    def assetTypeOpenFileBrowser(self):
        proj = self.proj_list.currentText()
        assetTypePath = self.getAssetPath(proj) + '/' + self.asset_type.currentItem().text()
        print('assetTypePath = '+ assetTypePath)
        os.startfile(assetTypePath)

    def assetNameOpenFileBrowser(self):
        
        department_dir = self.getDepartmentDir('')
        assetName = department_dir
        print('assetName = '+ assetName)
        os.startfile(assetName)


    def openRigMidFileBrowser(self):
        
        department_dir = self.getDepartmentDir('rig/output/rig')
        rigMid_dir = department_dir
        print('rigMid_dir = '+ rigMid_dir)
        os.startfile(rigMid_dir)

    def openRigWipVerFileBrowser(self):
        
        rigWip_dir = self.getRigWipDir()
        rigWip_dir = rigWip_dir.replace('/', '\\')
        print('rigWip_dir = '+ rigWip_dir)
        os.startfile(rigWip_dir)

    def openRigWipFileBrowser(self):

        selected_version = self.rig_Wip_ver.currentItem().text()
        rigWip_dir = self.getRigWipDir() + '/' + selected_version + '/maya'
        rigWip_dir = rigWip_dir.replace('/', '\\')
        print('rigWip_dir = '+ rigWip_dir)
        os.startfile(rigWip_dir)

    def openRigPubVerFileBrowser(self):
        
        rigPub_dir = self.getRigPubDir()
        rigPub_dir = rigPub_dir.replace('/', '\\')
        print('rigPub_dir = '+ rigPub_dir)
        os.startfile(rigPub_dir)
        
    def openRigPubFileBrowser(self):

        selected_version = self.rig_Pub_ver.currentItem().text()
        rigPub_dir = self.getRigPubDir() + '/' + selected_version + '/maya'
        rigPub_dir = rigPub_dir.replace('/', '\\')
        print('rigPub_dir = '+ rigPub_dir)
        os.startfile(rigPub_dir)

    def openRigWipBtn(self):
        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0
        
        asset_name = self.asset_name.currentItem().text()
        selected_version = self.rig_Wip_ver.currentItem().text()
        middle_name = self.rigMiddle_list.currentItem().text()
        rigWip_dir = self.getRigWipDir() + '/' + selected_version + '/maya/'
        rigWip_dir = rigWip_dir.replace('/', '\\')
        print('rigWip_dir = '+ rigWip_dir)


        rigWip_file = rigWip_dir + '/' + asset_name + '_' + middle_name + '_' + selected_version + '.mb'
        print('rigWip_file = '+ rigWip_file)
        cmds.file(rigWip_file, o=True, f=True)

    def saveRigWipBtn(self):

        if QMessageBox.No == self.confirmMessage('Do you want to save this file?'):
            return 0

        asset_name = self.asset_name.currentItem().text()
        middle_name = self.rigMiddle_list.currentItem().text()        
        wip_maya_dir = self.getRigSaveDir('work') + '/rig/' + middle_name
        re_pattern = re.compile('v(\d{3})')

        print ('wip_maya_dir = ' + wip_maya_dir)

        if len(os.listdir(wip_maya_dir)) == 0:
            wip_version = 'v001'
            os.makedirs(wip_maya_dir + '/' + wip_version + '/maya/')
        else:        
            for file_ver in (os.listdir(wip_maya_dir)):
                for ver in (os.listdir(f'{wip_maya_dir}/{file_ver}/maya')):
                    if re.search(re_pattern, ver):
                        version_num = int(re.search(re_pattern, ver).group(1))+1
                        wip_version = f'v{str(version_num).zfill(3)}'


        # make WIP maya dir
        maya_dir = wip_maya_dir + '/' + wip_version + '/maya/'
        print ('maya_dir = '+ maya_dir)
        if not os.path.isdir(maya_dir):
            os.makedirs(maya_dir)

        # make WIP save path

        wip_maya_file = asset_name + '_' + middle_name + '_' + wip_version + '.mb'
        wip_maya_path = f'{maya_dir}/{wip_maya_file}'

        # save file
        print('wip_maya_path = ' + wip_maya_path)
        self.mayaCleanup()
        cmds.file(rn=wip_maya_path)
        cmds.file(s=True, f=True)

        # update version list
        self.getRigWipVersion()

    def openRigPubBtn(self):
        if QMessageBox.No == self.confirmMessage('Do you want to open this file?'):
            return 0
        
        asset_name = self.asset_name.currentItem().text()
        selected_version = self.rig_Pub_ver.currentItem().text()
        selected_file = self.pub_rig.currentItem().text()
        middle_name = self.rigMiddle_list.currentItem().text()
        rigPub_dir = self.getRigPubDir() + '/' + selected_version + '/maya'
        rigPub_dir = rigPub_dir.replace('/', '\\')
        print('rigPub_dir = '+ rigPub_dir)


        rigPub_file = rigPub_dir + '/' + selected_file
        print('rigPub_file = '+ rigPub_file)
        cmds.file(rigPub_file, o=True, f=True)
    
    def saveRigPubBtn(self):
        if QMessageBox.No == self.confirmMessage('Do you want to save this file?'):
            return 0
        
        asset_name = self.asset_name.currentItem().text()
        middle_name = self.rigMiddle_list.currentItem().text()
        pub_maya_dir = self.getRigSaveDir('output') + '/rig/' + middle_name
        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        raw_name, extension = os.path.splitext(filename)
        pattern = '_v([0-9]+)'
        pub_version = 'v'+str(re.search(pattern, raw_name).group(1))




        # make PUB maya dir
        pub_maya_dir = self.getRigSaveDir('output') + '/rig/' + middle_name + '/' + pub_version + '/maya/'
        if not os.path.isdir(pub_maya_dir):
            os.makedirs(pub_maya_dir)

        # make PUB save path

        pub_maya_file = asset_name + '_' + middle_name + '_' + pub_version + '.mb'
        pub_maya_path = f'{pub_maya_dir}/{pub_maya_file}'

        # save file
        print('pub_maya_path = ' + pub_maya_path)

        if os.path.isfile(pub_maya_path):
            self.errorMessage('!! Pub version does already Exist !!')
            return 0

        self.mayaCleanup()
        cmds.file(rn=pub_maya_path)
        cmds.file(s=True, f=True)

        # update version list
        self.getRigPubVersion()


    def openLookDevWipFileBrowser(self):

        wip_dir = self.getLookDevSaveDir('work') + '/maya/scenes/increments'
        wip_dir = wip_dir.replace('/', '\\')
        print('wip_dir = '+ wip_dir)
        os.startfile(wip_dir)

    # semi common function
    def openLookDevPubFileBrowser(self):

        pub_dir = self.getLookDevSaveDir('output') + '/shadegeo/shade_main/'+ self.LookDevPub_version.currentItem().text() + '/maya'
        print ('pub_dir : '+pub_dir)
        pub_dir = pub_dir.replace('/', '\\')
        os.startfile(pub_dir)

        
    def closeEvent(self, event):

        self.saveCurrentENV()
        

    def initUI(self):

        # project list
        self.proj_list = QComboBox()
        self.proj_list.setMaximumWidth(130)
        self.getProjectList()
        self.proj_list.currentIndexChanged.connect(self.getEpisodeList)

        # episode list
        self.episode_list = QListWidget()        
        self.episode_list.currentItemChanged.connect(self.getAssetType)
        self.episode_list.currentItemChanged.connect(self.getShotList)
        episode_layout = QVBoxLayout()
        episode_layout_label = QLabel('Episode')
        episode_layout.addWidget(self.proj_list)
        episode_layout.addWidget(episode_layout_label)
        episode_layout.addWidget(self.episode_list)        
        episode_grp = QGroupBox('Project')        
        episode_grp.setLayout(episode_layout)
        episode_grp.setMaximumWidth(130)

        # shot list
        
        self.shot_list = QListWidget()        
        self.shot_list.currentItemChanged.connect(self.getLayoutWip)
        self.shot_list.currentItemChanged.connect(self.getLayoutPub)
        self.shot_list.currentItemChanged.connect(self.getAniWip)
        self.shot_list.currentItemChanged.connect(self.getAniPub)
        self.shot_list.currentItemChanged.connect(self.getlightWip)
        self.shot_list.currentItemChanged.connect(self.getlightPub)
        #PlayBlaster_btn = QPushButton('PlayBlaster')
        #PlayBlaster_btn.clicked.connect(self.playblasterBtn)
        shot_layout = QVBoxLayout()
        shot_layout.addWidget(self.shot_list)
        #shot_layout.addWidget(PlayBlaster_btn)
        shot_grp = QGroupBox('Shot List')
        shot_grp.setMaximumWidth(130)
        shot_grp.setLayout(shot_layout)
        




        ## layout list ##

        # layout wip
        layoutWipOpen_btn = QPushButton('Open Wip')
        layoutWipSave_btn = QPushButton('Save Wip')
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
        layoutList_grp.setCheckable(True)
        layoutList_grp.setChecked(False)
        layoutList_grp.setLayout(layoutList_layout)


        ## animation list ##

        # ani wip
        aniWipOpen_btn = QPushButton('Open Wip')
        aniWipSave_btn = QPushButton('Save Wip')
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
        aniList_grp.setCheckable(True)
        aniList_grp.setChecked(False)
        aniList_grp.setLayout(aniList_layout)


        ## lighting list ##

        # lighting wip
        lightCollect_btn = QPushButton('Collect')
        lightWipOpen_btn = QPushButton('Open Wip')
        lightWipSave_btn = QPushButton('Save Wip')
        lightCollect_btn.clicked.connect(self.lightCollectBtn)
        lightWipOpen_btn.clicked.connect(self.lightOpenWIPBtn)
        lightWipSave_btn.clicked.connect(self.lightSaveWIPBtn)
        lightWip_lable = QLabel('Light Wip')
        self.lightWip_list = QListWidget()
        self.lightWip_list.itemDoubleClicked.connect(self.lightWipOpenFileBrowser)
        lightWip_layout = QVBoxLayout()
        lightWip_layout.addWidget(lightWip_lable)
        lightWip_layout.addWidget(self.lightWip_list)
        lightWip_layout.addWidget(lightCollect_btn)
        lightWip_layout.addWidget(lightWipOpen_btn)
        lightWip_layout.addWidget(lightWipSave_btn)

        # light pub
        lightPubOpen_btn = QPushButton('Open Pub')
        lightPubSave_btn = QPushButton('Publish')
        lightPubOpen_btn.clicked.connect(self.lightOpenPubBtn)
        lightPubSave_btn.clicked.connect(self.lightSavePubBtn)
        lightPub_lable = QLabel('Light Pub')
        self.lightPub_list = QListWidget()
        self.lightPub_list.itemDoubleClicked.connect(self.lightPubOpenFileBrowser)
        lightPub_layout = QVBoxLayout()
        lightPub_layout.addWidget(lightPub_lable)
        lightPub_layout.addWidget(self.lightPub_list)
        lightPub_layout.addWidget(lightPubOpen_btn)
        lightPub_layout.addWidget(lightPubSave_btn)
        
        # light_list 
        lightList_layout  = QHBoxLayout()
        lightList_layout.addLayout(lightWip_layout)
        lightList_layout.addLayout(lightPub_layout)
        lightList_grp = QGroupBox('Lighting List')
        lightList_grp.setCheckable(True)
        lightList_grp.setChecked(False)
        lightList_grp.setLayout(lightList_layout)


        # asset type
        self.asset_type = QListWidget()
        self.asset_type.currentItemChanged.connect(self.getAssetName)
        self.asset_type.itemDoubleClicked.connect(self.assetTypeOpenFileBrowser)
        asset_type_layout = QVBoxLayout()
        asset_type_layout.addWidget(self.asset_type)
        asset_type_grp = QGroupBox('Asset Type')
        asset_type_grp.setLayout(asset_type_layout)

        # asset name
        self.asset_name = QListWidget()
        self.asset_name.setMinimumWidth(100)
        self.asset_name.currentItemChanged.connect(self.getRigMiddleName)
        self.asset_name.itemDoubleClicked.connect(self.assetNameOpenFileBrowser)
        asset_name_layout = QVBoxLayout()
        asset_name_layout.addWidget(self.asset_name)
        asset_name_grp = QGroupBox('Asset Name')
        asset_name_grp.setLayout(asset_name_layout)



        ## MODEL LIST ##


        # Rig version

        # Rig middle name
        rigMiddle_name_label = QLabel('Middle Name')
        self.rigMiddle_list = QListWidget()
        self.rigMiddle_list.currentItemChanged.connect(self.getRigPubVersion)
        self.rigMiddle_list.currentItemChanged.connect(self.getRigWipVersion)
        self.rigMiddle_list.itemDoubleClicked.connect(self.openRigMidFileBrowser)
        rigMiddle_name_layout = QVBoxLayout()
        rigMiddle_name_layout.addWidget(rigMiddle_name_label)
        rigMiddle_name_layout.addWidget(self.rigMiddle_list)

        # Rig Wip version
        rigWipVerLabel = QLabel('wipVer')
        self.rig_Wip_ver = QListWidget()
        self.rig_Wip_ver.setMinimumWidth(40)
        self.rig_Wip_ver.currentItemChanged.connect(self.getRigWipName)
        self.rig_Wip_ver.itemDoubleClicked.connect(self.openRigWipVerFileBrowser)
        rigWipVerLayout = QVBoxLayout()
        rigWipVerLayout.addWidget(rigWipVerLabel)
        rigWipVerLayout.addWidget(self.rig_Wip_ver)

        # wipRIG List
        wip_rig_label = QLabel('RIG Wip')
        self.wip_rig = QListWidget()
        self.wip_rig.setMinimumWidth(140)
        self.wip_rig.itemDoubleClicked.connect(self.openRigWipFileBrowser)
        wip_rig_layout = QVBoxLayout()
        wip_rig_layout.addWidget(wip_rig_label)
        wip_rig_layout.addWidget(self.wip_rig)

        # Rig Pub version
        rigPubVerLabel = QLabel('pubVer')
        self.rig_Pub_ver = QListWidget()
        self.rig_Pub_ver.setMinimumWidth(40)
        self.rig_Pub_ver.currentItemChanged.connect(self.getRigPubName)
        self.rig_Pub_ver.itemDoubleClicked.connect(self.openRigPubVerFileBrowser)
        rigPubVerLayout = QVBoxLayout()
        rigPubVerLayout.addWidget(rigPubVerLabel)
        rigPubVerLayout.addWidget(self.rig_Pub_ver)

        # Rig reference import
        Rig_ref_btn = QPushButton('Asset Ref import')
        Rig_ref_btn.clicked.connect(self.assetRefBtn)

        # Rig replace
        Rig_rep_btn = QPushButton('Asset replace')
        Rig_rep_btn.clicked.connect(self.assetRepBtn)
        #

        # pubRIG List
        pub_rig_label = QLabel('RIG Pub')
        self.pub_rig = QListWidget()
        self.pub_rig.setMinimumWidth(140)
        self.pub_rig.itemDoubleClicked.connect(self.openRigPubFileBrowser)
        pub_rig_layout = QVBoxLayout()
        pub_rig_layout.addWidget(pub_rig_label)
        pub_rig_layout.addWidget(self.pub_rig)


        rigVersion_layoutA = QHBoxLayout()
        rigVersion_layoutA.addLayout(rigWipVerLayout)
        rigVersion_layoutA.addLayout(wip_rig_layout)

        rigVersion_layoutB = QHBoxLayout()
        rigVersion_layoutB.addLayout(rigPubVerLayout)
        rigVersion_layoutB.addLayout(pub_rig_layout)


        rigAssetBtn_layout = QVBoxLayout()
        rigAssetBtn_layout.addWidget(Rig_ref_btn)
        rigAssetBtn_layout.addWidget(Rig_rep_btn)
        rigAssetBtn_grp = QGroupBox('Reference Asset')
        rigAssetBtn_grp.setLayout(rigAssetBtn_layout)


        rigVersion_layoutC = QVBoxLayout()
        rigVersion_layoutC.addLayout(rigVersion_layoutB)
        rigVersion_layoutC.addWidget(rigAssetBtn_grp)
        
        rigVersion_layoutD = QHBoxLayout()
        rigVersion_layoutD.addLayout(rigVersion_layoutA)
        rigVersion_layoutD.addLayout(rigVersion_layoutC)

        rigVersion_layout = QVBoxLayout()
        rigVersion_layout.addLayout(rigVersion_layoutD)
        rigVersion_layout.addLayout(rigVersion_layoutC)

        
        # RigWip/RigPub button
        # RigvWip button
        open_RigWip_btn = QPushButton('Open Wip')
        open_RigWip_btn.clicked.connect(self.openRigWipBtn)
        save_RigWip_btn = QPushButton('WIP Save')
        save_RigWip_btn.clicked.connect(self.saveRigWipBtn)
        RigWipBtn_layout = QVBoxLayout()
        RigWipBtn_layout.addWidget(open_RigWip_btn)
        RigWipBtn_layout.addWidget(save_RigWip_btn)
        # RigPub button
        RigPub_btn = QPushButton('Publish')
        RigPub_btn.clicked.connect(self.saveRigPubBtn)
        open_RigPub_btn = QPushButton('Open Pub')
        open_RigPub_btn.clicked.connect(self.openRigPubBtn)
        RigPubBtn_layout = QVBoxLayout()
        RigPubBtn_layout.addWidget(open_RigPub_btn)
        RigPubBtn_layout.addWidget(RigPub_btn)
        # RigButton layout
        RigVerBtn_layout = QHBoxLayout()
        RigVerBtn_layout.addLayout(RigWipBtn_layout)
        RigVerBtn_layout.addLayout(RigPubBtn_layout)

        #
        rig_layoutA = QVBoxLayout()
        rig_layoutA.addLayout(rigVersion_layout)
        rig_layoutA.addLayout(RigVerBtn_layout)


        rig_layout = QHBoxLayout()
        rig_layout.addLayout(rigMiddle_name_layout)
        rig_layout.addLayout(rig_layoutA)
        rig_layout_grp = QGroupBox('Rig')
        rig_layout_grp.setCheckable(True)
        rig_layout_grp.setChecked(False)
        rig_layout_grp.setLayout(rig_layout)


        # LookDev version

        # LookDevWip version list


        self.LookDevWip_version = QListWidget()
        self.LookDevWip_version.setMinimumWidth(80)
        self.LookDevWip_version.itemDoubleClicked.connect(self.openLookDevWipFileBrowser)
        LookDevWip_version_layout = QVBoxLayout()
        LookDevWip_version_layout.addWidget(self.LookDevWip_version)
        LookDevWip_version_grp = QGroupBox('WIP Version')
        LookDevWip_version_grp.setLayout(LookDevWip_version_layout)

        # LookDevPub version list
        assign_shader_btn = QPushButton('Assign Shader')
        assign_shader_btn.clicked.connect(self.assignShaderBtn)

        self.LookDevPub_version = QListWidget()
        self.LookDevPub_version.setMinimumWidth(80)
        self.LookDevPub_version.itemDoubleClicked.connect(self.openLookDevPubFileBrowser)
        LookDevPub_version_layout = QVBoxLayout()
        LookDevPub_version_layout.addWidget(self.LookDevPub_version)
        LookDevPub_version_layout.addWidget(assign_shader_btn)
        LookDevPub_version_grp = QGroupBox('Publish Version')
        LookDevPub_version_grp.setLayout(LookDevPub_version_layout)
        # version layout
        lookDevVer_layout = QHBoxLayout()
        lookDevVer_layout.addWidget(LookDevWip_version_grp)
        lookDevVer_layout.addWidget(LookDevPub_version_grp)

        # lookDevWip/lookDevpub button
        # lookDevWip button
        open_LookDevWip_btn = QPushButton('Open Wip')        
        open_LookDevWip_btn.clicked.connect(self.openLookDevWipBtn)
        save_LookDevWip_btn = QPushButton('WIP Save')
        save_LookDevWip_btn.clicked.connect(self.saveLookDevWipBtn)
        LookDevWip_layout = QVBoxLayout()
        LookDevWip_layout.addWidget(open_LookDevWip_btn)
        LookDevWip_layout.addWidget(save_LookDevWip_btn)
        # lookDevPub button
        lookDevPub_btn = QPushButton('Publish')
        lookDevPub_btn.clicked.connect(self.savelookDevPubBtn)
        open_LookDevPub_btn = QPushButton('Open Pub')        
        open_LookDevPub_btn.clicked.connect(self.openLookDevPubBtn)
        lookDevPub_layout = QVBoxLayout()
        lookDevPub_layout.addWidget(open_LookDevPub_btn)
        lookDevPub_layout.addWidget(lookDevPub_btn)
        # lookDevButton layout
        lookDevbtn_layout = QHBoxLayout()
        lookDevbtn_layout.addLayout(LookDevWip_layout)
        lookDevbtn_layout.addLayout(lookDevPub_layout)


        # lookDev_layout
        lookDev_layout = QVBoxLayout()
        lookDev_layout.addLayout(lookDevVer_layout)
        lookDev_layout.addLayout(lookDevbtn_layout)
        lookDev_layout_grp = QGroupBox('Look Dev')
        lookDev_layout_grp.setCheckable(True)
        lookDev_layout_grp.setChecked(False)
        lookDev_layout_grp.setLayout(lookDev_layout)


        # column1 layout
        column1_layout = QVBoxLayout()
        #
        column1_row1_layout = QHBoxLayout()
        column1_row1_layout.addWidget(episode_grp)
        column1_row1_layout.addWidget(asset_type_grp)
        column1_row1_layout.addWidget(asset_name_grp)        
        column1_row1_layout.addWidget(lookDev_layout_grp) # lookdevUI
        column1_row1_layout.addWidget(rig_layout_grp)
        #

        column1_layout.addLayout(column1_row1_layout)


        # column2 layout
        column2_layout = QHBoxLayout()
        column2_layout.addWidget(shot_grp)
        column2_layout.addWidget(layoutList_grp)
        column2_layout.addWidget(aniList_grp)
        column2_layout.addWidget(lightList_grp)



        # main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(column1_layout)
        main_layout.addLayout(column2_layout)
        self.setLayout(main_layout)

        self.setWindowTitle(f'piplineTool [version : {toolVersion} PROJ_DRIVE = {PROJ_DRIVE}]')
        self.show()

        cmds.window(self.window_name, e=True, w=1000)



piplineToolUI()