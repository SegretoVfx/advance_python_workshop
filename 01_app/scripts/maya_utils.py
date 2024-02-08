# ------------------------------------------------------------
# --- MAYA UTILS ---
# Description   = List of standard functions that can be usefull
#
# Date   = 2024 - 01 - 23
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage = import the current file into your script and call the function
# ------------------------------------------------------------
import os
import pathlib

import maya.cmds as cmds


# --- SCENE NAME MANIPULATION ---
def get_cur_scn_parent_dir():
    ws = cmds.workspace(q=True, dir=True)
    path = pathlib.Path(ws)
    return path.parent


def get_cur_scn_full_path():
    _path = cmds.file(q=True, sn=True)

    return _path


def get_cur_scn_file_name():
    _file_name = cmds.file(q=True, sn=True, shn=True)

    return _file_name


def get_cur_scn_raw_name(file_name):
    """Get the current scene name without the extension."""
    _raw_name, _ = os.path.splitext(file_name)

    return _raw_name


def get_cur_scn_ext(file_name):
    _, extension = os.path.splitext(file_name)

    return extension


def split_string(str, sp="_"):
    _split_lst = str.split(sp)

    return _split_lst


def get_cur_scn_version(file_name):
    """Get the current scene version number.
    Return None if the name of the scene hasn't been versionned.

    Returns:
        str: version number
        None: If there's no numbers at the end of the file name
    """
    _version = split_string(file_name)[-1]

    if _version.isnumeric():
        # The last part of the list is a number => Can be incremented
        return _version

    return None


# --- INCREMENT ---
def increment_input(input):
    if not input.isnumeric():
        raise ValueError("The argument must be a numeral.")

    _output = int(input) + 1

    return _output


def increment_file_name(file_name=None):
    if file_name is None:
        file_name = get_cur_scn_file_name()

    if file_name:
        f_ext = get_cur_scn_ext(file_name)
        f_raw_name = get_cur_scn_raw_name(file_name)
        f_version = get_cur_scn_version(f_raw_name)

        if f_version is None:
            new_version = "001"
            new_name = f"{f_raw_name}_{new_version}{f_ext}"
        else:
            new_version = increment_input(f_version)
            new_version = str(f"{new_version:03d}")

            # Removing the version number from the original file
            split_name = split_string(f_raw_name)
            split_name.pop(-1)
            join_name = "_".join(split_name)

            new_name = f"{join_name}_{new_version}{f_ext}"

        return new_name

    else:
        return None

# --- MAYA ACTION ---
def do_playblast(output):
    """Launch a background playblast without opening the Maya GUI

    Args:
        output (str): the name of the output video - must contain the .mp4
    """
    print(output)
    cmds.playblast(
        format="qt",
        percent=100,
        viewer=False,
        filename=output,
        forceOverwrite=True,
        widthHeight=[1980, 1080],
    )




def confirm_dialog(message=None):
    if message is None:
        message = "Default confirm dialog"

    cmds.confirmDialog(
        title="Confirm",
        message=message,
        button=["Ok"],
    )
