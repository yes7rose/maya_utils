# encoding:utf-8

from maya.OpenMaya import MGlobal

import maya.cmds as cmds


def checkAndLoadPlugin(pluginName=""):
    """
    load plugin if not loaded.
    :param pluginName:
    :return:
    """
    if not cmds.pluginInfo(pluginName, query=True, loaded=True):
        cmds.loadPlugin(pluginName)
        MGlobal.displayInfo("plugin " + pluginName + " loaded success")