# ------------------------------------------------------------
# --- ANIM SHELF FUNCTIONS ---
# Description   = All the functions needed to launch the tools from the shelf.
#
# Date   = 2024 - 01 - 23
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage = This library is called from the anim_shelf_creator file.
# ------------------------------------------------------------

import maya.cmds as cmds
import maya_utils
import py_utils

import importlib


print("Hello from shelf functions")

# ------------------------------------------------------------
# --- FILE ---


def open_scene(*args):
    cmds.OpenScene()


def save_scene(*args):
    cmds.file(save=True)


def save_scene_as(*args):
    cmds.SaveSceneAs()


def save_scene_increment(*args):
    """auto-increment save the current scene,
    If the scene already has a number it'll be incremented,
    If not, it will be generated,
    If the scene hadn't been saved a default name will be set.
    """
    file_ext = maya_utils.get_cur_scn_ext()
    raw_name = maya_utils.get_cur_scn_raw_name()
    file_name = maya_utils.get_cur_scn_file_name()
    old_version = maya_utils.get_cur_scn_version()
    split_sc_name = maya_utils.split_cur_scn_name()

    if file_name == "":
        if old_version is None:
            new_version = "001"
            new_name = f"{raw_name}_{new_version}"

        else:
            # Remove version from previews file name
            split_sc_name.pop(-1)

            new_version = int(old_version) + 1
            # new_version = int(old_vn) + 1

            new_version = str(f"{new_version:03d}")

            new_name = f"{'_'.join(split_sc_name)}_{new_version}"

    else:
        new_name = "origin_001"

    cmds.file(rename=f"{new_name}{file_ext}")
    cmds.file(save=True, type="mayaAscii")

    # from scripts.segretoTools import segretoEasyMotionTrail
    # importlib.reload(segretoEasyMotionTrail)
    # segretoEasyMotionTrail.main()


# ------------------------------------------------------------
# --- TOOLS ---


# --- wes tools ---
def launch_wes_tools(*args):
    """Open the wes tool window
    There is a lot of usefull tools available there.
    """
    wes = importlib.import_module(".wesAnimTools", "py")

    wes.UI()


# --- ack tools ---
def launch_ack_tools(*args):
    """Open the wes tool window
    There is a lot of usefull tools available there.
    """
    ack = importlib.import_module(".ack_launcherUI", "mel")

    ack.AckToolsLauncher()


# --- atools ---
def launch_atools(*args):
    """install the aTools
    There is a lot of usefull tools available there.
    """
    atools = importlib.import_module(".aToolsInstall", "py")
