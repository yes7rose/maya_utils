#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
@version: ??
@author: 闫刚
@license: 
@contact: 7470718@qq.com
@site: http://www.cashmerepipeline.com
@software: 
@file: anim_utils.py
@time: 2017/12/11 16:13
"""

import maya.cmds as cmds

def getTimeLineStartEnd():
    """

    :return:
    """
    start_frame = cmds.playbackOptions(query=True, min = True)
    end_frame = cmds.playbackOptions(query = True, max = True) + 1

    return (start_frame, end_frame)

def getFPSUnit():
    """

    :return:
    """
    fps_unit = cmds.currentUnit( query=True, time=True)

    return fps_unit