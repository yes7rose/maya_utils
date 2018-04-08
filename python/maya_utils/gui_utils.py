# encoding:utf-8

import maya.OpenMayaUI as apiUI
# import sip
import shiboken

from PySide import QtGui, QtCore

# def sipGetMayaWindow():
#    """
#    Get the main Maya window as a QtGui.QMainWindow instance
#    @return: QtGui.QMainWindow instance of the top level Maya windows
#    """
#    ptr = apiUI.MQtUtil.mainWindow()
#    if ptr is not None:
#        return sip.wrapinstance(long(ptr), QtCore.QObject)


def shibokenGetMayaMainWindow():
    mayaMainWindowPtr = apiUI.MQtUtil.mainWindow()
    print(mayaMainWindowPtr)
    if mayaMainWindowPtr:
        mayaMainWindow = shiboken.wrapInstance(long(mayaMainWindowPtr), QtGui.QWidget)
        return mayaMainWindow
    else:
        return None

# def sipToQtObject(mayaName):
#    """
#    Convert a Maya ui path to a Qt object
#    @param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
#    @return: PyQt representation of that object
#    """
#    ptr = apiUI.MQtUtil.findControl(mayaName)
#    if ptr is None:
#        ptr = apiUI.MQtUtil.findLayout(mayaName)
#    if ptr is None:
#        ptr = apiUI.MQtUtil.findMenuItem(mayaName)
#    if ptr is not None:
#        return sip.wrapinstance(long(ptr), QtCore.QObject)