"""
aniamtionShelf.py


Description:
animation shelf generator
This script will be launched by the userSetup.py file 
located in the same script folder

How To:

    
Author:
Julien Segreto 

Based on the script from 
https://bindpose.com/scripting-custom-shelf-in-maya-python/ 

Release:
Feb 2022
"""
import sys
import os
from os import walk, path
import maya.cmds as cmds
from functools import partial
import importlib

# Global variables
curScriptDir = path.dirname(__file__)
print("The scripts are located in : {0}".format(curScriptDir))

shelfName = "juls_tools"
extraButton = True
# Loading script files for tester
import j_animShelfFunctions as asf

importlib.reload(asf)


# URL OF THE WIKI
wiki_url = "https://wiki.pixomondo.com/departments/animation/shelf"
hotkey_url = "https://wiki.pixomondo.com/en/departments/animation/internal_tools/pxographeditortools"
# hotkey_url    = 'https://wiki.pixomondo.com/en/workflows/animation/animation-tools/PXOGraphEditorTools'
ml_tools_url = "http://morganloomis.com/tools/"
ack_tools_url = "http://aaronkoressel.com/index.php?nav=tools"


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
        icon="defaultIconTest.png",
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


###################################################################################
"""ANIMATION SHELF GENERATOR"""


class customShelf(_shelf):
    def build(self):
        ## SAVE Local
        self.add_button(
            label="",
            annotation="Open Scene UI",
            icon="juls_toolbox_shelf_open.png",
            command=partial(asf.loadSaveTool, "load"),
        )

        ## SAVE Local
        self.add_button(
            label="",
            annotation="Save scene",
            icon="juls_toolbox_shelf_saveLocal.png",
            command=asf.loadDefaultSave,
        )

        ## SAVE
        self.add_button(
            label="",
            annotation="Save increment scene",
            icon="juls_toolbox_shelf_saveSG.png",
            command=partial(asf.loadSaveTool, "save"),
        )

        ## LOAD
        self.add_button(
            "",
            icon="juls_toolbox_shelf_import.png",
            annotation="Right-click open Scene Content UI",
        )
        #  RMB open most used option
        p = cmds.popupMenu(b=3, postMenuCommand=partial(asf.loadSaveTool, "content"))
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)
        # Scene content
        self.add_menu_item(
            p, "Scene Content UI", icon="", command=partial(asf.loadSaveTool, "content")
        )
        # asset loader
        self.add_menu_item(
            p, "Asset Loader", icon="", command=partial(asf.loadSaveTool, "asset")
        )
        # Cache loader
        self.add_menu_item(p, "Cache Loader UI", icon="", command=asf.loadCacheUI)
        # Shotgun Loader
        self.add_menu_item(
            p,
            "Shotgun Loader UI",
            icon="juls_toolbox_shelf_SG.png",
            command=asf.loadSGCacheUI,
        )

        self.add_sub_separator()

        # update all reference in the scene
        self.add_menu_item(
            p, "Update All Referenced Assets", icon="", command=asf.updateAllReference
        )

        ## LOAD
        self.add_button(
            "", icon="copy2clipBoard.png", annotation="Right-click open Shot folder"
        )
        #  RMB open most used option
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(asf.open_shot_folder, "content")
        )
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)
        # Scene content
        self.add_menu_item(
            p,
            "open Shot folder",
            icon="",
            command=partial(asf.open_shot_folder, "content"),
        )
        # asset loader
        self.add_menu_item(
            p,
            "open Shot images folder",
            icon="",
            command=partial(asf.open_shot_images_folder, "asset"),
        )

        self.add_separator()

        ## PIXO SHOTGUN
        ## SHOTGUN EDIT
        self.add_button(
            "",
            icon="juls_toolbox_shelf_SGedit.png",
            annotation="Right-click Set timeline to work range",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=partial(asf.loadsetFrameRange, "shot"))
        p = cmds.popupMenu(b=1)
        # set Maya framerange to shot range (from shotgun)
        self.add_menu_item(
            p,
            "Set timeline to work range",
            icon="",
            command=partial(asf.loadsetFrameRange, "shot"),
        )
        # set Maya framerange to cut range (from shotgun)
        self.add_menu_item(
            p,
            "Set timeline to cut range",
            icon="",
            command=partial(asf.loadsetFrameRange, "cut"),
        )

        self.add_sub_separator()

        # set Maya scene resolution (from shotgun)
        self.add_menu_item(
            p,
            "Set Camera resolution from Shotgun",
            icon="",
            command=asf.setResolutionFromSG,
        )

        ## SHOTGUN INFO
        self.add_button(
            "",
            icon="juls_toolbox_shelf_SGinfo.png",
            annotation="Right-click open Shotgun",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadSGOpen)
        p = cmds.popupMenu(b=1)

        # open task
        self.add_menu_item(
            p, "open Shotgun on task", icon="", command=partial(asf.loadSGOpen, "task")
        )
        # open Shot
        self.add_menu_item(
            p, "open Shotgun on Shot", icon="", command=partial(asf.loadSGOpen, "shot")
        )
        # open sequence
        self.add_menu_item(
            p,
            "open Shotgun on Sequence",
            icon="",
            command=partial(asf.loadSGOpen, "sequence"),
        )
        # open project
        self.add_menu_item(
            p,
            "open Shotgun on Project",
            icon="",
            command=partial(asf.loadSGOpen, "project"),
        )

        self.add_sub_separator()

        # open shotgun panel
        self.add_menu_item(p, "open Shotgun panel", icon="", command=asf.loadSGPanel)

        self.add_sub_separator()

        # Open SG Notes
        self.add_menu_item(p, "Shot Notes", icon="", command=asf.loadSGShotNotes)

        ## SHOTGUN
        self.add_button(
            "",
            icon="juls_toolbox_shelf_SGexchange.png",
            annotation="Right-click change shot context",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadChangeContext)
        p = cmds.popupMenu(b=1)
        # Shotgun loader
        self.add_menu_item(
            p, "Change Shot Context", icon="", command=asf.loadChangeContext
        )
        self.add_menu_item(p, "Display Shot Context", icon="", command=asf.loadContext)
        self.add_menu_item(
            p,
            "Shotgun Loader UI",
            icon="juls_toolbox_shelf_SG.png",
            command=asf.loadSGCacheUI,
        )

        self.add_separator()

        ## PLAYBLAST / PUBLISH TOOLS
        ## PLAYBLAST
        self.add_button(
            "",
            icon="juls_toolbox_shelf_playblast.png",
            annotation="Right-click open PXO Playblast UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadPlayblastUi)
        p = cmds.popupMenu(b=1)
        # playblast UI
        self.add_menu_item(p, "PXO Playblast UI", icon="", command=asf.loadPlayblastUi)
        # pxo playblast
        self.add_menu_item(p, "PXO Playblast", icon="", command=asf.loadPlayblast)
        # playblast witness cam
        self.add_menu_item(
            p, "PXO Witness Playblast", icon="", command=asf.loadPlayblastWitness
        )

        # ## RV
        # self.add_button("", icon = "pxoanim_shelf_RV.png",
        #                 annotation = "Right-click open Last Payblast", )
        # p = cmds.popupMenu(b = 3, postMenuCommand = 'print("Open Last playblast")')
        # p = cmds.popupMenu(b = 1)
        # # Open last playblast
        # self._disabled_add_menu_item(p, "Open last playblast",
        #                    icon = "",
        #                    command = 'print("Open Last playblast")')
        # # Open RV
        # self._disabled_add_menu_item(p, "Launch RV",
        #                    icon = "",
        #                    command = 'print("Open RV")')

        # ## EDIT MODE
        # self.add_button("", icon = "pxoanim_shelf_edit.png",
        #                 annotation = "Right-click load in-context imageplanes to cut range")
        # p = cmds.popupMenu(b = 3, postMenuCommand = 'print("To be done")')
        # p = cmds.popupMenu(b = 1)
        # # Load imageplane in context
        # self._disabled_add_menu_item(p, "Load in-context imageplane to cut range",
        #                    icon = "",
        #                    command = "")
        # # Load imageplane in context
        # self._disabled_add_menu_item(p, "Load in-context imageplane to cut range - pre/post to shot range",
        #                    icon = "",
        #                    command = "")
        # # Load imageplane in context
        # self._disabled_add_menu_item(p, "Load in-context imageplane to shot range - pre/post to cut range",
        #                    icon = "",
        #                    command = "")

        ## PUBLISH
        self.add_button(
            "",
            icon="juls_toolbox_shelf_publish.png",
            annotation="Right-click Deadline Anim Publish UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.legacy_loadDeadlinePublish)
        p = cmds.popupMenu(b=1)
        # Open Deadline Publish UI
        self.add_menu_item(
            p,
            "Deadline anim publish UI (legacy)",
            icon="",
            command=asf.legacy_loadDeadlinePublish,
        )
        # Open Local Publish UI
        self.add_menu_item(
            p,
            "Local anim publish UI (legacy)",
            icon="",
            command=asf.legacy_loadLocalPublish,
        )

        self.add_sub_separator()

        # Open Deadline Publish UI
        self.add_menu_item(
            p, "Deadline pyblish UI", icon="", command=asf.deadline_pyblish
        )
        # Open Local Publish UI
        self.add_menu_item(p, "Local publish UI", icon="", command=asf.local_pyblish)

        self.add_sub_separator()

        # Open Camera Publish UI
        self.add_menu_item(
            p, "Custom camera publish UI", icon="", command=asf.loadCameraPublish
        )

        self.add_sub_separator()

        # Open Camera Publish UI
        self.add_menu_item(
            p, "Tag list editor UI", icon="", command=asf.open_tag_manager
        )

        self.add_separator()

        # ## SCENE SETUP TOOLS
        # ## PIXO TOOLS
        # self.add_button("", icon = "pxoanim_shelf_pxo.png",
        #                 annotation = "Right-click enable Graph Editor Hot Keys")
        # p = cmds.popupMenu(b = 3, postMenuCommand = "")
        # p = cmds.popupMenu(b = 1)
        # # Graph Editor Hot Keys
        # self.add_menu_item(p, "Enable Graph Editor Hot Keys -- Manual",
        #                    icon = "",
        #                    command = partial(asf.openWebBrowser, hotkey_url))
        # # Hot Box Menu
        # self._disabled_add_menu_item(p, "Enable Hot Box (space bar) Menu",
        #                    icon = "",
        #                    command = "")
        # self.add_sub_separator()

        # # Load Huumand standard reference
        # self.add_menu_item(p, "Create PXO Standard Man",
        #                    icon = "",
        #                    command = asf.importReferenceStandardMan)

        # # Remove Huumand standard reference
        # self.add_menu_item(p, "Remove PXO Standard Man",
        #                    icon = "",
        #                    command = asf.removeReferenceStandardMan)

        # self.add_sub_separator()

        ## CAMERA TOOLS
        self.add_button(
            "",
            icon="juls_toolbox_shelf_cam.png",
            annotation="Right-click Creates followCam on selected node (point Contraint)",
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(asf.createObserverCamera, "cam")
        )
        p = cmds.popupMenu(b=1)
        # creates follow camera on selected node
        self.add_menu_item(
            p,
            "Create followCam on selected (point Contraint)",
            icon="",
            command=partial(asf.createObserverCamera, "cam"),
        )
        # creates follow camera UI
        self.add_menu_item(
            p,
            "Create followCam UI",
            icon="",
            command=partial(asf.createObserverCamera, "UI"),
        )

        self.add_sub_separator()

        # creates Witness cam
        self.add_menu_item(
            p,
            "Create WitnessCam on selected (persp)",
            icon="",
            command=partial(asf.loadSegretoCreateWitnessCamUI, "Persp"),
        )
        # open Witness cam UI
        self.add_menu_item(
            p,
            "Create WitnessCam UI",
            icon="",
            command=asf.loadSegretoCreateWitnessCamUI,
        )

        self.add_sub_separator()

        # Print annotation on screen
        self.add_menu_item(
            p,
            "Display channel HUD",
            icon="",
            command=partial(asf.loadAnnotationUI, "show"),
        )
        # Print annotation on screen
        self.add_menu_item(
            p,
            "delete channel HUD",
            icon="",
            command=partial(asf.loadAnnotationUI, "delete"),
        )

        self.add_sub_separator()

        # # open Multi-view UI
        # self._disabled_add_menu_item(p, "Multi-view UI",
        #                    icon = "",
        #                    command = '')
        # Fix perspactive
        self.add_menu_item(p, "Fix perspective", icon="", command=asf.loadFixPersp)
        # Bake camera UI
        self.add_menu_item(p, "Bake camera UI", icon="", command=asf.loadBakeCamera)

        ## IMAGE PLANE
        self.add_button(
            "",
            icon="juls_toolbox_shelf_imageplane.png",
            annotation="Right-click Cache and Play",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadCacheNplay)
        p = cmds.popupMenu(b=1)
        # Cache the scene and play realtime
        self.add_menu_item(p, "Cache and Play", icon="", command=asf.loadCacheNplay)
        # Image plane helper
        self.add_menu_item(
            p, "Image Plane Tool UI", icon="", command=asf.loadImagePlaneHelper
        )

        ## HOLD OUT
        self.add_button(
            "",
            icon="juls_toolbox_shelf_holdout.png",
            annotation="Right-click Create holdout useBackground",
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(asf.loadHoldoutCreator, "useBackground")
        )
        p = cmds.popupMenu(b=1)
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Create holdout useBackground",
            icon="",
            command=partial(asf.loadHoldoutCreator, "useBackground"),
        )
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Create holdout Grey lambert",
            icon="",
            command=partial(asf.loadHoldoutCreator, "lambert"),
        )
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Create holdout Black surfaceShader",
            icon="",
            command=partial(asf.loadHoldoutCreator, "surfaceShader"),
        )
        self.add_sub_separator()
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Revert to default Shader lambert1",
            icon="",
            command=partial(asf.loadHoldoutCreator, "default"),
        )
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Select holdout geometry",
            icon="",
            command='cmds.hyperShade( objects= "shd_*" )',
        )

        ## SCENE MAINTENANCE
        self.add_button(
            "",
            icon="juls_toolbox_shelf_maintenance.png",
            annotation="Right-click open Outliner Color manager UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadOutlinerColorManager)
        p = cmds.popupMenu(b=1)
        # Outliner Color Manager
        self.add_menu_item(
            p,
            "Outliner Color Manager UI",
            icon="",
            command=asf.loadOutlinerColorManager,
        )
        # segreto Create Display Layers
        self.add_menu_item(
            p, "Create Display layer", icon="", command=asf.loadDisplayLayerCreator
        )
        # Channel box enhancer
        self.add_menu_item(
            p, "Install Channel Box Plus", icon="", command=asf.loadChannelBoxPlus
        )

        # ## FIX
        # self.add_button("", icon = "pxoanim_shelf_fix.png",
        #                 annotation = "Right-click clean keyframes on not allowed nodes")
        # p = cmds.popupMenu(b = 3, postMenuCommand = '')
        # p = cmds.popupMenu(b = 1)
        # # clean key frames on not allowed nodes
        # self._disabled_add_menu_item(p, "clean keyframes on not allowed nodes",
        #                    icon = "",
        #                    command = 'print("CLEAN FIXtool")')
        # # clean non-rig contraints
        # self._disabled_add_menu_item(p, "fix gpu cache",
        #                    icon = "",
        #                    command = 'print("CLEAN FIXtool")')

        self.add_separator()

        ## ANIMSCHOOL PICKER

        self.add_button(
            label="",
            annotation="Launch Animschool Picker",
            icon="juls_toolbox_shelf_picker.png",
            command=partial(asf.loadAnimSchoolPicker),
        )

        ## LIBRARY
        self.add_button(
            "",
            icon="juls_toolbox_shelf_library.png",
            annotation="Right-click open Studio Library UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadStudioLibrary)
        p = cmds.popupMenu(b=1)
        # studio library
        self.add_menu_item(
            p,
            "Studio Library UI",
            icon="studioLibrary.png",
            command=asf.loadStudioLibrary,
        )
        # loadPose2Shelf
        self.add_menu_item(
            p, "pose2Shelf", icon="pose2Shelf.png", command=asf.loadPose2Shelf
        )
        # # pose grabber
        # self._disabled_add_menu_item(p, "PXO Pose Grabber UI",
        #                    icon = "",
        #                    command = '')
        # # Anim Curve Loader
        # self._disabled_add_menu_item(p, "PXO Animation Curve Loader UI",
        #                    icon = "",
        #                    command = '')

        ## TOOLS
        ## RIGS
        self.add_button(
            "",
            icon="juls_toolbox_shelf_rigs.png",
            annotation="Right-click toggles All/Selected rigs resolution",
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(asf.loadSwitchResolution, "tog")
        )
        p = cmds.popupMenu(b=1)
        # Geo to switch Res
        self.add_menu_item(
            p,
            "Toggle All/Selected rigs resolution",
            icon="",
            command=partial(asf.loadSwitchResolution, "tog"),
        )
        # Geo to High Res
        self.add_menu_item(
            p,
            "All/Selected rigs to High resolution",
            icon="juls_toolbox_shelf_rigs_lowtohigh.png",
            command=partial(asf.loadSwitchResolution, "high"),
        )
        # Geo to Low Res
        self.add_menu_item(
            p,
            "All/Selected rigs to Low resolution",
            icon="juls_toolbox_shelf_rigs_hightolow.png",
            command=partial(asf.loadSwitchResolution, "low"),
        )

        self.add_sub_separator()

        # Reset Selected
        self.add_menu_item(
            p,
            "reset selected controllers",
            icon="",
            command=partial(asf.loadSegretoResetAttr, "ctrl", False),
        )
        # Reset asset
        self.add_menu_item(
            p,
            "reset selected asset",
            icon="",
            command=partial(asf.loadSegretoResetAttr, "asset", False),
        )
        # Reset scene
        self.add_menu_item(
            p,
            "reset all scene",
            icon="",
            command=partial(asf.loadSegretoResetAttr, "scene", False),
        )

        self.add_sub_separator()

        # killl anim Selected
        self.add_menu_item(
            p,
            "kill animation selected controllers",
            icon="",
            command=partial(asf.loadSegretoResetAttr, "ctrl", True),
        )
        # killl anim  asset
        self.add_menu_item(
            p,
            "kill animation selected asset",
            icon="",
            command=partial(asf.loadSegretoResetAttr, "asset", True),
        )

        self.add_sub_separator()

        # Enabling pick walking
        self.add_menu_item(
            p,
            "Enable Pick Walking",
            icon="juls_toolbox_shelf_rigs_pickwalking.png",
            command=asf.loadPickWalking,
        )
        # Mocap
        self.add_menu_item(
            p,
            "Launch Mocap Setup",
            icon="juls_toolbox_shelf_mocap.png",
            command=asf.loadMoCapsetup,
        )

        self.add_separator()

        ## TOOLSETS
        self.add_button(
            "",
            icon="juls_toolbox_shelf_tools.png",
            annotation="Right-click open ack tools",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadAckTool)
        p = cmds.popupMenu(b=1)

        # Morgan Loomis Sub menus list
        sub = self.add_sub_menu(p, "Morgan Loomis Tools", icon="ml_default.png")
        mypath = "{0}/scripts/ml_toolbox_menu".format(curScriptDir)
        # lstScripts = cmds.getFileList( folder=mypath, filespec= '*.py' )
        # lstScripts.remove('ml_utilities.py')
        # lstScripts.remove('__init__.py')
        # ''' Menu generator '''
        # for script in lstScripts:
        #     sname = script.split(".")[0]
        #     icoName = '{1}.png'.format(curScriptDir, sname)
        #     self.add_menu_item(sub, sname,
        #                        icon =icoName,
        #                        command = partial(asf.loadMlTool, sname))

        # Aaron Koressel Tools menu
        self.add_menu_item(
            p, "Aaron Koressel tools UI", icon="", command=asf.loadAckTool
        )

        # Wesley Chandler Tools
        self.add_menu_item(
            p, "Wesley Chandler Tools UI", icon="", command=asf.loadWesleyTool
        )

        # add sub_separator
        cmds.menuItem(p=p, divider=True)

        # Toolset
        self.add_menu_item(p, "PXO_toolset", icon="", command=asf.loadToolSet)

        # # animbot
        # self._disabled_add_menu_item(p, "Animbot UI",
        #                    icon = "",
        #                    command = "")
        # # aTool
        # self.add_menu_item(p, "aTool UI",
        #                    icon = "animbot.png",
        #                    command = asf.loadATool)

        # add sub_separator
        cmds.menuItem(p=p, divider=True)

        # Aaron Koressel Tools menu
        self.add_menu_item(
            p,
            "Aaron Koressel tools Manual",
            icon="",
            command=partial(asf.openWebBrowser, ack_tools_url),
        )

        # Morgan Loomis menu
        self.add_menu_item(
            p,
            "Morgan Loomis tools Manual",
            icon="",
            command=partial(asf.openWebBrowser, ml_tools_url),
        )

        # bh Ghost
        self.add_menu_item(p, "bhGhost UI", icon="bhGhost.png", command=asf.loadBhGhost)
        # Create Annotation
        self.add_menu_item(
            p, "Create annotation UI", icon="", command=asf.loadCreateAnnotateNode
        )

        self.add_sub_separator()

        # bh speed
        self.add_menu_item(p, "bhSpeed UI", icon="bhSpeed.png", command=asf.loadBhSpeed)
        # Smear
        self.add_menu_item(p, "boSmear UI", icon="", command=asf.loadBoSmear)

        ## Selector
        self.add_button(
            "",
            icon="juls_toolbox_shelf_select.png",
            annotation="Right-click selects all Keyed Controllers",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadSelectAllKeyed)
        p = cmds.popupMenu(b=1)
        # Select all Keyed controllers
        self.add_menu_item(
            p,
            "Select all Keyed controllers (scene / selected asset)",
            icon="",
            command=asf.loadSelectAllKeyed,
        )

        self.add_sub_separator()

        # Select all controllers (current selection or all asset)
        self.add_menu_item(
            p,
            "Select all Controllers (scene / selected asset)",
            icon="",
            command=partial(asf.loadSelectAll, "ctrl"),
        )

        # Select geo
        self.add_menu_item(
            p,
            "Select all Geometries (scene / selected asset)",
            icon="",
            command=partial(asf.loadSelectAll, "geo"),
        )

        # # Select geo
        # self.add_menu_item(p, "Select all Cameras (scene / selected asset)",
        #                    icon = "",
        #                    command = partial(asf.loadSelectAll, 'cam'))

        # # Select geo
        # self.add_menu_item(p, "Select all curves (scene / selected asset)",
        #                    icon = "",
        #                    command = partial(asf.loadSelectAll, 'crv'))

        # Select contraint
        self._disabled_add_menu_item(
            p, "Select Constraint", icon="", command=asf.loadSelectConstraint
        )

        self.add_sub_separator()

        # Find sub frames
        self._disabled_add_menu_item(
            p, "Find subframe", icon="", command='print("Find something tool")'
        )
        # Find textures
        self._disabled_add_menu_item(
            p, "Finde textures", icon="", command='print("Find something tool")'
        )
        # Find selected node's Parent
        self._disabled_add_menu_item(
            p,
            "Find parent of selected node",
            icon="",
            command='print("Find something tool")',
        )
        # Find love
        # self.add_menu_item(p, "Find Love",
        #                    icon = "",
        #                    command = '\n\nprint("I LOVE YOU {0}")'.format(os.getenv('username').replace(".", " ")))

        self.add_separator()

        ## COPY ANIM
        # mode: str, selection mode for pasting ->>
        #        "insert", "replace", "replaceCompletely", "merge",
        #        "scaleInsert," "scaleReplace", "scaleMerge",
        #        "fitInsert", "fitReplace", "fitMerge"
        self.add_button(
            "",
            icon="juls_toolbox_shelf_copy.png",
            annotation="Right-click copy all animation (A -> B)",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.segreto_anim_utils)
        p = cmds.popupMenu(b=1)
        # copies animation from first selected node to second, including attribute channels
        self.add_menu_item(
            p, "Copy anim (A -> B)", icon="", command=asf.segreto_anim_utils
        )
        # all Translation
        self._disabled_add_menu_item(
            p,
            "Copy translation anim (A -> B)",
            icon="",
            command=partial(asf.segreto_anim_utils, attribute=["tx", "ty", "tz"]),
        )
        # all rotation
        self._disabled_add_menu_item(
            p,
            "Copy rotation anim (A -> B)",
            icon="",
            command=partial(asf.segreto_anim_utils, attribute=["rx", "ry", "rz"]),
        )
        # copy anim UI
        # self._disabled_add_menu_item(p, "Copy anim UI",
        #                    icon = "",
        #                    command = 'print("copy anim tool")')

        ## MIRROR ANIMATION UI
        self.add_button(
            "",
            icon="juls_toolbox_shelf_mirror.png",
            annotation="Right-click open Mirror Animation tools UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadStudioLibrary)
        p = cmds.popupMenu(b=1)
        # Mirror animation with Studio Library
        self.add_menu_item(
            p,
            "Studio Library UI",
            icon="studioLibrary.png",
            command=asf.loadStudioLibrary,
        )
        #  Mirror animation with PXO UI
        self._disabled_add_menu_item(
            p, "Mirror Animation tools UI", icon="", command=asf.loadStudioLibrary
        )

        ## WALK HELPER
        self.add_button(
            "",
            icon="juls_toolbox_shelf_walkhelper.png",
            annotation="Right-click launches Sticky feet",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadStickyFeet)
        p = cmds.popupMenu(b=1)
        # Walk helper tool
        self.add_menu_item(p, "Sticky feet", icon="", command=asf.loadStickyFeet)
        # Path node
        self._disabled_add_menu_item(
            p, "Path Tool", icon="", command='print("walk helper Tool")'
        )
        # Walk helper IU
        self._disabled_add_menu_item(
            p, "Walk Cycle Helper UI", icon="", command='print("walk helper Tool")'
        )

        self.add_separator()

        ## SNAP
        self.add_button(
            "",
            icon="juls_toolbox_shelf_snap.png",
            annotation="Right-click snap all channels",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.snap_parent)
        p = cmds.popupMenu(b=1)

        # snap all
        self.add_menu_item(p, "Snap all channels", icon="", command=asf.snap_parent)
        # snap translation only
        self.add_menu_item(p, "Snap Translation", icon="", command=asf.snap_translate)
        # snap rotation only
        self.add_menu_item(p, "Snap Rotation", icon="", command=asf.snap_rotate)

        self.add_sub_separator()

        # Snap tool UI
        self.add_menu_item(
            p,
            "Snap tool UI",
            icon="juls_toolbox_shelf_snap.png",
            command=asf.loadAlignTool,
        )
        # animSnap
        self.add_menu_item(p, "animSnap UI", icon="", command=asf.loadAnimSnap)
        # Match Placement
        self.add_menu_item(
            p, "Match Placement UI", icon="", command=asf.loadGbMatchPlacement
        )

        # snap Selected channels
        # self._disabled_add_menu_item(p, "Snap selected channels",
        #                    icon = "",
        #                    command = 'print("Snap tool")')

        ## Constraint UI
        self.add_button(
            label="",
            icon="juls_toolbox_shelf_constraint.png",
            annotation="Right-click open Easy Constraint UI",
            command=asf.loadEasyParentUI,
        )
        p = cmds.popupMenu(b=3, postMenuCommand=partial(asf.loadEasyParentUI, "UI", ""))
        p = cmds.popupMenu(b=1)
        # Constraint UI
        self.add_menu_item(
            p,
            "Easy Constraint UI",
            icon="",
            command=partial(asf.loadEasyParentUI, "UI", ""),
        )
        self.add_sub_separator()
        # parent constraint with offset
        self.add_menu_item(
            p,
            "parent constraint offset",
            icon="",
            command=partial(asf.loadEasyParentUI, "parenting", True),
        )
        # parent constraint without offset
        self.add_menu_item(
            p,
            "parent constraint snap",
            icon="",
            command=partial(asf.loadEasyParentUI, "parenting", False),
        )
        # orientation constraint with offset
        self.add_menu_item(
            p,
            "orientation constraint offset",
            icon="",
            command=partial(asf.loadEasyParentUI, "orienting", True),
        )
        # orientation constraint without offset
        self.add_menu_item(
            p,
            "orientation constraint snap",
            icon="",
            command=partial(asf.loadEasyParentUI, "orienting", False),
        )
        # point (selected nodes to Specific Point on Geo with offset)
        self.add_menu_item(
            p,
            "point constraint offset",
            icon="",
            command=partial(asf.loadEasyParentUI, "pointing", True),
        )
        # point (selected nodes to specific Point on geo without offset)
        self.add_menu_item(
            p,
            "point constraint snap",
            icon="",
            command=partial(asf.loadEasyParentUI, "pointing", False),
        )
        # Rivet (with offset)
        self.add_menu_item(
            p,
            "Rivet offset",
            icon="",
            command=partial(asf.loadEasyParentUI, "rivet", True),
        )
        # point (snap)
        self.add_menu_item(
            p,
            "Rivet snap",
            icon="",
            command=partial(asf.loadEasyParentUI, "rivet", False),
        )

        self.add_sub_separator()

        # unparenting
        self.add_menu_item(
            p,
            "kill constraint (selected objects)",
            icon="",
            command=partial(asf.loadEasyParentUI, "unparenting", ""),
        )
        # unparenting
        self.add_menu_item(
            p,
            "kill constraint (all scene)",
            icon="",
            command=partial(asf.loadEasyParentUI, "killConst", ""),
        )
        # bakeAnim
        self.add_menu_item(
            p,
            "bake Anim and delete constraint",
            icon="",
            command=partial(asf.loadEasyParentUI, "bakeAnim", ""),
        )

        ## Space switch
        self.add_button(
            "",
            icon="juls_toolbox_shelf_spaceswitch.png",
            annotation="Right-click open segretoLocinate",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadLocinate)
        p = cmds.popupMenu(b=1)
        # Locinate made by Julien Segreto
        self.add_menu_item(
            p, "segretoLocinate", icon="locator.png", command=asf.loadLocinate
        )
        # open morgan Loomis world bakerUI
        self.add_menu_item(
            p, "ml_world Bake", icon="ml_worldBake.png", command=asf.loadWorldBaker
        )

        self.add_sub_separator()

        # open morgan Loomis rotation order UI
        self.add_menu_item(
            p,
            "ml_convert Rotation Order",
            icon="ml_convertRotationOrder.png",
            command=asf.loadRotationOrderSwitch,
        )

        ## IK/FK switch
        # self.add_button("", icon = "pxoanim_shelf_IKFKswitch.png",
        #                 annotation = "Right-click switch IK/FK on current frame")
        # p = cmds.popupMenu(b = 3, postMenuCommand = partial(asf.loadIkFkSwitch, 'one'))
        # p = cmds.popupMenu(b = 1)
        # # switch IKFK on current frame and set a key
        # self._disabled_add_menu_item(p, "IK/FK switch on current frame",
        #                    icon = "",
        #                    command = partial(asf.loadIkFkSwitch, 'one'))
        # # switch IKFK on current frame without setting a key
        # self._disabled_add_menu_item(p, "IK/FK switch on current frame (unkeyed)",
        #                    icon = "",
        #                    command = partial(asf.loadIkFkSwitch, 'unkeyed'))
        # # switch IKFK on all frame range animation - Smart Bake
        # self._disabled_add_menu_item(p, "IK/FK switch all animation (smart)",
        #                    icon = "",
        #                    command = partial(asf.loadIkFkSwitch, 'smart'))
        # # switch IKFK on all frame range animation - Bake Every frame
        # self._disabled_add_menu_item(p, "IK/FK switch all animation",
        #                    icon = "",
        #                    command = partial(asf.loadIkFkSwitch, 'all'))

        ## EDIT ANIM CURVE UI
        self.add_button(
            "",
            icon="juls_toolbox_shelf_curve.png",
            annotation="Right-click open Segreto_Shift Keys UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadSegretoShiftKeyUI)
        p = cmds.popupMenu(b=1)
        # Shift Keys
        self.add_menu_item(
            p, "Segreto_Shift Keys UI", icon="", command=asf.loadSegretoShiftKeyUI
        )

        self.add_sub_separator()

        # Keyframe reduction UI
        self.add_menu_item(
            p,
            "Keyframe Reduction UI",
            icon="keyframeReduction.png",
            command=asf.loadKeyframeReduction,
        )
        # clean redundant keys
        self.add_menu_item(
            p, "ackDeleteRedundantKeys ", icon="", command=asf.loadAckDeleteRedundant
        )

        self.add_sub_separator()

        # Tween machine
        self.add_menu_item(
            p, "Tween Machine UI", icon="tweenMachine.png", command=asf.loadTweenMachine
        )

        # Scale anim curve
        self.add_menu_item(
            p, "np_curve Local Scale UI", icon="", command=asf.loadNP_curveLocalScale
        )

        # Smooth anim curve
        self.add_menu_item(p, "KTL_smooth Key", icon="", command=asf.loadKTL_smoothKey)
        # Smooth Key
        self.add_menu_item(p, "oaSmooth Key", icon="", command=asf.loadOaSmoothKeys)
        self.add_sub_separator()
        # ar Shake
        self.add_menu_item(
            p, "arShaker UI", icon="arShake.png", command=asf.loadArShake
        )
        # Fix subframes
        self._disabled_add_menu_item(p, "fix subframes ", icon="", command="")

        ## RETIME
        self.add_button(
            "",
            icon="juls_toolbox_shelf_retime.png",
            annotation="Right-click open Segreto_Shift Keys UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadSegretoShiftKeyUI)
        p = cmds.popupMenu(b=1)
        # Shift Keys
        self.add_menu_item(
            p, "Segreto_Shift Keys UI", icon="", command=asf.loadSegretoShiftKeyUI
        )
        # Retime node
        self._disabled_add_menu_item(
            p, "Create retime node", icon="", command='print("Create retimer node")'
        )
        # import nuke retime curve
        self._disabled_add_menu_item(
            p,
            "Importe Nuke retime curve",
            icon="",
            command='print("Create retimer node")',
        )

        ## Motion trail tools
        self.add_button(
            "",
            icon="juls_toolbox_shelf_motiontrail.png",
            annotation="Right-click open Advanced Motion Trail UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=asf.loadAdvancedMotionTrailUI)
        p = cmds.popupMenu(b=1)
        # AdvaNCED Motion trail UI
        self.add_menu_item(
            p,
            "Advanced Motion Trail UI",
            icon="",
            command=asf.loadAdvancedMotionTrailUI,
        )
        # Simple Motion trail UI
        self.add_menu_item(
            p, "Easy Motion Trail UI", icon="", command=asf.loadEasyMotionTrailUI
        )
        # Simple Motion trail UI
        self.add_menu_item(
            p, "ml_arc Tracer UI", icon="ml_arcTracer.png", command=asf.loadMlArcTracer
        )

        ## DYNAMIC
        self.add_button(
            "",
            icon="juls_toolbox_shelf_dynamics.png",
            annotation="Right-click open Dynamic Overlap Tool UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand="")
        p = cmds.popupMenu(b=1)
        # Speedometer
        self.add_menu_item(p, "Speedometer UI", icon="", command=asf.loadSpeedometer)
        # Retime node
        self._disabled_add_menu_item(p, "Dynamic Overlap Tool UI", icon="", command="")
        # Gravity ball tool
        self._disabled_add_menu_item(p, "Gravity Ball UI", icon="", command="")
        # Ballistic animation
        self.add_menu_item(
            p,
            "ml_ballistic Animation",
            icon="ml_ballisticAnimation.png",
            command=asf.loadBallisticAnimation,
        )
        # Distance o meter
        self.add_menu_item(
            p, "Distance-o-meter", icon="", command=asf.loadDistanceMeter
        )

        # ## viewport
        # self.add_button("", icon = "pxoanim_shelf_view.png",
        #                   annotation = "Right-click open bhGhost")
        # p = cmds.popupMenu(b = 3, postMenuCommand = asf.loadBhGhost)
        # p = cmds.popupMenu(b = 1)

        # self.add_separator()

        self.add_separator()

        ## open new scene
        self.add_button(
            "", icon="juls_toolbox_shelf_projectWIP.png", annotation="Force new scene"
        )
        p = cmds.popupMenu(b=1)
        # bh Ghost
        self.add_menu_item(
            p,
            "force new scene NO SAVING",
            icon="juls_toolbox_shelf_projectWIP.png",
            command="cmds.file(new=True, f=True)",
        )

        self.add_separator()

        ## WIKI
        self.add_button(
            label="",
            annotation="WIKI",
            icon="wiki.png",
            command=partial(asf.openWebBrowser, wiki_url),
        )

        self.add_separator()

        ## IF YOU SEE THIS YOUR IN SCRIPTOR VERSION
        if extraButton:
            self.add_button(label="Local", annotation="", icon="")
            self.add_button(label="Mode!", annotation="", icon="")


customShelf()

"""
###################################################################################

class customShelf(_shelf):
    def build(self):
        self.add_button(label= "button1", icon = "icCRpickWalkToggle.png")
        self.add_button("button2", icon = "icQuadrupedRiggerUI.png")
        cmds.separator(style=None)
        self.add_button("Animation", icon = "flowPathObj.png")
        p = cmds.popupMenu(b = 1)
        self.add_menu_item(p, "locinator", icon = "icQuadrupedRiggerUI.png")
        self.add_menu_item(p, "tweeners")
        sub = self.add_sub_menu(p, "subMenuLevel1",icon = "flowPathObj.png")
        self.add_menu_item(sub, "subMenuLevel1Item1")
        sub2 = self.add_sub_menu(sub, "subMenuLevel2",icon = "kk_icons/b04.XPM")
        self.add_menu_item(sub2, "subMenuLevel2Item1")
        self.add_menu_item(sub2, "subMenuLevel2Item2",icon = "flowPathObj.png")
        self.add_menu_item(sub, "subMenuLevel1Item2")
        self.add_menu_item(p, "popupMenuItem3",icon = "kk_icons/b21.XPM")
customShelf()
###################################################################################
"""
