# ------------------------------------------------------------
# --- SHElF BUILDER ---
# Description = Build the shelf into Maya containing some shortcuts to my tools
#
# Date   = 2024 - 01 - 23
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage = The shelf will be launched automatically with Maya 
#         as long as Maya is open within the "advance_python_workshop"
#         environment. 
#         Use the maya.bat file to open Maya 2024 using.
# ------------------------------------------------------------


import importlib
import maya.cmds as cmds

from functools import partial

import anim_shelf_functions as animfunc
importlib.reload(animfunc)

dev_mode = True

shelf_name = "juls_anim_shelf"


def _null(*args):
    pass


class Builder:
    """A simple class to build shelves in maya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf"."""
    
    def __init__(self, name=shelf_name, iconPath=""):
        self.name = name
        
        self.iconPath = iconPath
        
        self.labelBackground = (0.2, 0, 0.5, 1)
        self.labelColour = (0, 1, 1)
        
        self.clean_old_shelf()
        cmds.setParent(self.name)
        self.build()
    
    def build(self):
        """This method should be overwritten in derived classes to actually
        build the shelf elements. Otherwise, nothing is added to the shelf."""
        pass
    
    def add_button(
            self,
            label,
            annotation,
            icon="segretoShelf.png",
            command=_null,
            doubleCommand=_null,
            enable=True,
    ):
        """Adds a shelf button with the specified label, command, double click
        command and image."""
        cmds.setParent(self.name)
        if icon:
            icon = self.iconPath + icon
        cmds.shelfButton(
            width=37,
            height=37,
            image=icon,
            l=label,
            ndp=True,
            command=command,
            dcc=doubleCommand,
            enable=enable,
            imageOverlayLabel=label,
            olb=self.labelBackground,
            olc=self.labelColour,
            annotation=annotation,
        )
    
    def add_separator(self):
        """Adds a shelf button with the specified label, command, double click
        command and image."""
        cmds.setParent(self.name)
        cmds.shelfButton(
            width=37,
            height=37,
            image="empty.png",
            l="",
            olb=self.labelBackground,
            olc=self.labelColour,
        )
    
    def add_sub_separator(self):
        """Adds separator in the menu list."""
        cmds.setParent(self.name)
        cmds.menuItem(divider=True)
    
    def add_menu_item(self, parent, label, command=_null, icon=""):
        """Adds a shelf button with the specified label, command, double click
        command and image."""
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, l=label, c=command, i=icon, tearOff=1)
    
    def _disabled_add_menu_item(self, parent, label, command=_null, icon=""):
        """Disabled menu"""
        return cmds.menuItem(p=parent, l=label, tearOff=1, enable=False)
    
    def add_sub_menu(self, parent, label, icon=None):
        """Adds a sub menu item with the specified label and icon to the
        specified parent popup menu."""
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p=parent, l=label, i=icon, subMenu=1, tearOff=1)
    
    def clean_old_shelf(self):
        """Checks if the shelf exists and empties it if it does or creates it
        if it does not."""
        if cmds.shelfLayout(self.name, ex=1):
            if cmds.shelfLayout(self.name, q=1, ca=1):
                for each in cmds.shelfLayout(self.name, q=1, ca=1):
                    cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p="ShelfLayout")


class AnimShelf(Builder):
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
        
        # ------------------------------------------------------------
        # Add separator for safety (can click on save unintentionally)
        
        self.add_separator()
        
        # ------------------------------------------------------------
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
        
        # ------------------------------------------------------------
        
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
        
        # ------------------------------------------------------------
        # --- PICKERS ---
        self.add_button(
            "",
            icon="ws_shelf_picker.png",
            annotation="Right-click for default",
        )
        #  RMB open most used option
        p = cmds.popupMenu(b=3, postMenuCommand="")
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)
        
        # --- AWE CONTROL PICKER ---
        self.add_menu_item(
            p,
            "awe control picker",
            icon="aweControlPicker.png",
            command=animfunc.launch_awe_picker,
        )
        
        # --- DW PICKER ---
        #self._disabled_add_menu_item(
        # p,
        #     "DW picker",
        #     icon="",
        #     command=animfunc.launch_dw_picker,
        # )
        
        # --- pr Selection ---
        self.add_menu_item(
            p,
            "prSelection",
            icon="shelf_prSelectionUi.bmp",
            command=animfunc.launch_pr_selection,
        )
        
        # ------------------------------------------------------------
        
        self.add_separator()
        
        # ------------------------------------------------------------
        # --- PLAYBLAST ---
        self.add_button(
            "",
            icon="ws_shelf_playblast.png",
            annotation="Right-click open Scene Content UI",
        )
        #  RMB open most used option
        p = cmds.popupMenu(b=3, postMenuCommand="")
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)
        
        # --- Playblast Camera ---
        self.add_menu_item(
            p,
            "Playblast current view",
            icon="",
            command=animfunc.launch_playblast,
        )
        
        # ------------------------------------------------------------
        
        self.add_separator()
        
        # ------------------------------------------------------------
        # --- ANIM PATH TOOL---
        self.add_button(
            label="",
            annotation="Open Anim path tool UI",
            icon="ws_shelf_animPath.png",
            command=animfunc.launch_juls_anim_path,
        )
        
        # ------------------------------------------------------------
        
        self.add_separator()
        
        # ------------------------------------------------------------
        # --- save ---
        self.add_button(
            label="",
            annotation="launch Studio Library",
            icon="studiolibrary.png",
            command=animfunc.launch_studiolib,
        )
        # ------------------------------------------------------------
        # --- SCRIPT EDITORS ---
        if dev_mode:
            self.add_separator()
            self.add_separator()
            self.add_separator()
            self.add_separator()
            self.add_separator()
            
            self.add_button(
                "",
                icon="ws_shelf_editor.png",
                annotation="link editor ports",
            )
            #  RMB open most used option
            p = cmds.popupMenu(b=3, postMenuCommand="")
            # LMB will open a sub menu
            p = cmds.popupMenu(b=1)
            
            # --- link ports with vscode ---
            self.add_menu_item(
                p,
                "open vs code ports",
                icon="vs_code_icon.png",
                command=partial(animfunc.link_editor_port, "vscode"),
            )
            
            # --- link ports with Pycharm ---
            self.add_menu_item(
                p,
                "open pycharm ports",
                icon="pycharm_icon.png",
                command=partial(animfunc.link_editor_port, "pycharm"),
            )
            
            # --- playblast in background ---
            self.add_menu_item(
                p,
                "disconnect",
                icon="disconnect.png",
                command=animfunc.disconnect_port,
            )
