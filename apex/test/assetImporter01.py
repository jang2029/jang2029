from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.mel as mel

import os
import csv
import re
import json
import sys



ASSET_FOLDER = 'P:/projects/eaapexseason17_42048P/assets/3D'
tmp_dir =  os.getenv('TMP').replace('\\', '/')
env_path = f'{tmp_dir}/pipeline_ENV.json'
print (env_path)

def getMayaMainWindow():

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

    return mayaMainWindow





class ModelUI(QWidget):


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