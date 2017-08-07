# encoding:utf-8

from maya.openMaya import MGlobal
import maya.cmds as cmds


def movePivotToBottomCenter(objectName=""):
    """
    Move Object pivots to bottom centor for ajust.

    :param objectName: trasnform node name.
    :return: bool
    """
    if not objectName:
        MGlobal.displayError("Please provide ObjectName")
        return False

    boxMin = cmds.getAttr(objectName + ".boundingBoxMin")[0]
    boxMax = cmds.getAttr(objectName + ".boundingBoxMax")[0]

    posx = (boxMax[0] + boxMin[0]) / 2
    posy = boxMin[1]
    posz = (boxMax[2] + boxMin[2]) / 2
    bottomCenter = [posx, posy, posz]
    cmds.xform(objectName, piv=bottomCenter, ws=True)

    return True

def moveObjectToOrigin(objectName=""):
    """
    move object to world 0 0 0

    :param objectName:
    :return:
    """
    if not objectName:
        MGlobal.displayError("Please provide ObjectName")
        return False

    localPivot = cmds.xform(objectName , q=True, rotatePivot=True)
    worldPivot = cmds.xform(objectName , q=True, rotatePivot=True, worldSpace=True)

    posx = 0.0
    posy = 0.0
    posz = 0.0

    if  worldPivot[0] == localPivot[0]:
        posx = worldPivot[0]
    else:
        posx = worldPivot[0] - localPivot[0]

    if  worldPivot[1] == localPivot[1]:
        posy = worldPivot[1]
    else:
        posy = worldPivot[1] - localPivot[1]

    if  worldPivot[2] == localPivot[2]:
        posz = worldPivot[2]
    else:
        posz = worldPivot[2] - localPivot[2]


    cmds.move(-posx, -posy, -posz, objectName, absolute=True)