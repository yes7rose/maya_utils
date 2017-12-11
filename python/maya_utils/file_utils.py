# encoding: utf-8

import os
import logging
import re

import scandir

from maya.OpenMaya import MGlobal

import maya.cmds as cmds
import pymel.core as pmcore

#
# ====== current file =====
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

def getCurrentWorkspaceDir():
    workSpaceDir = cmds.workspace(query=True, rootDirectory=True)
    return workSpaceDir

def getCurrentSceneName():
    currentSceneName = pmcore.system.sceneName().basename()
    return currentSceneName

def getCurrentSceneAbsPath():
    current_path = pmcore.system.sceneName()
    return current_path


#
# ===== reference file =====
#
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

def getRefNodeOfNode(node_name):
    """ """
    is_ref_node = cmds.referenceQuery(node_name, isNodeReferenced=True)
    if not is_ref_node:
        logging.error("Node is not a ref node")
        return None

    ref_node = cmds.referenceQuery( node_name, referenceNode=True)

    return ref_node


#
# ===== file version assasiated ======
#
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


def getFileNameOfVersion(file_location, version_str):
    """   """
    if not os.path.exists(file_location):
        logging.error(u"file location not exists:%s"%file_location)
        return None

    file_entrys = []
    for entry in scandir(file_location):
        if entry.is_file():
            file_entry.append(entry)

    if not file_entrys:
        logging.error(u"no files under file location:%s"%file_location)
        return None

    file_list = [entry.name for entry in file_entrys]
    for file_name in file_list:
        if version_str in file_name:
            return file_name

    logging.warn(u"no file have version:%s"%version_str)
    return None

#  ===== files of dir =====
def getFilesOfDir(dir_name, type_ext):
    """   """
    if not os._exists(dir_name):
        logging.error(u"dir not exists:%s"%dir_name)
        return None

    file_list = os.listdir(dir_name)
    result_list = filter(lambda f: f.endswith(type_ext), file_list)

    if not result_list:
        logging.warning(u"no files of type:%s under dir:%s"%(type_ext, dir_name))
        return None

    return result_list

def getAbcFilesOfDir(dir_name):
    """
    get abc file list of the dir
    """
    abc_file_list = getFilesOfDir(dir_name, 'abc')

    if not abc_file_list:
        return None

    return abc_file_list

def getMaFilesOfDir(dir_name):
    """
    get ma file list of the dir
    """
    result_list = getFilesOfDir(dir_name, 'ma')

    if not result_list:
        return None

    return result_list

def refAbcFilesInDir(dir_name):
    """
    ref abc files in dir
    """

#
#  ======file name check======
#
def isFileNameMatchPatten(file_name, patten):
    """
    check if the file name is match the patten
    """
    match= re.match(patten, file_name)

    if match:
        return True
    else:
        return False


# =====  openvdb file  =======


