# WORKSHOP TOOL **************************************************************
# Description   = Workshop assignment is a Python package to generate a Maya shelf providing a
# list of useful tools.
# The shelf will be recreated from scratch at every start of Maya to insure a clear and updated version of every tool.
# This shelf is created for training purpose and doesn't come with any guaranty.
# Workshop : https://www.alexanderrichtertd.com/
#
# File name     = shelfBase.py
# Date of birth = 1/19/2024
#
# Author  = Juls
# Email   = segretovfx@gmail.com
#
# Usage = It'll be autolaunched when Maya starts
#
# *********************************************************************


import maya.cmds as cmds

from os import path
from functools import partial

# Global variables
curScriptDir = path.dirname(__file__)
print("The scripts are located in : {0}".format(curScriptDir))

shelfName = "ws_anim_shelf"

# URL OF THE WIKI
ar_url = "https://www.alexanderrichtertd.com/"


def _null(*args):
    pass


class _shelf:
    """A simple class to build shelves in maya. Since the build method is empty,
    it should be extended by the derived class to build the necessary shelf elements.
    By default it creates an empty shelf called "customShelf"."""

    def __init__(self, name=shelfName, iconPath=""):
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


"""This is an example shelf."""


class customShelf(_shelf):
    def build(self):

        ## SAVE Local
        self.add_button(
            label="",
            annotation="Open Scene UI",
            icon="ws_anim_shelf_open.png",
            command="",
        )

        ## SAVE Local
        self.add_button(
            label="",
            annotation="Save scene",
            icon="ws_anim_shelf_saveLocal.png",
            command="",
        )

        ## SAVE
        self.add_button(
            label="",
            annotation="Save increment scene",
            icon="ws_anim_shelf_saveSG.png",
            command="",
        )

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


customShelf()
