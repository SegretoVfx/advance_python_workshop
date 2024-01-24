# ------------------------------------------------------------
# --- ANIM SHELF CREATOR ---
# Description   = The class to adapt for the shelf creation
#
# Date   = 2024 - 01 - 23
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage = This classe need the ShelfBuilder module to be imported.
# ------------------------------------------------------------


import Shelf_Builder
import maya.cmds as cmds
import anim_shelf_functions as animfunc

from functools import partial


class AnimShelf(Shelf_Builder.Builder):
    def build(self):
        # ------------------------------------------------------------
        # --- FILE ---

        # --- open file ---
        self.add_button(
            label="",
            annotation="Open Scene UI",
            icon="ws_shelf_open.png",
            command=animfunc.open_scene,
        )

        # --- save ---
        self.add_button(
            label="",
            annotation="Save scene",
            icon="ws_shelf_saveLocal.png",
            command=animfunc.save_scene,
        )

        # --- save as ---
        self.add_button(
            label="",
            annotation="save scene as UI",
            icon="ws_shelf_saveAs.png",
            command=animfunc.save_scene_as,
        )

        # --- save increment ---
        self.add_button(
            label="",
            annotation="Increment save scene",
            icon="ws_shelf_saveIncrement.png",
            command=animfunc.save_scene_increment,
        )

        self.add_separator()

        # ------------------------------------------------------------
        # --- TOOLS ---
        self.add_button(
            "",
            icon="ws_shelf_tools.png",
            annotation="Right-click open Scene Content UI",
        )
        #  RMB open most used option
        p = cmds.popupMenu(b=3, postMenuCommand="")
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)

        # --- WES TOOLS ---
        self.add_menu_item(
            p,
            "Wes anim tools",
            icon="",
            command=animfunc.launch_wes_tools,
        )

        # --- ACK TOOLS ---
        self.add_menu_item(
            p,
            "ack anim tools",
            icon="",
            command=animfunc.launch_ack_tools,
        )
        
        
        # --- aTOOLS ---
        self.add_menu_item(
            p,
            "aTools",
            icon="",
            command=animfunc.launch_atools,
        )
        
        # Shotgun Loader
        self.add_menu_item(
            p,
            "Shotgun Loader UI",
            icon="ws_anim_shelf_SG.png",
            command="",
        )


AnimShelf()
