# -*- coding: utf-8 -*-

#Source code for some common Maya/PyQt functions we will be using
#import sip
# sip.setapi('QString', 2)
# sip.setapi('QVariant', 2)
from PySide import QtGui, QtCore
import shiboken
import os
import itertools

import maya.OpenMayaUI as apiUI
from maya.OpenMaya import MGlobal
from maya.OpenMaya import MObject
from maya.OpenMaya import MFnDependencyNode
from maya.OpenMaya import MDagPath
from maya.OpenMaya import MSelectionList
from maya.OpenMaya import MPlug
from maya.OpenMaya import MFnNumericAttribute
from maya.OpenMaya import MFnNumericData
from maya.OpenMaya import MFn
from maya.OpenMaya import MFnUnitAttribute
from maya.OpenMaya import MFnTypedAttribute
from maya.OpenMaya import MFnData

import maya.cmds as cmds
import pymel.core as pmcore
import maya.mel as mel

#def sipGetMayaWindow():
#    """
#    Get the main Maya window as a QtGui.QMainWindow instance
#    @return: QtGui.QMainWindow instance of the top level Maya windows
#    """
#    ptr = apiUI.MQtUtil.mainWindow()
#    if ptr is not None:
#        return sip.wrapinstance(long(ptr), QtCore.QObject)


def shibokenGetMayaMainWindow():
    mayaMainWindowPtr = apiUI.MQtUtil.mainWindow()
    if mayaMainWindowPtr:
        mayaMainWindow = shiboken.wrapInstance(long(mayaMainWindowPtr), QtGui.QWidget)
        return mayaMainWindow
    else:
        return None

#def sipToQtObject(mayaName):
#    """
#    Convert a Maya ui path to a Qt object
#    @param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
#    @return: PyQt representation of that object
#    """
#    ptr = apiUI.MQtUtil.findControl(mayaName)
#    if ptr is None:
#        ptr = apiUI.MQtUtil.findLayout(mayaName)
#    if ptr is None:
#        ptr = apiUI.MQtUtil.findMenuItem(mayaName)
#    if ptr is not None:
#        return sip.wrapinstance(long(ptr), QtCore.QObject)

def getNodeFromName(in_name):
    selector = MSelectionList()
    MGlobal.getSelectionListByName(in_name, selector)
    node = MObject()
    selector.getDependNode(0, node)
    return node


def getDependNodeFromName(in_name):
    return MFnDependencyNode(getNodeFromName(in_name))


def getDagPathFromName(in_name):
    selector = MSelectionList()
    MGlobal.getSelectionListByName(in_name, selector)
    path = MDagPath()
    selector.getDagPath(0, path)
    return path

def findMPlug(in_node, in_attribute):
    '''
    @param in_node_name: string, unique name of the node,
    meaning the full path if multiple nodes of this name exist
    @param in_attribute_name: string, attribute to find,
    should exist or you'll get errors
    '''
    node = getNodeFromName(in_node)
    return MPlug(node, MFnDependencyNode(node).attribute(in_attribute))


def getPlugValue(in_plug):
    '''
    @param in_plug: MPlug, to get value from
    '''
    plugs = []
    if in_plug.isCompound():
        for i in in_plug.numChildren():
            plugs.append(in_plug.child(i))
    elif in_plug.isArray():
        for i in in_plug.numElements():
            plugs.append(in_plug.getElementByPhysicalIndex(i))
    else:
        plugs.append(in_plug)

    out = [] #compound list of all data in the plug or its child plugs
    for plug in plugs:
        attr = plug.attribute()
        if attr.hasFn(MFn.kNumericAttribute):
            type = MFnNumericAttribute(attr).unitType()
            if type in (MFnNumericData.kBoolean, MFnNumericData.kByte):
                out.append(plug.asBool())
            elif type == MFnNumericData.kChar:
                out.append(plug.asChar())
            elif type == MFnNumericData.kShort:
                out.append(plug.asShort())
            elif type in (MFnNumericData.kInt, MFnNumericData.kLong):
                out.append(plug.asInt())
            elif type == MFnNumericData.kFloat:
                out.append(plug.asFloat())
            elif type == MFnNumericData.kDouble:
                out.append(plug.asDouble())
        elif attr.hasFn(MFn.kUnitAttribute):
            type = MFnUnitAttribute(attr).unitType()
            if type == MFnUnitAttribute.kAngle:
                out.append(plug.asMAngle())
            elif type == MFnUnitAttribute.kDistance:
                out.append(plug.asMDistance())
            elif type == MFnUnitAttribute.kTime:
                out.append(plug.asMTime())
        elif attr.hasFn(MFn.kTypedAttribute):
            type = MFnTypedAttribute(attr).attrType()
            if type == MFnData.kString:
                out.append(plug.asString())
        else:
            #last resort for unimplemented data types
            out.append(plug.asMObject())
    return out

def getObjectsShadersSet(objShape=""):

    cmds.select(clear=True)
    cmds.select(objShape, r=True)

    nodes = cmds.ls(selection=True, dag=True, shapes=True)
    nodeCount = len(nodes)

    # get shading groups from shapes:
    shadingGroups = ""
    if nodeCount >= 1:
        shadingGroups = cmds.listConnections(nodes, t='shadingEngine')
    shadingGroupsCount = len(shadingGroups)

    # get the shaders:
    if shadingGroupsCount >= 1:
        shaders = cmds.ls(cmds.listConnections(shadingGroups), materials=1)
        shadersSet = set(shaders)

    return shadersSet
#     for shader in shadersSet:
#         print shader

## export objects to location
#
def exportObjectAsMbFile(location="", objectName=""):
    if objectName == "":
        MGlobal.displayWarning("No object exported!!!")
        return False

    else:
        print(objectName)
        cmds.select(objectName, replace=True)
        cmds.file(location + "/" + objectName, exportSelected=True, type="mayaBinary", constructionHistory=False, force=True)
        return True

## export objects to location
#
def exportObjectAsAssFile(location="", objectName=""):
    if objectName == "":
        MGlobal.displayWarning("No object exported!!!")
        return False

    else:
        cmds.select(objectName, r=True)
        cmds.file(location + "/" + objectName, type="mayaBinary", force=True, exportSelected=True)
        return True

## Move Object pivots to bottom centor for ajust.
#
def movePivotToBottomCenter(objectName=""):
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

## create object preview camera
def createPreviewCamera(objectName):
    cmds.camera()
    cmds.rename("preview")
    mel.eval("cameraMakeNode 2 \"\";")
    selList = cmds.ls(selection=True)
    print(selList)

    previewCam = selList[0]
    previewAim = selList[1]

    boxMin = cmds.getAttr(objectName + ".boundingBoxMin")[0]
    boxMax = cmds.getAttr(objectName + ".boundingBoxMax")[0]

    ## move aim to bbx center
    aimPos = [(boxMax[0] + boxMin[0]) / 2, (boxMax[1] + boxMin[1]) / 2, (boxMax[2] + boxMin[2]) / 2]
    print(aimPos)
    cmds.move(aimPos[0], aimPos[1], aimPos[2], previewAim)

    camPosy = boxMax[1] * 1.7
    camPosx = boxMin[0] + camPosy * 1.2
    camPosz = boxMin[2] + camPosy * 1.2
    cmds.move(camPosx, camPosy, camPosz, previewCam)

    preCamShape = cmds.listRelatives(previewCam, children=True)[0]
    cmds.lookThru(preCamShape, "perspView")

## get scene texture file names
#
def getAbsolutePathTextureFileNames():
    # get workspace dir
    workSpaceDir = cmds.workspace(query=True, rootDirectory=True)
    # get file nodes
    fileNodes = cmds.ls(type="file")
    #print(fileNodes)

    # add file name to list
    textureFiles = []
    for node in fileNodes:
        textureFile = cmds.getAttr(node + ".fileTextureName")
        #print(textureFile)

        # check file exists, add absolute path
        if not os.path.exists(textureFile):
            # workspace relative path
            if os.path.exists(workSpaceDir + textureFile):
                absTextureFile = workSpaceDir + textureFile
            # in sourceimages dir
            elif os.path.exists(workSpaceDir + "sourceimages/" + textureFile):
                absTextureFile = workSpaceDir + "sourceimages/" + textureFile
            else:
                print(textureFile, " does not exists, please check...")
                continue
        else:
            absTextureFile = textureFile
        # if not in list, add it
        if not  absTextureFile in textureFiles:
            #print(absTextureFile)
            textureFiles.append(absTextureFile)

    return textureFiles

## create file node with place2d
#
def createFileNodeWithPlace2d():
    fileNode = cmds.shadingNode("file", asTexture=True)
    place2dNode = cmds.shadingNode("place2dTexture", asUtility=True)

    cmds.connectAttr(place2dNode + ".coverage", fileNode + ".coverage", force=True)
    cmds.connectAttr(place2dNode + ".translateFrame", fileNode + ".translateFrame", force=True)
    cmds.connectAttr(place2dNode + ".rotateFrame", fileNode + ".rotateFrame", force=True)
    cmds.connectAttr(place2dNode + ".mirrorU", fileNode + ".mirrorU", force=True)
    cmds.connectAttr(place2dNode + ".mirrorV", fileNode + ".mirrorV", force=True)
    cmds.connectAttr(place2dNode + ".stagger", fileNode + ".stagger", force=True)
    cmds.connectAttr(place2dNode + ".wrapU", fileNode + ".wrapU", force=True)
    cmds.connectAttr(place2dNode + ".wrapV", fileNode + ".wrapV", force=True)
    cmds.connectAttr(place2dNode + ".repeatUV", fileNode + ".repeatUV", force=True)
    cmds.connectAttr(place2dNode + ".offset", fileNode + ".offset", force=True)
    cmds.connectAttr(place2dNode + ".rotateUV", fileNode + ".rotateUV", force=True)
    cmds.connectAttr(place2dNode + ".noiseUV", fileNode + ".noiseUV", force=True)
    cmds.connectAttr(place2dNode + ".vertexUvOne", fileNode + ".vertexUvOne", force=True)
    cmds.connectAttr(place2dNode + ".vertexUvTwo", fileNode + ".vertexUvTwo", force=True)
    cmds.connectAttr(place2dNode + ".vertexUvThree", fileNode + ".vertexUvThree", force=True)
    cmds.connectAttr(place2dNode + ".vertexCameraOne", fileNode + ".vertexCameraOne", force=True)
    cmds.connectAttr(place2dNode + ".outUV", fileNode + ".uv", force=True)
    cmds.connectAttr(place2dNode + ".outUvFilterSize", fileNode + ".uvFilterSize", force=True)

    return fileNode

## make object isolate view on
#
def makeObjectIsolateOn(objectName):
    if objectName:
        #currentView = cmds.paneLayout('viewPanes', q=True, pane1=True)
        currentView = u'modelPanel4'

        cmds.select(objectName, replace=True)
        cmds.isolateSelect(currentView, state=1)

## make object isolate view off
#
def makeObjectIsolateOff(objectName):
    if objectName:
        #currentView = cmds.paneLayout('viewPanes', q=True, pane1=True)
        currentView = u'modelPanel4'
        cmds.select(objectName, replace=True)
        cmds.isolateSelect(currentView, state=0)

## load plugin if not loaded
#
def checkAndLoadPlugin(pluginName=""):
    if not cmds.pluginInfo(pluginName, query=True, loaded=True):
        cmds.loadPlugin(pluginName)
        MGlobal.displayInfo("plugin " + pluginName + " loaded success")

def getCurrentWorkspaceDir():
    workSpaceDir = cmds.workspace(query=True, rootDirectory=True)
    return workSpaceDir

def getCurrentSceneName():
    currentSceneName = pmcore.system.sceneName().basename()[:-3]
    return currentSceneName
    pass

def split_list(iterable, size):
    it = iter(iterable)
    item = list(itertools.islice(it, size))
    while item:
        yield item
        item = list(itertools.islice(it, size))
