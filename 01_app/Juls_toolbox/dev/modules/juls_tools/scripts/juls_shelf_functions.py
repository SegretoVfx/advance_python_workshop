# JULS ANIM SHELF FUNCTION CALL ************************************************
# Description   = ALl the functions needed for the juls_anim_tools_shelf to
# be built.
#
# File name     = juls.shelf_functions.py
# Date of birth = 1/19/2024
#
# Author  = Juls
# Email   = segretovfx@gmail.com
#
# Usage =
#
# *********************************************************************


import maya.cmds as cmds

print("Hello from shelf functions")


def open_scene(*args):
    from funclib import scene_load
