# encoding: utf-8

import os
import logging
import re

import scandir

from maya.OpenMaya import MGlobal

import maya.cmds as cmds
import pymel.core as pmcore


# ====== current file =====
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
    currentSceneName = pmcore.system.sceneName().basename()
    return currentSceneName


# ===== reference file =====
def getNodesInReferenceFromFileName(ref_file):
    """   """
    if not os.path.exists(ref_file):
        logging.error(u"file not exists:%s"%ref_file)
        return None

    if not isFileReferenced(ref_file):
        logging.error("File Not referenced:%s"%ref_file)
        return None

    node_list = cmds.referenceQuery(ref_file, nodes=True)
    if not node_list:
        logging.warning("reference file has no nodes:%s"%ref_file)

    return node_list

def getNodesInReferenceFromRefNode(ref_node):
    """   """
    if not cmds.objExists(ref_node):
        logging.error("ref node not exists:%s"%ref_node)
        return None

    node_list = cmds.referenceQuery(ref_node, nodes=True)
    if not node_list:
        logging.warning("ref file has no nodes")
        return None

    return node_list

def getRefFileNameFromRefNode(ref_node):
    """   """
    if not cmds.objExists(ref_node):
        logging.error("ref node not exists:%s"%ref_node)
        return None

    ref_file_name = cmds.refereceQuery(ref_node, filename=True)
    if not ref_file_name:
        logging.error("ref node has no link file")
        return None

    return ref_file_name

def getAllReferencedFileNames():
    """
    get all file name
    """
    ref_node_list = cmds.ls(type="reference")
    if not ref_node_list:
        logging.warning("No file referenced in current scene")
        return None

    ref_file_list = []
    for ref_node in ref_node_list:
        ref_file = cmds.referenceQuery(ref_node, filename=True)
        ref_file_list.append(ref_file)

    return ref_file_list

def isFileReferenced(file_name):
    """
    check file is referenced
    """
    ref_file_list = getAllReferencedFileNames()
    if file_name in ref_file_list:
        return True
    else:
        return False

# ===== file version ======
def getFileVersionString(file_name):
    """
    get the version string "vxxx", split with _ or .
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

def getVersionFolderList(root_folder):
    """
    get the version folders under root
    """
    folder_name_list = []
    for entry in os.scandir(root_folder):
        if entry.name.startswith('v') and entry.is_dir():
            folder_name_list.append(entry.name)

    if not folder_name_list:
        logging.error("no version folders under folder:%s"%root_folder)
        return None

    ver_pattern = re.compile("v[\d]+")
    result = filter(lambda folder_name: re.match(ver_pattern, folder_name, folder_name_list))
    return result

def getLatestVersionFile(file_list):
    """   """
    if not file_list:
        logging.error(u"file list should not empty.")
        return None

    version = 0
    result_file = ""
    for file_name in file_list:
        ver_str =  getFileVersionString(file_name)
        if not ver_str:
            continue

        ver_num = int(ver_str[1:])
        if ver_num > version:
            result_file = file_name
            version = ver_num

    if not result_file:
        logging.error(u"files have no versions")
        return None
    else:
        return result_file

def getLatestVersionFolder(folder_list):
    """   """
    if not folder_list:
        logging.error("folder list should not empty")
        return None

    version = 0
    result_folder = ""
    for folder in folder_list:
        ver_num = int(folder[1:])

        if ver_num > version:
            result_folder = folder
            version = ver_num

    if not result_folder:
        logging.error("Has no version folder")
        return None
    else:
        return result_folder

#  ===== abc file =====
def getAbcFilesOfDir(dir_name):
    """
    get abc file list of the dir
    """
    if not os.path.exists(dir_name):
        logging.error(u"文件夹不存在，请检查:%s"%dir_name)
        return None

    file_list = os.listdir(dir_name)
    abcfile_list = filter(lambda f: os.path.splitext(f) == ".abc", file_list)
    if not abcfile_list:
        logging.error(u"目录下没有abc文件:%s"%dir_name)
        return None

    return abcfile_list

def refAbcFilesInDir(dir_name):
    """
    ref abc files in dir
    """

# openvdb file


