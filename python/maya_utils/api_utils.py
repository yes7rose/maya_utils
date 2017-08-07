# encoding:utf-8

import logging

import maya.api.OpenMaya as om

# fast convenience tests on API objects
def isValidMObjectHandle(obj):
    if isinstance(obj, om.MObjectHandle):
        return obj.isValid() and obj.isAlive()
    else:
        return False

def isValidMObject(obj):
    if isinstance(obj, om.MObject):
        return not obj.isNull()
    else:
        return False

def isValidMPlug(obj):
    if isinstance(obj, om.MPlug):
        return not obj.isNull()
    else:
        return False

def isValidMDagPath(obj):
    if isinstance(obj, om.MDagPath):
        # when the underlying MObject is no longer valid, dag.isValid() will still return true,
        # but obj.fullPathName() will be an empty string
        return obj.isValid() and obj.fullPathName()
    else:
        return False

def isValidMNode(obj):
    if isValidMObject(obj):
        return obj.hasFn(om.MFn.kDependencyNode)
    else:
        return False

def isValidMDagNode(obj):
    if isValidMObject(obj):
        return obj.hasFn(om.MFn.kDagNode)
    else:
        return False

def isValidMNodeOrPlug(obj):
    return isValidMPlug(obj) or isValidMNode(obj)

# returns a MObject for an existing node
def toMObject(nodeName):
    """ Get the API MObject given the name of an existing node """
    sel = om.MSelectionList()
    obj = om.MObject()
    result = None
    try:
        sel.add(nodeName)
        sel.getDependNode(0, obj)
        if isValidMObject(obj):
            result = obj
    except:
        pass
    return result

def toMDagPath(nodeName):
    """ Get an API MDagPAth to the node, given the name of an existing dag node """
    obj = toMObject(nodeName)
    if obj:
        dagFn = om.MFnDagNode(obj)
        dagPath = om.MDagPath()
        dagFn.getPath(dagPath)
        return dagPath


def getMObjectFromName(node_name):
    """
    """
    sel_list = om.MSelectionList()
    sel_list.add(node_name)

    m_object = None
    try:
        m_object = sel_list.getDependNode(0)

    except Exception:
        logging.error("can not get mobject")

    return m_object


def getMDagPathFromName(dag_name):
    """
    """
    sel_list = om.MSelectionList()
    sel_list.add(dag_name)

    dag_path = None
    try:
        dag_path = sel_list.getDagPath(0)

    except Exception:
        logging.error("can not get dagpath")

    return dag_path
