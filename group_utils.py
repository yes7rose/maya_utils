# encoding:utf-8

import maya.cmds as cmds

def getGroupAllDecendShapeNodes(group_name):
    """
    """
    shapeList = cmds.ls(group_name, dag=True, shapes=True)

    return shapeList

