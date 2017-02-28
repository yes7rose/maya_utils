# encoding:utf-8

from maya.OpenMaya import MPlug
from maya.OpenMaya import MFnDependencyNode
from maya.OpenMaya import MFn
from maya.OpenMaya import MFnNumericData
from maya.OpenMaya import MFnNumericAttribute
from maya.OpenMaya import MFnUnitAttribute
from maya.OpenMaya import MFnTypedAttribute
from maya.OpenMaya import MFnData

import node_utils

def findMPlug(in_node, in_attribute):
    '''
    @param in_node_name: string, unique name of the node,
    meaning the full path if multiple nodes of this name exist
    @param in_attribute_name: string, attribute to find,
    should exist or you'll get errors
    '''
    node = node_utils.getNodeFromName(in_node)
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