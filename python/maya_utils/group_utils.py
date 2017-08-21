# encoding:utf-8

import maya.cmds as cmds

def getGroupAllDecendShapeNodes(group_name):
    """
    """
    shapeList = cmds.ls(group_name, dag=True, shapes=True)

    return shapeList

def getShapeSiblings(shape_node):
    """
    """
    parent = cmds.listRelatives(shape_node, parent=True)
    shape_list = cmds.listRelatives(parent, children=True)

    if len(shape_list) <= 1:
        print("shape have no sibling")
        return None
    
    shape_list.remove(shape_node)

    return shape_list