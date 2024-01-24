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
import maya_utils as utils


print("Hello from shelf functions")


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
    file_ext = utils.get_cur_scn_ext()
    raw_name = utils.get_cur_scn_raw_name()
    file_name = utils.get_cur_scn_file_name()
    old_version = utils.get_cur_scn_version()
    split_sc_name = utils.split_cur_scn_name()

    if file_name is not "":
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
