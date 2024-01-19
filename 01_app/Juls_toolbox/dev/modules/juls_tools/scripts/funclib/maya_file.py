import maya.cmds as cmds


def scene_load(scene_name=""):
    if not scene_name:
        cmds.OpenScene()
    else:
        cmds.OpenScene(scene_name)
