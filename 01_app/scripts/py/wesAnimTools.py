import maya.cmds as cmds
import maya.mel as mel

import importlib

# wes = importlib.import_module(".")
# wes = importlib.import_module(".wesTools", "py")
# Load in wesKeyEditor
# import wesKeyEditor
# wes = importlib.import_module(".", "py.wesTools")
# from py.wesTools import wesSceneSetup as wesSS

import py.wesTools
import py.wesTools.wesSceneSetup
import py.wesTools.wesScreenTracker
import py.wesTools.wesOffsetAnim
import py.wesTools.wesRetime
import py.wesTools.wesImagePlanes
import py.wesTools.wesKeyEditor

# print(dir(py.wesTools.wesSceneSetup))


def UI():
    if cmds.dockControl("wesToolBarDock", exists=True):
        cmds.deleteUI("wesToolBarDock")

    if cmds.window("wesAnimToolsUI", exists=True, resizeToFitChildren=True):
        cmds.deleteUI("wesAnimToolsUI")
        # cmds.windowPref("wesAnimToolsUI", removeAll=True)

    user_width = 140
    user_height = 18

    # Create window interface
    wesAnimToolsUI = cmds.window(
        "wesAnimToolsUI",
        title="wesAnimToolsUI",
        sizeable=True,
        width=user_width,
    )

    # Choose either scrollLayout or rowColumnLayout
    # cmds.scrollLayout('wesLayout', height=650, width=user_width+23)
    cmds.rowColumnLayout("wesLayout")
    cmds.setParent("..")
    cmds.showWindow(wesAnimToolsUI)

    print("content")
    ##################Add Modules###################
    # SceneSetup Module
    py.wesTools.wesSceneSetup.UI(
        parentWindow="wesLayout",
        user_width=user_width,
        user_height=user_height,
        frameClosed=False,
    )
    print("hypercontent")

    # Screen Tracker Module
    py.wesTools.wesScreenTracker.UI(
        parentWindow="wesLayout",
        user_width=user_width,
        user_height=user_height,
        frameClosed=False,
    )

    # Finger Select
    # wesFingerSelect.UI(parentWindow='wesLayout', user_width=user_width, user_height=user_height, frameClosed=True)

    # wesOffsetAnim
    py.wesTools.wesOffsetAnim.UI(
        parentWindow="wesLayout",
        user_width=user_width,
        user_height=user_height,
        frameClosed=True,
    )

    # reTime module
    py.wesTools.wesRetime.UI(
        parentWindow="wesLayout",
        user_width=user_width,
        user_height=user_height,
        frameClosed=True,
    )

    # imageplane module
    py.wesTools.wesImagePlanes.UI(
        parentWindow="wesLayout",
        user_width=user_width,
        user_height=user_height,
        frameClosed=True,
    )

    # wesKeyEditor module
    py.wesTools.wesKeyEditor.UI(
        parentWindow="wesLayout",
        user_width=user_width,
        user_height=user_height,
        frameClosed=False,
    )

    # Dock the window
    cmds.dockControl(
        "wesToolBarDock",
        label="wesAnimTools",
        area="right",
        content=wesAnimToolsUI,
        allowedArea=["left", "right"],
    )
