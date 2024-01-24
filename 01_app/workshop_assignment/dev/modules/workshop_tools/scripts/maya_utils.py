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

import maya.cmds as cmds


# --- SCENE NAME MANIPULATION ---
def get_cur_scn_file_name():
    """Get the current file name.

    Returns:
        str: File name
    """
    file_name = cmds.file(q=True, sn=True, shn=True)

    return file_name


def get_cur_scn_raw_name():
    """Get the current scene name.
    Return None if the scene hasn't been saved yet.

    Returns:
        str: raw_name (scene name without the extension)
    """
    raw_name, _ = os.path.splitext(get_cur_scn_file_name())

    return raw_name


def get_cur_scn_ext():
    """Get the current scene extension.
    Return None if the scene hasn't been saved yet.

    Returns:
        str: extension
    """
    _, extension = os.path.splitext(get_cur_scn_file_name())

    return extension


def split_cur_scn_name():
    """split the current scene name into a list using '_' as
    a separator

    Returns:
        ls: list of the split name
    """
    raw_name = get_cur_scn_raw_name()

    ls_name = raw_name.split("_")
    print(ls_name)

    return ls_name


def get_cur_scn_version():
    """Get the current scene version number.
    Return None if the name of the scene hasn't been versionned.

    Returns:
        str: version
    """
    version = split_cur_scn_name()[-1]

    if not version.isnumeric():
        return None

    return version
