#
# maya 2022
# mayapy 3.7.7

from winreg import QueryValue
from maya import OpenMayaUI as omui

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance

import maya.cmds as cmds

import re
import sys


def checkPolyVertexNormal():

    for mesh in cmds.ls(typ='mesh', ap=True):
        tnode = cmds.listRelatives(mesh, p=True, f=True)[0]

        edge_count = cmds.polyEvaluate(tnode, e=True) - 1
        cmds.polySoftEdge(f'{tnode}.e[0:{edge_count}]', a=0) # setToFace
        cmds.polySoftEdge(tnode, a=30, ch=True) # soften/harden edge
        cmds.delete(all=True, ch=True)

    cmds.select(cl=True)

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

def getMayaMainWindow():

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)

    return mayaMainWindow

        
class NotEqualShapename(QWidget):

    def __init__(self):

        super().__init__()

        self.window_name = 'keyring_ae65f8640285f4253575aed1c98fd414'
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name)
        self.setParent(getMayaMainWindow())
        self.setWindowFlags(Qt.Window)
        self.setObjectName(self.window_name)

        self.initUI()

    def notEqualShapename(self):

        not_equal_shape_name = checkNotEqualShapename()

        self.transform_list.clear()
        self.shape_list.clear()

        for transformname in not_equal_shape_name:
            shapename = not_equal_shape_name[transformname]

            self.transform_list.addItem(transformname)
            self.shape_list.addItem(shapename)

    def selectTransformNode(self):

        selected_item = self.transform_list.currentItem().text()

        cmds.select(selected_item, r=True)

    def selectShapeNode(self):

        selected_item = self.shape_list.currentItem().text()

        cmds.select(selected_item, r=True)

    def initUI(self):

        not_unique_btn = QPushButton('Search not equal shape name')
        not_unique_btn.clicked.connect(self.notEqualShapename)

        self.transform_list = QListWidget()
        self.transform_list.itemClicked.connect(self.selectTransformNode)
        transform_layout = QVBoxLayout()
        transform_layout.addWidget(self.transform_list)
        transform_grp = QGroupBox('Transform Node')
        transform_grp.setLayout(transform_layout)

        self.shape_list = QListWidget()
        self.shape_list.itemClicked.connect(self.selectShapeNode)
        shape_layout = QVBoxLayout()
        shape_layout.addWidget(self.shape_list)
        shape_grp = QGroupBox('Shape Node')
        shape_grp.setLayout(shape_layout)

        list_layout = QHBoxLayout()
        list_layout.addWidget(transform_grp)
        list_layout.addWidget(shape_grp)

        main_layout = QVBoxLayout()
        main_layout.addWidget(not_unique_btn)
        main_layout.addLayout(list_layout)

        self.setLayout(main_layout)

        self.setWindowTitle('Not Equal Shapenode Name')
        self.show()
