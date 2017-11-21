# encoding:utf-8

import  maya.cmds as cmds
import maya.mel as mel


def saveHUDVisibleStatus():
    """
    """
    head_obj_list = cmds.headsUpDisplay(listHeadsUpDisplays=True)
    hud_status_dict  = {}
    for head_obj in head_obj_list:
        status = cmds.headsUpDisplay(head_obj, visible=True, query=True)
        hud_status_dict[head_obj]=status

    return hud_status_dict

def restoreHUDVisibleStatus(hud_dict):
    """
    """
    for hud_obj, status in hud_dict.items():
        cmds.headsUpDisplay(hud_obj, visible=status, edit=True)

def saveViewportDisplayStatus():
    """
    :return status dict
    """
    persp_panel = "modelPanel4"
    
    cmds.setFocus(persp_panel)
    cmds.modelEditor(persp_panel, edit=True, activeView=True)
    
    display_status_dict = {}
    display_status_dict["rendererName"]=cmds.modelEditor(persp_panel, query=True, rendererName=True)
    display_status_dict["nurbsCurves"]=cmds.modelEditor(persp_panel, query=True, nurbsCurves=True)
    display_status_dict["nurbsSurfaces"]=cmds.modelEditor(persp_panel, query=True, nurbsSurfaces=True)
    display_status_dict["cv"]=cmds.modelEditor(persp_panel, query=True, cv=True)
    display_status_dict["hulls"]=cmds.modelEditor(persp_panel, query=True, hulls=True)
    display_status_dict["polymeshes"]=cmds.modelEditor(persp_panel, query=True, polymeshes=True)
    display_status_dict["subdivSurfaces"]=cmds.modelEditor(persp_panel, query=True, subdivSurfaces=True)
    display_status_dict["planes"]=cmds.modelEditor(persp_panel, query=True, planes=True)
    display_status_dict["lights"]=cmds.modelEditor(persp_panel, query=True, lights=True)
    display_status_dict["cameras"]=cmds.modelEditor(persp_panel, query=True, cameras=True)
    display_status_dict["imagePlane"]=cmds.modelEditor(persp_panel, query=True, imagePlane=True)
    display_status_dict["joints"]=cmds.modelEditor(persp_panel, query=True, joints=True)
    display_status_dict["ikHandles"]=cmds.modelEditor(persp_panel, query=True, ikHandles=True)
    display_status_dict["deformers"]=cmds.modelEditor(persp_panel, query=True, deformers=True)
    display_status_dict["dynamics"]=cmds.modelEditor(persp_panel, query=True, dynamics=True)
    display_status_dict["particleInstancers"]=cmds.modelEditor(persp_panel, query=True, particleInstancers=True)
    display_status_dict["fluids"]=cmds.modelEditor(persp_panel, query=True, fluids=True)
    display_status_dict["hairSystems"]=cmds.modelEditor(persp_panel, query=True, hairSystems=True)
    display_status_dict["follicles"]=cmds.modelEditor(persp_panel, query=True, follicles=True)
    display_status_dict["nCloths"]=cmds.modelEditor(persp_panel, query=True, nCloths=True)
    display_status_dict["nParticles"]=cmds.modelEditor(persp_panel, query=True, nParticles=True)
    display_status_dict["dynamicConstraints"]=cmds.modelEditor(persp_panel, query=True, dynamicConstraints=True)
    display_status_dict["locators"]=cmds.modelEditor(persp_panel, query=True, locators=True)
    display_status_dict["dimensions"]=cmds.modelEditor(persp_panel, query=True, dimensions=True)
    display_status_dict["pivots"]=cmds.modelEditor(persp_panel, query=True, pivots=True)
    display_status_dict["handles"]=cmds.modelEditor(persp_panel, query=True, handles=True)
    display_status_dict["textures"]=cmds.modelEditor(persp_panel, query=True, textures=True)
    display_status_dict["strokes"]=cmds.modelEditor(persp_panel, query=True, strokes=True)
    display_status_dict["motionTrails"]=cmds.modelEditor(persp_panel, query=True, motionTrails=True)
    display_status_dict["pluginShapes"]=cmds.modelEditor(persp_panel, query=True, pluginShapes=True)
    display_status_dict["clipGhosts"]=cmds.modelEditor(persp_panel, query=True, clipGhosts=True)
    display_status_dict["greasePencils"]=cmds.modelEditor(persp_panel, query=True, greasePencils=True)
    display_status_dict["manipulators"]=cmds.modelEditor(persp_panel, query=True, manipulators=True)
    display_status_dict["grid"]=cmds.modelEditor(persp_panel, query=True, grid=True)
    display_status_dict["hud"]=cmds.modelEditor(persp_panel, query=True, hud=True)
    display_status_dict["sel"]=cmds.modelEditor(persp_panel, query=True, sel=True)

    return display_status_dict

def restoreViewportDisplayStatus(display_status_dict):
    """
    """
    persp_panel = "modelPanel4"    
    cmds.setFocus(persp_panel)
    cmds.modelEditor(persp_panel, edit=True, activeView=True)

    cmds.modelEditor(persp_panel, edit=True, rendererName=display_status_dict["rendererName"])
    cmds.modelEditor(persp_panel, edit=True, nurbsCurves=display_status_dict["nurbsCurves"])
    cmds.modelEditor(persp_panel, edit=True, nurbsSurfaces= display_status_dict["nurbsSurfaces"])
    cmds.modelEditor(persp_panel, edit=True, cv=display_status_dict["cv"])
    cmds.modelEditor(persp_panel, edit=True, hulls=display_status_dict["hulls"])
    cmds.modelEditor(persp_panel, edit=True, polymeshes=display_status_dict["polymeshes"])
    cmds.modelEditor(persp_panel, edit=True, subdivSurfaces=display_status_dict["subdivSurfaces"])
    cmds.modelEditor(persp_panel, edit=True, planes=display_status_dict["planes"])
    cmds.modelEditor(persp_panel, edit=True, lights=display_status_dict["lights"])
    cmds.modelEditor(persp_panel, edit=True, cameras=display_status_dict["cameras"])
    cmds.modelEditor(persp_panel, edit=True, imagePlane=display_status_dict["imagePlane"])
    cmds.modelEditor(persp_panel, edit=True, joints=display_status_dict["joints"])
    cmds.modelEditor(persp_panel, edit=True, ikHandles=display_status_dict["ikHandles"])
    cmds.modelEditor(persp_panel, edit=True, deformers=display_status_dict["deformers"])
    cmds.modelEditor(persp_panel, edit=True, dynamics=display_status_dict["dynamics"])
    cmds.modelEditor(persp_panel, edit=True, particleInstancers=display_status_dict["particleInstancers"])
    cmds.modelEditor(persp_panel, edit=True, fluids=display_status_dict["fluids"])
    cmds.modelEditor(persp_panel, edit=True, hairSystems=display_status_dict["hairSystems"])
    cmds.modelEditor(persp_panel, edit=True, follicles=display_status_dict["follicles"])
    cmds.modelEditor(persp_panel, edit=True, nCloths=display_status_dict["nCloths"])
    cmds.modelEditor(persp_panel, edit=True, nParticles=display_status_dict["nParticles"])
    cmds.modelEditor(persp_panel, edit=True, dynamicConstraints=display_status_dict["dynamicConstraints"])
    cmds.modelEditor(persp_panel, edit=True, locators=display_status_dict["locators"])
    cmds.modelEditor(persp_panel, edit=True, dimensions=display_status_dict["dimensions"])
    cmds.modelEditor(persp_panel, edit=True, pivots=display_status_dict["pivots"])
    cmds.modelEditor(persp_panel, edit=True, handles=display_status_dict["handles"])
    cmds.modelEditor(persp_panel, edit=True, textures=display_status_dict["textures"])
    cmds.modelEditor(persp_panel, edit=True, strokes=display_status_dict["strokes"])
    cmds.modelEditor(persp_panel, edit=True, motionTrails=display_status_dict["motionTrails"])
    cmds.modelEditor(persp_panel, edit=True, pluginShapes=display_status_dict["pluginShapes"])
    cmds.modelEditor(persp_panel, edit=True, clipGhosts= display_status_dict["clipGhosts"])
    cmds.modelEditor(persp_panel, edit=True, greasePencils=display_status_dict["greasePencils"])
    cmds.modelEditor(persp_panel, edit=True, manipulators=display_status_dict["manipulators"])
    cmds.modelEditor(persp_panel, edit=True, grid=display_status_dict["grid"])
    cmds.modelEditor(persp_panel, edit=True, hud=display_status_dict["hud"])
    cmds.modelEditor(persp_panel, edit=True, sel=display_status_dict["sel"])


def makeObjectIsolateOn(objectName):
    """
    make object isolate view on
    :param objectName:
    :return:
    """
    if objectName:
        #currentView = cmds.paneLayout('viewPanes', q=True, pane1=True)
        currentView = u'modelPanel4'

        cmds.select(objectName, replace=True)
        cmds.isolateSelect(currentView, state=1)


def makeObjectIsolateOff(objectName):
    """
    make object isolate view off
    :param objectName:
    :return:
    """
    if objectName:
        #currentView = cmds.paneLayout('viewPanes', q=True, pane1=True)
        currentView = u'modelPanel4'
        cmds.select(objectName, replace=True)
        cmds.isolateSelect(currentView, state=0)