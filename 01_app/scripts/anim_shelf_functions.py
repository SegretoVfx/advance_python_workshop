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
import os
import importlib

import maya.mel as mel
import maya.cmds as cmds

import maya_utils


# ------------------------------------------------------------
# --- FILE ---


def open_scene(*args):
    cmds.OpenScene()


def save_scene(*args):
    if maya_utils.get_cur_scn_full_path():
        cmds.file(save=True)
    else:
        maya_utils.confirm_dialog("The current file must be saved as...")


def save_scene_as(*args):
    cmds.SaveSceneAs()


def save_scene_increment(*args):
    """auto-increment save the current scene,
    If the scene already has a number it'll be incremented,
    If not, it will be generated,
    If the scene hadn't been saved a reminder will pop up.
    """
    new_name = maya_utils.increment_file_name()

    if new_name is None:
        message = "The Scene must be saved first."
        maya_utils.confirm_dialog(message)
    else:
        cmds.file(rename=new_name)
        cmds.file(save=True)  # , type="mayaAscii")


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


# ------------------------------------------------------------
# --- PICKERS ---


# --- awe control picker ---
def launch_awe_picker(*args):
    _awe_tool_name = "aweControlPicker"
    _awe_file_path = f"{os.path.dirname(__file__)}\\mel\\{_awe_tool_name}\\"
    _file = open(f"{_awe_file_path}/{_awe_tool_name}.mel")

    _content = _file.read()  # .replace('\n',' ')
    _file.close()

    mel.eval(f"{_content}")


def launch_dw_picker(*args):
    # import dwpicker
    importlib.import_module(".dwpicker", "py")
    dwpicker.show()


def launch_pr_selection(*args):
    importlib.import_module(".prSelectionUi", "py")

    prSelectionUi.UI()


# ------------------------------------------------------------
# --- PLAYBLAST ---


# --- Playblast current view ---
def launch_playblast(*args):
    cur_scn_name = maya_utils.get_cur_scn_file_name()
    cur_raw_name = maya_utils.get_cur_scn_raw_name(cur_scn_name)

    if not cur_raw_name:
        message = "The Scene must be saved first."
        maya_utils.confirm_dialog(message)
    else:
        maya_utils.do_playblast(f"movies\{str(cur_raw_name)}.mp4")

        message = "Playblast complete."
        maya_utils.confirm_dialog(message)


# ------------------------------------------------------------
# --- JULS ANIM PATH TOOL ---
def launch_juls_anim_path(*args):
    import juls_anim_motion_path

    juls_anim_motion_path.main()


# ------------------------------------------------------------
# --- EDITORS ---


# --- Oen editors prots ---
def link_editor_port(editor, *args):
    # Open ports for vscode and pycharm

    def connect_port(_port, _source, _output):
        # Open new ports
        if not cmds.commandPort(_port, query=True):
            cmds.commandPort(_port, sourceType=_source, echoOutput=True)

            print(f"{editor} port{port} connected")
            print(_output)

    if editor == "pycharm":
        port = ":4434"
        source = "python"
        output = (
            f'{"-"*40}\n'
            "# Keyboard Shortcuts                        \n"
            "#                                           \n"
            "# Use ALT+S : send selected script to Maya. \n"
            "# Use ALT+A : send all script to Maya.      \n"
            "#                                           \n"
            f'{"-"*40}\n'
        )

        connect_port(port, source, output)

    elif editor == "vscode":
        # PYTHON
        port = ":7001"
        source = "mel"

        output = (
            f'{"-"*40}\n'
            "# MEL script Shortcuts                         \n"
            "#                                              \n"
            "# On Mac                                       \n"
            "# Use CMD+SHIFT+M : send mel script to Maya.   \n"
            "#                                              \n"
            "# On Windows/Linux                             \n"
            "# Use ALT+SHIFT+M : send mel script to Maya.   \n"
            "#                                              \n"
            f'{"-"*40}\n'
        )

        connect_port(port, source, output)

        # MEL
        port = ":7002"
        source = "python"

        output = (
            f'{"-"*40}\n'
            "# PYTHON script Shortcuts                      \n"
            "#                                              \n"
            "# On Mac                                       \n"
            "# Use CMD+SHIFT+P : send python script to Maya.\n"
            "#                                              \n"
            "# On Windows/Linux                             \n"
            "# Use ALT+SHIFT+P : send python script to Maya.\n"
            "#                                              \n"
            f'{"-"*40}\n'
        )

        connect_port(port, source, output)


def disconnect_port(*args):
    # Disconnect all open ports
    ports = cmds.commandPort(listPorts=True, q=True)
    print(ports)
    for port in ports:
        is_open = cmds.commandPort(port, q=True)

        if is_open:
            cmds.commandPort(name=f"{port}", cl=True)
            print(f"Closing {port} port")
