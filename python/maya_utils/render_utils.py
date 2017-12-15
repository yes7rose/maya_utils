# encoding:utf-8

import maya.cmds as cmds

def getRenderSize():
    """
    """
    width = cmds.getAttr("defaultResolution.width")
    height = cmds.getAttr("defaultResolution.height")

    return (width, height)

def getRenderStartEndFrame():
    """

    :return: start and end frame number
    """
    start = cmds.getAttr("defaultRenderGlobals.startFrame")
    end = cmds.getAttr("defaultRenderGlobals.endFrame")

    return (start, end)