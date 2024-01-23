
# SHELF CLASS **************************************************************
# Description   = The class to adapt for the shelf creation
# 
# Date of birth = 2024-01-22
# 
# Author  = Juls
# Email   = segretovfx@gmail.com
# 
# Usage = This classe need the ShelfBuilder module to be imported.
# 
# ********************************************************************* 

import Shelf_Builder
import maya.cmds as cmds
import anim_shelf_functions as animfunc
 
from functools import partial


class AnimShelf(Shelf_Builder.Builder):
    def build(self):

        ## SAVE Local
        self.add_button(
            label="",
            annotation="Open Scene UI",
            icon="ws_anim_shelf_open.png",
            command="self.animfunc.open_scene",
        )

        ## SAVE Local
        self.add_button(
            label="",
            annotation="Save scene",
            icon="ws_anim_shelf_saveLocal.png",
            command="",
        )

        ## SAVE
        # self.add_button(
        #     label="",
        #     annotation="Save increment scene",
        #     icon="ws_anim_shelf_saveSG.png",
        #     command="",
        # )

        ## LOAD
        self.add_button(
            "",
            icon="ws_anim_shelf_import.png",
            annotation="Right-click open Scene Content UI",
        )
        #  RMB open most used option
        p = cmds.popupMenu(b=3, postMenuCommand="")
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)
        # Scene content
        self.add_menu_item(p, "Scene Content UI", icon="", command="")
        # asset loader
        self.add_menu_item(p, "Asset Loader", icon="", command="")
        # Cache loader
        self.add_menu_item(p, "Cache Loader UI", icon="", command="")
        # Shotgun Loader
        self.add_menu_item(
            p,
            "Shotgun Loader UI",
            icon="ws_anim_shelf_SG.png",
            command="",
        )

        self.add_sub_separator()

        # update all reference in the scene
        self.add_menu_item(p, "Update All Referenced Assets", icon="", command="")


AnimShelf()