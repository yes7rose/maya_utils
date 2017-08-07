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
        load_result = cmds.loadPlugin(pluginName)
        if load_result:
            MGlobal.displayInfo("plugin " + pluginName + " loaded success")
            return True
        else:
            MGlobal.displayError("Can find and load plugin:%s"%pluginName)
            return False
    else:
        MGlobal.displayInfo("Plugin already loaded:%s"%pluginName)
        return True