# encoding:utf-8

import maya.cmds as cmds

def get_render_size():
    """
    """
    width = cmds.getAttr("defaultResolution.width")
    height = cmds.getAttr("defaultResolution.height")

    return (width, height)
