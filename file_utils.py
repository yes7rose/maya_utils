# encoding: utf-8

import os
import logging
import re

from maya.OpenMaya import MGlobal

import maya.cmds as cmds

def exportObjectAsMbFile(location="", objectName=""):
    if objectName == "":
        MGlobal.displayWarning("No object exported!!!")
        return False

    else:
        print(objectName)
        cmds.select(objectName, replace=True)
        cmds.file(location + "/" + objectName, exportSelected=True, type="mayaBinary", constructionHistory=False, force=True)

        return True


def getCurrentWorkspaceDir():
    workSpaceDir = cmds.workspace(query=True, rootDirectory=True)
    return workSpaceDir


def getCurrentSceneName():
    currentSceneName = pmcore.system.sceneName().basename()[:-3]
    return currentSceneName

def getNodesInReferenceFromFileName(ref_file):
    pass

def getNodesInReferenceFromRefNode(ref_node):
    pass

def getFileVersionString(file_name):
    """
    get the version string "vxxx"
    """
    version_patten = re.compile("(?<=[_\.])v\d{1,}(?=[_\.])")

    version_list = re.findall(version_patten, file_name)
    if not version_list :
        logging.warning(u"文件名不包含有version字符串:%s"%file_name)
        return None

    if len(version_list) > 1:
        logging.warning(u"文件名包含有多个version字符串:%s"%file_name)
        return None

    return version_list[0]
