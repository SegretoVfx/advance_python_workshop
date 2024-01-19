# JULS ANIM SHELF ***********************************************
# Description   = Launch the process to create the juls_anim_shelf
#                 This script will be launched by the userSetup.py file
#                 located in the script folder
#
# File name     = juls_anim_shelf.py
# Date of birth = 1/10/2024
#
# Author  = Juls
# Email   = segretovfx@gmail.com
#
# Based on the script from
# https://bindpose.com/scripting-custom-shelf-in-maya-python/
# Using tones of scripts from the internet
#
# Usage = This will work only if used with this three other files:
#          juls_shelf_builder
#          juls_shelf_functions
#          juls_shelf_info
#
# *********************************************************************

import importlib

import maya.cmds as cmds


from functools import partial


import juls_shelf_functions as jfunc
import juls_shelf_builder as jbuild
import juls_shelf_info as jinfo

importlib.reload(jbuild)
importlib.reload(jfunc)
importlib.reload(jinfo)


class AnimShelf(jbuild.Builder):
    def build(self):
        ## SAVE Local
        self.add_button(
            label="",
            annotation="Open Scene UI",
            icon="juls_toolbox_shelf_open.png",
            command=partial(asf.loadSaveTool, "load"),
        )
