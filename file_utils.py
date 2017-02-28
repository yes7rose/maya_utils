# encoding: utf-8

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