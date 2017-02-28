# encoding:utf-8

import maya.cmds as cmds
import maya.mel as mel

def createPreviewCamera(objectName):
    """
    create object preview camera, frame the object
    :param objectName:
    :return:
    """
    cmds.camera()
    cmds.rename("preview")
    mel.eval("cameraMakeNode 2 \"\";")
    selList = cmds.ls(selection=True)
    # print(selList)

    previewCam = selList[0]
    previewAim = selList[1]

    boxMin = cmds.getAttr(objectName + ".boundingBoxMin")[0]
    boxMax = cmds.getAttr(objectName + ".boundingBoxMax")[0]

    ## move aim to bbx center
    aimPos = [(boxMax[0] + boxMin[0]) / 2, (boxMax[1] + boxMin[1]) / 2, (boxMax[2] + boxMin[2]) / 2]
    # print(aimPos)
    cmds.move(aimPos[0], aimPos[1], aimPos[2], previewAim)

    camPosy = boxMax[1] * 1.7
    camPosx = boxMin[0] + camPosy * 1.2
    camPosz = boxMin[2] + camPosy * 1.2
    cmds.move(camPosx, camPosy, camPosz, previewCam)

    preCamShape = cmds.listRelatives(previewCam, children=True)[0]
    cmds.lookThru(preCamShape, "perspView")
