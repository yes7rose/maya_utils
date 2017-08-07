# encoding:utf-8

from maya.OpenMaya import MGlobal
from maya.OpenMaya import MObject
from maya.OpenMaya import MSelectionList
from maya.OpenMaya import MFnDependencyNode
from maya.OpenMaya import MDagPath

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

