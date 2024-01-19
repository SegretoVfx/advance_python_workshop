# JULS ANIM SHELF ***********************************************
# Description   = Launch the process to create the juls_anim_shelf
#                 This script will be launched by the userSetup.py file
#                 located in the same script folder
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


# import juls_shelf_functions as jfunc
import juls_shelf_builder as jbuild
import juls_shelf_info as jinfo

importlib.reload(jbuild)
importlib.reload(jfunc)
importlib.reload(jinfo)


class AnimShelf(jbuild.Builder):
    def build(self):
        ## SCENE
        ## MENU

        self.add_button(
            "",
            icon="pxoanim_shelf_SGexchange.png",
            annotation="Right-click change shot context",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadChangeContext)
        p = cmds.popupMenu(b=1)

        # CHANGE CONTEXT
        self.add_menu_item(
            p, "Change Shot Context", icon="", command=jfunc.loadChangeContext
        )

        # DISPLAY CONTEXT
        self.add_menu_item(
            p, "Display Shot Context", icon="", command=jfunc.loadContext
        )

        # SHOTGRID LOADER
        self.add_menu_item(
            p,
            "Shotgrid Loader UI",
            icon="pxoanim_shelf_SG.png",
            command=jfunc.loadSGCacheUI,
        )

        ## LOAD SCENE
        self.add_button(
            label="",
            annotation="Load Scene UI",
            icon="pxoanim_shelf_open.png",
            command=partial(jfunc.loadSaveTool, "load"),
        )

        self.add_separator()

        ## SAVE LOCAL
        self.add_button(
            label="",
            annotation="Save scene",
            icon="pxoanim_shelf_saveLocal.png",
            command=jfunc.loadDefaultSave,
        )

        ## SAVE AS
        self.add_button(
            label="",
            annotation="Save increment scene",
            icon="pxoanim_shelf_saveSG.png",
            command=partial(jfunc.loadSaveTool, "save"),
        )

        self.add_separator()

        ## IMPORT MENU
        self.add_button(
            "",
            icon="pxoanim_shelf_import.png",
            annotation="Right-click open Scene Content UI",
        )
        # RMB open most used option
        p = cmds.popupMenu(b=3, postMenuCommand=partial(jfunc.loadSaveTool, "content"))
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)

        ### SCENE CONTENT
        self.add_menu_item(
            p,
            "Scene Content UI",
            icon="",
            command=partial(jfunc.loadSaveTool, "content"),
        )
        ### ASSET LOADER
        self.add_menu_item(
            p, "Asset Loader", icon="", command=partial(jfunc.loadSaveTool, "asset")
        )
        ### CACHE LOADER
        self.add_menu_item(p, "Cache Loader UI", icon="", command=jfunc.loadCacheUI)
        ### SHOTGUN LOADER
        self.add_menu_item(
            p,
            "Shotgun Loader UI",
            icon="pxoanim_shelf_SG.png",
            command=jfunc.loadSGCacheUI,
        )

        self.add_sub_separator()

        ### UPDATE ALL REFERENCE
        self.add_menu_item(
            p, "Update All Referenced Assets", icon="", command=jfunc.updateAllReference
        )

        ##########################################################

        self.add_separator()

        ## MANAGE
        self.add_button(
            label="Files", icon="", annotation="Right-click open Shot folder"
        )
        #  RMB open most used option
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(jfunc.open_shot_folder, "content")
        )
        # LMB will open a sub menu
        p = cmds.popupMenu(b=1)

        # FOLDER
        self.add_menu_item(
            p,
            "open Shot Project folder",
            icon="",
            command=partial(jfunc.open_shot_folder, "content"),
        )
        # IMAGE SEQUENCE
        self.add_menu_item(
            p,
            "open Shot Framestore folder",
            icon="",
            command=partial(jfunc.open_shot_images_folder, "asset"),
        )

        ## SHOTGUN INFO
        self.add_button(
            "", icon="pxoanim_shelf_SGinfo.png", annotation="Right-click open Shotgun"
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadSGOpen)
        p = cmds.popupMenu(b=1)

        # open task
        self.add_menu_item(
            p,
            "open Shotgun on task",
            icon="",
            command=partial(jfunc.loadSGOpen, "task"),
        )
        # open Shot
        self.add_menu_item(
            p,
            "open Shotgun on Shot",
            icon="",
            command=partial(jfunc.loadSGOpen, "shot"),
        )
        # open sequence
        self.add_menu_item(
            p,
            "open Shotgun on Sequence",
            icon="",
            command=partial(jfunc.loadSGOpen, "sequence"),
        )
        # open project
        self.add_menu_item(
            p,
            "open Shotgun on Project",
            icon="",
            command=partial(jfunc.loadSGOpen, "project"),
        )

        self.add_sub_separator()

        # open shotgun panel
        self.add_menu_item(p, "open Shotgun panel", icon="", command=jfunc.loadSGPanel)

        self.add_sub_separator()

        # Open SG Notes
        self.add_menu_item(p, "Shot Notes", icon="", command=jfunc.loadSGShotNotes)

        ##########################################################

        self.add_separator()

        ## PIXO SHOTGUN
        ## SHOTGUN EDIT
        self.add_button(
            "",
            icon="pxoanim_shelf_SGedit.png",
            annotation="Right-click Set timeline to work range",
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(jfunc.loadsetFrameRange, "shot")
        )
        p = cmds.popupMenu(b=1)
        # set Maya framerange to shot range (from shotgun)
        self.add_menu_item(
            p,
            "Set timeline to work range",
            icon="",
            command=partial(jfunc.loadsetFrameRange, "shot"),
        )
        # set Maya framerange to cut range (from shotgun)
        self.add_menu_item(
            p,
            "Set timeline to cut range",
            icon="",
            command=partial(jfunc.loadsetFrameRange, "cut"),
        )

        self.add_sub_separator()

        # set Maya scene resolution (from shotgun)
        self.add_menu_item(
            p,
            "Set Camera resolution from Shotgun",
            icon="",
            command=jfunc.setResolutionFromSG,
        )

        ## PLAYBLAST / PUBLISH TOOLS
        ## PLAYBLAST
        self.add_button(
            "",
            icon="pxoanim_shelf_playblast.png",
            annotation="Right-click open PXO Playblast UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadPlayblastUi)
        p = cmds.popupMenu(b=1)
        # playblast UI
        self.add_menu_item(
            p, "PXO Playblast UI", icon="", command=jfunc.loadPlayblastUi
        )
        # pxo playblast
        self.add_menu_item(p, "PXO Playblast", icon="", command=jfunc.loadPlayblast)
        # playblast witness cam
        self.add_menu_item(
            p, "PXO Witness Playblast", icon="", command=jfunc.loadPlayblastWitness
        )

        self.add_separator()

        ## PUBLISH
        self.add_button(
            "",
            icon="pxoanim_shelf_publish.png",
            annotation="Right-click Deadline Anim Publish UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.legacy_loadDeadlinePublish)
        p = cmds.popupMenu(b=1)
        # Open Deadline Publish UI
        self.add_menu_item(
            p,
            "Deadline anim publish UI (legacy)",
            icon="",
            command=jfunc.legacy_loadDeadlinePublish,
        )
        # Open Local Publish UI
        self.add_menu_item(
            p,
            "Local anim publish UI (legacy)",
            icon="",
            command=jfunc.legacy_loadLocalPublish,
        )

        self.add_sub_separator()

        # Open Deadline Publish UI
        self.add_menu_item(
            p, "Deadline pyblish UI", icon="", command=jfunc.deadline_pyblish
        )
        # Open Local Publish UI
        self.add_menu_item(p, "Local publish UI", icon="", command=jfunc.local_pyblish)

        self.add_sub_separator()

        # Open Camera Publish UI
        self.add_menu_item(
            p, "Custom camera publish UI", icon="", command=jfunc.loadCameraPublish
        )

        self.add_sub_separator()

        # Open Camera Publish UI
        self.add_menu_item(
            p, "Tag list editor UI", icon="", command=jfunc.open_tag_manager
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

        # ## SCENE SETUP TOOLS
        # ## PIXO TOOLS
        # self.add_button("", icon = "pxoanim_shelf_pxo.png",
        #                 annotation = "Right-click enable Graph Editor Hot Keys")
        # p = cmds.popupMenu(b = 3, postMenuCommand = "")
        # p = cmds.popupMenu(b = 1)
        # # Graph Editor Hot Keys
        # self.add_menu_item(p, "Enable Graph Editor Hot Keys -- Manual",
        #                    icon = "",
        #                    command = partial(fun.openWebBrowser, hotkey_url))
        # # Hot Box Menu
        # self._disabled_add_menu_item(p, "Enable Hot Box (space bar) Menu",
        #                    icon = "",
        #                    command = "")
        # self.add_sub_separator()

        # # Load Huumand standard reference
        # self.add_menu_item(p, "Create PXO Standard Man",
        #                    icon = "",
        #                    command = fun.importReferenceStandardMan)

        # # Remove Huumand standard reference
        # self.add_menu_item(p, "Remove PXO Standard Man",
        #                    icon = "",
        #                    command = fun.removeReferenceStandardMan)

        # self.add_sub_separator()

        ## CAMERA TOOLS
        self.add_button(
            "",
            icon="pxoanim_shelf_cam.png",
            annotation="Right-click Creates followCam on selected node (point Contraint)",
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(jfunc.createObserverCamera, "cam")
        )
        p = cmds.popupMenu(b=1)
        # creates follow camera on selected node
        self.add_menu_item(
            p,
            "Create followCam on selected (point Contraint)",
            icon="",
            command=partial(jfunc.createObserverCamera, "cam"),
        )
        # creates follow camera UI
        self.add_menu_item(
            p,
            "Create followCam UI",
            icon="",
            command=partial(jfunc.createObserverCamera, "UI"),
        )

        self.add_sub_separator()

        # creates Witness cam
        self.add_menu_item(
            p,
            "Create WitnessCam on selected (persp)",
            icon="",
            command=partial(jfunc.loadSegretoCreateWitnessCamUI, "Persp"),
        )
        # open Witness cam UI
        self.add_menu_item(
            p,
            "Create WitnessCam UI",
            icon="",
            command=jfunc.loadSegretoCreateWitnessCamUI,
        )

        self.add_sub_separator()

        # Print annotation on screen
        self.add_menu_item(
            p,
            "Display channel HUD",
            icon="",
            command=partial(jfunc.loadAnnotationUI, "show"),
        )
        # Print annotation on screen
        self.add_menu_item(
            p,
            "delete channel HUD",
            icon="",
            command=partial(jfunc.loadAnnotationUI, "delete"),
        )

        self.add_sub_separator()

        # # open Multi-view UI
        # self._disabled_add_menu_item(p, "Multi-view UI",
        #                    icon = "",
        #                    command = '')
        # Fix perspactive
        self.add_menu_item(p, "Fix perspective", icon="", command=jfunc.loadFixPersp)
        # Bake camera UI
        self.add_menu_item(p, "Bake camera UI", icon="", command=jfunc.loadBakeCamera)

        ## IMAGE PLANE
        self.add_button(
            "",
            icon="pxoanim_shelf_imageplane.png",
            annotation="Right-click Cache and Play",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadCacheNplay)
        p = cmds.popupMenu(b=1)
        # Cache the scene and play realtime
        self.add_menu_item(p, "Cache and Play", icon="", command=jfunc.loadCacheNplay)
        # Image plane helper
        self.add_menu_item(
            p, "Image Plane Tool UI", icon="", command=jfunc.loadImagePlaneHelper
        )

        ## HOLD OUT
        self.add_button(
            "",
            icon="pxoanim_shelf_holdout.png",
            annotation="Right-click Create holdout useBackground",
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(jfunc.loadHoldoutCreator, "useBackground")
        )
        p = cmds.popupMenu(b=1)
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Create holdout useBackground",
            icon="",
            command=partial(jfunc.loadHoldoutCreator, "useBackground"),
        )
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Create holdout Grey lambert",
            icon="",
            command=partial(jfunc.loadHoldoutCreator, "lambert"),
        )
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Create holdout Black surfaceShader",
            icon="",
            command=partial(jfunc.loadHoldoutCreator, "surfaceShader"),
        )
        self.add_sub_separator()
        # Creat holdout on selected geo (add BG shader)
        self.add_menu_item(
            p,
            "Revert to default Shader lambert1",
            icon="",
            command=partial(jfunc.loadHoldoutCreator, "default"),
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
            icon="pxoanim_shelf_maintenance.png",
            annotation="Right-click open Outliner Color manager UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadOutlinerColorManager)
        p = cmds.popupMenu(b=1)
        # Outliner Color Manager
        self.add_menu_item(
            p,
            "Outliner Color Manager UI",
            icon="",
            command=jfunc.loadOutlinerColorManager,
        )
        # segreto Create Display Layers
        self.add_menu_item(
            p, "Create Display layer", icon="", command=jfunc.loadDisplayLayerCreator
        )
        # Channel box enhancer
        self.add_menu_item(
            p, "Install Channel Box Plus", icon="", command=jfunc.loadChannelBoxPlus
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
            icon="pxoanim_shelf_picker.png",
            command=partial(jfunc.loadAnimSchoolPicker),
        )

        ## LIBRARY
        self.add_button(
            "",
            icon="pxoanim_shelf_library.png",
            annotation="Right-click open Studio Library UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadStudioLibrary)
        p = cmds.popupMenu(b=1)
        # studio library
        self.add_menu_item(
            p,
            "Studio Library UI",
            icon="studioLibrary.png",
            command=jfunc.loadStudioLibrary,
        )
        # loadPose2Shelf
        self.add_menu_item(
            p, "pose2Shelf", icon="pose2Shelf.png", command=jfunc.loadPose2Shelf
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
            icon="pxoanim_shelf_rigs.png",
            annotation="Right-click toggles All/Selected rigs resolution",
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(jfunc.loadSwitchResolution, "tog")
        )
        p = cmds.popupMenu(b=1)
        # Geo to switch Res
        self.add_menu_item(
            p,
            "Toggle All/Selected rigs resolution",
            icon="",
            command=partial(jfunc.loadSwitchResolution, "tog"),
        )
        # Geo to High Res
        self.add_menu_item(
            p,
            "All/Selected rigs to High resolution",
            icon="pxoanim_shelf_rigs_lowtohigh.png",
            command=partial(jfunc.loadSwitchResolution, "high"),
        )
        # Geo to Low Res
        self.add_menu_item(
            p,
            "All/Selected rigs to Low resolution",
            icon="pxoanim_shelf_rigs_hightolow.png",
            command=partial(jfunc.loadSwitchResolution, "low"),
        )

        self.add_sub_separator()

        # Reset Selected
        self.add_menu_item(
            p,
            "reset selected controllers",
            icon="",
            command=partial(jfunc.loadSegretoResetAttr, "ctrl", False),
        )
        # Reset asset
        self.add_menu_item(
            p,
            "reset selected asset",
            icon="",
            command=partial(jfunc.loadSegretoResetAttr, "asset", False),
        )
        # Reset scene
        self.add_menu_item(
            p,
            "reset all scene",
            icon="",
            command=partial(jfunc.loadSegretoResetAttr, "scene", False),
        )

        self.add_sub_separator()

        # killl anim Selected
        self.add_menu_item(
            p,
            "kill animation selected controllers",
            icon="",
            command=partial(jfunc.loadSegretoResetAttr, "ctrl", True),
        )
        # killl anim  asset
        self.add_menu_item(
            p,
            "kill animation selected asset",
            icon="",
            command=partial(jfunc.loadSegretoResetAttr, "asset", True),
        )

        self.add_sub_separator()

        # Enabling pick walking
        self.add_menu_item(
            p,
            "Enable Pick Walking",
            icon="pxoanim_shelf_rigs_pickwalking.png",
            command=jfunc.loadPickWalking,
        )
        # Mocap
        self.add_menu_item(
            p,
            "Launch Mocap Setup",
            icon="pxoanim_shelf_mocap.png",
            command=jfunc.loadMoCapsetup,
        )

        self.add_separator()

        ## TOOLSETS
        self.add_button(
            "", icon="pxoanim_shelf_tools.png", annotation="Right-click open ack tools"
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadAckTool)
        p = cmds.popupMenu(b=1)

        # Morgan Loomis Sub menus list
        sub = self.add_sub_menu(p, "Morgan Loomis Tools", icon="ml_default.png")

        self.add_menu_item(
            sub,
            "ml_animCurveEditor",
            icon="ml_animCurveEditor.png",
            command=partial(jfunc.loadMlTool, "ml_animCurveEditor"),
        )
        self.add_menu_item(
            sub,
            "ml_arcTracer",
            icon="ml_arcTracer.png",
            command=partial(jfunc.loadMlTool, "ml_arcTracer"),
        )
        self.add_menu_item(
            sub,
            "ml_ballisticAnimation",
            icon="ml_ballisticAnimation.png",
            command=partial(jfunc.loadMlTool, "ml_ballisticAnimation"),
        )
        self.add_menu_item(
            sub,
            "ml_breakdown",
            icon="ml_breakdown.png",
            command=partial(jfunc.loadMlTool, "ml_breakdown"),
        )
        self.add_menu_item(
            sub,
            "ml_cameraDepthDragger",
            icon="ml_cameraDepthDragger.png",
            command=partial(jfunc.loadMlTool, "ml_cameraDepthDragger"),
        )
        self.add_menu_item(
            sub,
            "ml_centerOfMass",
            icon="ml_centerOfMass.png",
            command=partial(jfunc.loadMlTool, "ml_centerOfMass"),
        )
        self.add_menu_item(
            sub,
            "ml_colorControl",
            icon="ml_colorControl.png",
            command=partial(jfunc.loadMlTool, "ml_colorControl"),
        )
        self.add_menu_item(
            sub,
            "ml_controlLibrary",
            icon="ml_controlLibrary.png",
            command=partial(jfunc.loadMlTool, "ml_controlLibrary"),
        )
        self.add_menu_item(
            sub,
            "ml_convertRotationOrder",
            icon="ml_convertRotationOrder.png",
            command=partial(jfunc.loadMlTool, "ml_convertRotationOrder"),
        )
        self.add_menu_item(
            sub,
            "ml_copyAnim",
            icon="ml_copyAnim.png",
            command=partial(jfunc.loadMlTool, "ml_copyAnim"),
        )
        self.add_menu_item(
            sub,
            "ml_copySkin",
            icon="ml_copySkin.png",
            command=partial(jfunc.loadMlTool, "ml_copySkin"),
        )
        self.add_menu_item(
            sub,
            "ml_deleteKey",
            icon="ml_deleteKey.png",
            command=partial(jfunc.loadMlTool, "ml_deleteKey"),
        )
        self.add_menu_item(
            sub,
            "ml_frameGraphEditor",
            icon="ml_frameGraphEditor.png",
            command=partial(jfunc.loadMlTool, "ml_frameGraphEditor"),
        )
        self.add_menu_item(
            sub,
            "ml_goToKeyframe",
            icon="ml_goToKeyframe.png",
            command=partial(jfunc.loadMlTool, "ml_goToKeyframe"),
        )
        self.add_menu_item(
            sub,
            "ml_graphEditorMask",
            icon="ml_graphEditorMask.png",
            command=partial(jfunc.loadMlTool, "ml_graphEditorMask"),
        )
        self.add_menu_item(
            sub,
            "ml_hold",
            icon="ml_hold.png",
            command=partial(jfunc.loadMlTool, "ml_hold"),
        )
        self.add_menu_item(
            sub,
            "ml_keyValueDragger",
            icon="ml_keyValueDragger.png",
            command=partial(jfunc.loadMlTool, "ml_keyValueDragger"),
        )
        self.add_menu_item(
            sub,
            "ml_lockAndHideAttributes",
            icon="ml_lockAndHideAttributes.png",
            command=partial(jfunc.loadMlTool, "ml_lockAndHideAttributes"),
        )
        self.add_menu_item(
            sub,
            "ml_parentShape",
            icon="ml_parentShape.png",
            command=partial(jfunc.loadMlTool, "ml_parentShape"),
        )
        self.add_menu_item(
            sub,
            "ml_pivot",
            icon="ml_pivot.png",
            command=partial(jfunc.loadMlTool, "ml_pivot"),
        )
        self.add_menu_item(
            sub,
            "ml_puppet",
            icon="ml_puppet.png",
            command=partial(jfunc.loadMlTool, "ml_puppet"),
        )
        self.add_menu_item(
            sub,
            "ml_resetBind",
            icon="ml_resetBind.png",
            command=partial(jfunc.loadMlTool, "ml_resetBind"),
        )
        self.add_menu_item(
            sub,
            "ml_resetChannels",
            icon="ml_resetChannels.png",
            command=partial(jfunc.loadMlTool, "ml_resetChannels"),
        )
        self.add_menu_item(
            sub,
            "ml_selectKeyed",
            icon="ml_selectKeyed.png",
            command=partial(jfunc.loadMlTool, "ml_selectKeyed"),
        )
        self.add_menu_item(
            sub,
            "ml_setKey",
            icon="ml_setKey.png",
            command=partial(jfunc.loadMlTool, "ml_setKey"),
        )
        self.add_menu_item(
            sub,
            "ml_softWeights",
            icon="ml_softWeights.png",
            command=partial(jfunc.loadMlTool, "ml_softWeights"),
        )
        self.add_menu_item(
            sub,
            "ml_stopwatch",
            icon="ml_stopwatch.png",
            command=partial(jfunc.loadMlTool, "ml_stopwatch"),
        )
        self.add_menu_item(
            sub,
            "ml_tangentWeight",
            icon="ml_tangentWeight.png",
            command=partial(jfunc.loadMlTool, "ml_tangentWeight"),
        )
        self.add_menu_item(
            sub,
            "ml_toggleVisibility",
            icon="ml_toggleVisibility.png",
            command=partial(jfunc.loadMlTool, "ml_toggleVisibility"),
        )
        self.add_menu_item(
            sub,
            "ml_transferKeytimes",
            icon="ml_transferKeytimes.png",
            command=partial(jfunc.loadMlTool, "ml_transferKeytimes"),
        )
        self.add_menu_item(
            sub,
            "ml_worldBake",
            icon="ml_worldBake.png",
            command=partial(jfunc.loadMlTool, "ml_worldBake"),
        )

        # Aaron Koressel Tools menu
        self.add_menu_item(
            p, "Aaron Koressel tools UI", icon="", command=jfunc.loadAckTool
        )

        # Wesley Chandler Tools
        self.add_menu_item(
            p, "Wesley Chandler Tools UI", icon="", command=jfunc.loadWesleyTool
        )

        # add sub_separator
        cmds.menuItem(p=p, divider=True)

        # Toolset
        self.add_menu_item(p, "PXO_toolset", icon="", command=jfunc.loadToolSet)

        # # animbot
        # self._disabled_add_menu_item(p, "Animbot UI",
        #                    icon = "",
        #                    command = "")
        # # aTool
        # self.add_menu_item(p, "aTool UI",
        #                    icon = "animbot.png",
        #                    command = fun.loadATool)

        # add sub_separator
        cmds.menuItem(p=p, divider=True)

        # Aaron Koressel Tools menu
        self.add_menu_item(
            p,
            "Aaron Koressel tools Manual",
            icon="",
            command=partial(jfunc.openWebBrowser, jinfo.ack_tools_url),
        )

        # Morgan Loomis menu
        self.add_menu_item(
            p,
            "Morgan Loomis tools Manual",
            icon="",
            command=partial(jfunc.openWebBrowser, jinfo.ml_tools_url),
        )

        # bh Ghost
        self.add_menu_item(
            p, "bhGhost UI", icon="bhGhost.png", command=jfunc.loadBhGhost
        )
        # Create Annotation
        self.add_menu_item(
            p, "Create annotation UI", icon="", command=jfunc.loadCreateAnnotateNode
        )

        self.add_sub_separator()

        # bh speed
        self.add_menu_item(
            p, "bhSpeed UI", icon="bhSpeed.png", command=jfunc.loadBhSpeed
        )
        # Smear
        self.add_menu_item(p, "boSmear UI", icon="", command=jfunc.loadBoSmear)

        ## Selector
        self.add_button(
            "",
            icon="pxoanim_shelf_select.png",
            annotation="Right-click selects all Keyed Controllers",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadSelectAllKeyed)
        p = cmds.popupMenu(b=1)
        # Select all Keyed controllers
        self.add_menu_item(
            p,
            "Select all Keyed controllers (scene / selected asset)",
            icon="",
            command=jfunc.loadSelectAllKeyed,
        )

        self.add_sub_separator()

        # Select all controllers (current selection or all asset)
        self.add_menu_item(
            p,
            "Select all Controllers (scene / selected asset)",
            icon="",
            command=partial(jfunc.loadSelectAll, "ctrl"),
        )

        # Select geo
        self.add_menu_item(
            p,
            "Select all Geometries (scene / selected asset)",
            icon="",
            command=partial(jfunc.loadSelectAll, "geo"),
        )

        # # Select geo
        # self.add_menu_item(p, "Select all Cameras (scene / selected asset)",
        #                    icon = "",
        #                    command = partial(fun.loadSelectAll, 'cam'))

        # # Select geo
        # self.add_menu_item(p, "Select all curves (scene / selected asset)",
        #                    icon = "",
        #                    command = partial(fun.loadSelectAll, 'crv'))

        # Select contraint
        self._disabled_add_menu_item(
            p, "Select Constraint", icon="", command=jfunc.loadSelectConstraint
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
            icon="pxoanim_shelf_copy.png",
            annotation="Right-click copy all animation (A -> B)",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.segreto_anim_utils)
        p = cmds.popupMenu(b=1)
        # copies animation from first selected node to second, including attribute channels
        self.add_menu_item(
            p, "Copy anim (A -> B)", icon="", command=jfunc.segreto_anim_utils
        )
        # all Translation
        self.add_menu_item(
            p,
            "Copy translation anim (A -> B)",
            icon="",
            command=partial(jfunc.segreto_anim_utils, attribute=["tx", "ty", "tz"]),
        )
        # all rotation
        self.add_menu_item(
            p,
            "Copy rotation anim (A -> B)",
            icon="",
            command=partial(jfunc.segreto_anim_utils, attribute=["rx", "ry", "rz"]),
        )
        # copy anim UI
        # self._disabled_add_menu_item(p, "Copy anim UI",
        #                    icon = "",
        #                    command = 'print("copy anim tool")')

        ## MIRROR ANIMATION UI
        self.add_button(
            "",
            icon="pxoanim_shelf_mirror.png",
            annotation="Right-click open Mirror Animation tools UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadStudioLibrary)
        p = cmds.popupMenu(b=1)
        # Mirror animation with Studio Library
        self.add_menu_item(
            p,
            "Studio Library UI",
            icon="studioLibrary.png",
            command=jfunc.loadStudioLibrary,
        )
        #  Mirror animation with PXO UI
        self._disabled_add_menu_item(
            p, "Mirror Animation tools UI", icon="", command=jfunc.loadStudioLibrary
        )

        ## WALK HELPER
        self.add_button(
            "",
            icon="pxoanim_shelf_walkhelper.png",
            annotation="Right-click launches Sticky feet",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadStickyFeet)
        p = cmds.popupMenu(b=1)
        # Walk helper tool
        self.add_menu_item(p, "Sticky feet", icon="", command=jfunc.loadStickyFeet)
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
            icon="pxoanim_shelf_snap.png",
            annotation="Right-click snap all channels",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.snap_parent)
        p = cmds.popupMenu(b=1)

        # snap all
        self.add_menu_item(p, "Snap all channels", icon="", command=jfunc.snap_parent)
        # snap translation only
        self.add_menu_item(p, "Snap Translation", icon="", command=jfunc.snap_translate)
        # snap rotation only
        self.add_menu_item(p, "Snap Rotation", icon="", command=jfunc.snap_rotate)

        self.add_sub_separator()

        # Snap tool UI
        self.add_menu_item(
            p,
            "Snap tool UI",
            icon="pxoanim_shelf_snap.png",
            command=jfunc.loadAlignTool,
        )
        # animSnap
        self.add_menu_item(p, "animSnap UI", icon="", command=jfunc.loadAnimSnap)
        # Match Placement
        self.add_menu_item(
            p, "Match Placement UI", icon="", command=jfunc.loadGbMatchPlacement
        )

        # snap Selected channels
        # self._disabled_add_menu_item(p, "Snap selected channels",
        #                    icon = "",
        #                    command = 'print("Snap tool")')

        ## Constraint UI
        self.add_button(
            label="",
            icon="pxoanim_shelf_constraint.png",
            annotation="Right-click open Easy Constraint UI",
            command=jfunc.loadEasyParentUI,
        )
        p = cmds.popupMenu(
            b=3, postMenuCommand=partial(jfunc.loadEasyParentUI, "UI", "")
        )
        p = cmds.popupMenu(b=1)
        # Constraint UI
        self.add_menu_item(
            p,
            "Easy Constraint UI",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "UI", ""),
        )
        self.add_sub_separator()
        # parent constraint with offset
        self.add_menu_item(
            p,
            "parent constraint offset",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "parenting", True),
        )
        # parent constraint without offset
        self.add_menu_item(
            p,
            "parent constraint snap",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "parenting", False),
        )
        # orientation constraint with offset
        self.add_menu_item(
            p,
            "orientation constraint offset",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "orienting", True),
        )
        # orientation constraint without offset
        self.add_menu_item(
            p,
            "orientation constraint snap",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "orienting", False),
        )
        # point (selected nodes to Specific Point on Geo with offset)
        self.add_menu_item(
            p,
            "point constraint offset",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "pointing", True),
        )
        # point (selected nodes to specific Point on geo without offset)
        self.add_menu_item(
            p,
            "point constraint snap",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "pointing", False),
        )
        # Rivet (with offset)
        self.add_menu_item(
            p,
            "Rivet offset",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "rivet", True),
        )
        # point (snap)
        self.add_menu_item(
            p,
            "Rivet snap",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "rivet", False),
        )

        self.add_sub_separator()

        # unparenting
        self.add_menu_item(
            p,
            "kill constraint (selected objects)",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "unparenting", ""),
        )
        # unparenting
        self.add_menu_item(
            p,
            "kill constraint (all scene)",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "killConst", ""),
        )
        # bakeAnim
        self.add_menu_item(
            p,
            "bake Anim and delete constraint",
            icon="",
            command=partial(jfunc.loadEasyParentUI, "bakeAnim", ""),
        )

        ## Space switch
        self.add_button(
            "",
            icon="pxoanim_shelf_spaceswitch.png",
            annotation="Right-click open segretoLocinate",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadLocinate)
        p = cmds.popupMenu(b=1)
        # Locinate made by Julien Segreto
        self.add_menu_item(
            p, "segretoLocinate", icon="locator.png", command=jfunc.loadLocinate
        )
        # open morgan Loomis world bakerUI
        self.add_menu_item(
            p, "ml_world Bake", icon="ml_worldBake.png", command=jfunc.loadWorldBaker
        )

        self.add_sub_separator()

        # open morgan Loomis rotation order UI
        self.add_menu_item(
            p,
            "ml_convert Rotation Order",
            icon="ml_convertRotationOrder.png",
            command=jfunc.loadRotationOrderSwitch,
        )

        ## IK/FK switch
        # self.add_button("", icon = "pxoanim_shelf_IKFKswitch.png",
        #                 annotation = "Right-click switch IK/FK on current frame")
        # p = cmds.popupMenu(b = 3, postMenuCommand = partial(fun.loadIkFkSwitch, 'one'))
        # p = cmds.popupMenu(b = 1)
        # # switch IKFK on current frame and set a key
        # self._disabled_add_menu_item(p, "IK/FK switch on current frame",
        #                    icon = "",
        #                    command = partial(fun.loadIkFkSwitch, 'one'))
        # # switch IKFK on current frame without setting a key
        # self._disabled_add_menu_item(p, "IK/FK switch on current frame (unkeyed)",
        #                    icon = "",
        #                    command = partial(fun.loadIkFkSwitch, 'unkeyed'))
        # # switch IKFK on all frame range animation - Smart Bake
        # self._disabled_add_menu_item(p, "IK/FK switch all animation (smart)",
        #                    icon = "",
        #                    command = partial(fun.loadIkFkSwitch, 'smart'))
        # # switch IKFK on all frame range animation - Bake Every frame
        # self._disabled_add_menu_item(p, "IK/FK switch all animation",
        #                    icon = "",
        #                    command = partial(fun.loadIkFkSwitch, 'all'))

        ## EDIT ANIM CURVE UI
        self.add_button(
            "",
            icon="pxoanim_shelf_curve.png",
            annotation="Right-click open Segreto_Shift Keys UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadSegretoShiftKeyUI)
        p = cmds.popupMenu(b=1)
        # Shift Keys
        self.add_menu_item(
            p, "Segreto_Shift Keys UI", icon="", command=jfunc.loadSegretoShiftKeyUI
        )

        self.add_sub_separator()

        # Keyframe reduction UI
        self.add_menu_item(
            p,
            "Keyframe Reduction UI",
            icon="keyframeReduction.png",
            command=jfunc.loadKeyframeReduction,
        )
        # clean redundant keys
        self.add_menu_item(
            p, "ackDeleteRedundantKeys ", icon="", command=jfunc.loadAckDeleteRedundant
        )

        self.add_sub_separator()

        # Tween machine
        self.add_menu_item(
            p,
            "Tween Machine UI",
            icon="tweenMachine.png",
            command=jfunc.loadTweenMachine,
        )

        # Scale anim curve
        self.add_menu_item(
            p, "np_curve Local Scale UI", icon="", command=jfunc.loadNP_curveLocalScale
        )

        # Smooth anim curve
        self.add_menu_item(
            p, "KTL_smooth Key", icon="", command=jfunc.loadKTL_smoothKey
        )
        # Smooth Key
        self.add_menu_item(p, "oaSmooth Key", icon="", command=jfunc.loadOaSmoothKeys)
        self.add_sub_separator()
        # ar Shake
        self.add_menu_item(
            p, "arShaker UI", icon="arShake.png", command=jfunc.loadArShake
        )
        # Fix subframes
        self._disabled_add_menu_item(p, "fix subframes ", icon="", command="")

        ## RETIME
        self.add_button(
            "",
            icon="pxoanim_shelf_retime.png",
            annotation="Right-click open Segreto_Shift Keys UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadSegretoShiftKeyUI)
        p = cmds.popupMenu(b=1)
        # Shift Keys
        self.add_menu_item(
            p, "Segreto_Shift Keys UI", icon="", command=jfunc.loadSegretoShiftKeyUI
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
            icon="pxoanim_shelf_motiontrail.png",
            annotation="Right-click open Advanced Motion Trail UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand=jfunc.loadEasyMotionTrailUI)
        p = cmds.popupMenu(b=1)

        # Simple Motion trail UI
        self.add_menu_item(
            p,
            "ml_arc Tracer UI",
            icon="ml_arcTracer.png",
            command=jfunc.loadEasyMotionTrailUI,
        )

        # Simple Motion trail UI
        self.add_menu_item(
            p,
            "ml_arc Tracer UI",
            icon="ml_arcTracer.png",
            command=jfunc.loadMlArcTracer,
        )

        # AdvaNCED Motion trail UI
        self.add_menu_item(
            p,
            "Advanced Motion Trail UI",
            icon="",
            command=jfunc.loadAdvancedMotionTrailUI,
        )

        ## DYNAMIC
        self.add_button(
            "",
            icon="pxoanim_shelf_dynamics.png",
            annotation="Right-click open Dynamic Overlap Tool UI",
        )
        p = cmds.popupMenu(b=3, postMenuCommand="")
        p = cmds.popupMenu(b=1)
        # Speedometer
        self.add_menu_item(p, "Speedometer UI", icon="", command=jfunc.loadSpeedometer)
        # Retime node
        self._disabled_add_menu_item(p, "Dynamic Overlap Tool UI", icon="", command="")
        # Gravity ball tool
        self._disabled_add_menu_item(p, "Gravity Ball UI", icon="", command="")
        # Ballistic animation
        self.add_menu_item(
            p,
            "ml_ballistic Animation",
            icon="ml_ballisticAnimation.png",
            command=jfunc.loadBallisticAnimation,
        )
        # Distance o meter
        self.add_menu_item(
            p, "Distance-o-meter", icon="", command=jfunc.loadDistanceMeter
        )

        # ## viewport
        # self.add_button("", icon = "pxoanim_shelf_view.png",
        #                   annotation = "Right-click open bhGhost")
        # p = cmds.popupMenu(b = 3, postMenuCommand = fun.loadBhGhost)
        # p = cmds.popupMenu(b = 1)

        # self.add_separator()

        self.add_separator()

        ## open new scene
        self.add_button(
            "", icon="pxoanim_shelf_projectWIP.png", annotation="Force new scene"
        )
        p = cmds.popupMenu(b=1)
        # bh Ghost
        self.add_menu_item(
            p,
            "force new scene NO SAVING",
            icon="pxoanim_shelf_projectWIP.png",
            command="cmds.file(new=True, f=True)",
        )

        self.add_separator()

        ## WIKI
        self.add_button(
            label="",
            annotation="WIKI",
            icon="wiki.png",
            command=partial(jfunc.openWebBrowser, jinfo.wiki_url),
        )

        self.add_separator()

        ## ZZ
        self.add_button(label="ZZ", annotation="ZZ", icon="", command="")
