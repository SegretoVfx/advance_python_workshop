
# ANIM SHELF FUNCTION **************************************************************
# Description   = All the functions that are called from the anim_shelf_creator module.
# 
# File name     = anim_shelf_functions.py
# Date of birth = 2024 - 01 - 22
# 
# Author  = Juls
# Email   = segretovfx@gmail.com
# 
# Usage = This library is called from the anim_shelf_creator file. 
# 
# *********************************************************************



import maya.cmds as cmds

print("Hello from shelf functions")


def open_scene(self, *args):
    cmds.OpenScene()
    
    
    # from scripts.segretoTools import segretoEasyMotionTrail
    # importlib.reload(segretoEasyMotionTrail)
    # segretoEasyMotionTrail.main()