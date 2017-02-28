# encoding: utf-8

import os
import maya.cmds as cmds

def getObjectsShaderGroupSet(objShape=""):

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


def getAbsolutePathTextureFileList():
    """
    get scene texture file name list
    :return: texture file name list
    """
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