# encoding:utf-8

import  maya.cmds as cmds


def makeObjectIsolateOn(objectName):
    """
    make object isolate view on
    :param objectName:
    :return:
    """
    if objectName:
        #currentView = cmds.paneLayout('viewPanes', q=True, pane1=True)
        currentView = u'modelPanel4'

        cmds.select(objectName, replace=True)
        cmds.isolateSelect(currentView, state=1)


def makeObjectIsolateOff(objectName):
    """
    make object isolate view off
    :param objectName:
    :return:
    """
    if objectName:
        #currentView = cmds.paneLayout('viewPanes', q=True, pane1=True)
        currentView = u'modelPanel4'
        cmds.select(objectName, replace=True)
        cmds.isolateSelect(currentView, state=0)