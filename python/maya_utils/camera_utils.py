# encoding:utf-8

import maya.cmds as cmds
import maya.mel as mel

from api_utils import getMObjectFromName

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

# return True if the two cameras are identical
def compareCamera( nodeName1, nodeName2 ):

    # basic error checking
    obj1 = getMObjectFromName(nodeName1)
    if not obj1.hasFn(OpenMaya.MFn.kCamera):
        return False

    obj2 = getMObjectFromName(nodeName2)
    if not obj2.hasFn(OpenMaya.MFn.kCamera):
        return False

    fn1 = OpenMaya.MFnCamera( obj1 )
    fn2 = OpenMaya.MFnCamera( obj2 )

    if fn1.filmFit() != fn2.filmFit():
        print "differ in filmFit"
        return False

    if not floatDiff(fn1.filmFitOffset(), fn2.filmFitOffset(), 4):
        print "differ in filmFitOffset"
        return False

    if fn1.isOrtho() != fn2.isOrtho():
        print "differ in isOrtho"
        return False

    if not floatDiff(fn1.orthoWidth(), fn2.orthoWidth(), 4):
        print "differ in orthoWidth"
        return False

    if not floatDiff(fn1.focalLength(), fn2.focalLength(), 4):
        print "differ in focalLength"
        return False

    if not floatDiff(fn1.lensSqueezeRatio(), fn2.lensSqueezeRatio(), 4):
        print "differ in lensSqueezeRatio"
        return False

    if not floatDiff(fn1.cameraScale(), fn2.cameraScale(), 4):
        print "differ in cameraScale"
        return False

    if not floatDiff(fn1.horizontalFilmAperture(),
        fn2.horizontalFilmAperture(), 4):
        print "differ in horizontalFilmAperture"
        return False

    if not floatDiff(fn1.verticalFilmAperture(), fn2.verticalFilmAperture(), 4):
        print "differ in verticalFilmAperture"
        return False

    if not floatDiff(fn1.horizontalFilmOffset(), fn2.horizontalFilmOffset(), 4):
        print "differ in horizontalFilmOffset"
        return False

    if not floatDiff(fn1.verticalFilmOffset(), fn2.verticalFilmOffset(), 4):
        print "differ in verticalFilmOffset"
        return False

    if not floatDiff(fn1.overscan(), fn2.overscan(), 4):
        print "differ in overscan"
        return False

    if not floatDiff(fn1.nearClippingPlane(), fn2.nearClippingPlane(), 4):
        print "differ in nearClippingPlane"
        return False

    if not floatDiff(fn1.farClippingPlane(), fn2.farClippingPlane(), 4):
        print "differ in farClippingPlane"
        return False

    if not floatDiff(fn1.preScale(), fn2.preScale(), 4):
        print "differ in preScale"
        return False

    if not floatDiff(fn1.postScale(), fn2.postScale(), 4):
        print "differ in postScale"
        return False

    if not floatDiff(fn1.filmTranslateH(), fn2.filmTranslateH(), 4):
        print "differ in filmTranslateH"
        return False

    if not floatDiff(fn1.filmTranslateV(), fn2.filmTranslateV(), 4):
        print "differ in filmTranslateV"
        return False

    if not floatDiff(fn1.horizontalRollPivot(), fn2.horizontalRollPivot(), 4):
        print "differ in horizontalRollPivot"
        return False

    if not floatDiff(fn1.verticalRollPivot(), fn2.verticalRollPivot(), 4):
        print "differ in verticalRollPivot"
        return False

    if fn1.filmRollOrder() != fn2.filmRollOrder():
        print "differ in filmRollOrder"
        return False

    if not floatDiff(fn1.filmRollValue(), fn2.filmRollValue(), 4):
        print "differ in filmRollValue"
        return False

    if not floatDiff(fn1.fStop(), fn2.fStop(), 4):
        print "differ in fStop"
        return False

    if not floatDiff(fn1.focusDistance(), fn2.focusDistance(), 4,):
        print "differ in focusDistance"
        return False

    if not floatDiff(fn1.shutterAngle(), fn2.shutterAngle(), 4):
        print "differ in shutterAngle"
        return False

    if fn1.usePivotAsLocalSpace() != fn2.usePivotAsLocalSpace():
        print "differ in usePivotAsLocalSpace"
        return False

    if fn1.tumblePivot() != fn2.tumblePivot():
        print "differ in tumblePivot"
        return False

    return True
