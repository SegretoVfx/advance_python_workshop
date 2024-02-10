# ------------------------------------------------------------
# --- juls anim motion path ---
# Description   = Creates a path followed by the selecte character
#
# Date   = 2024 - 02
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage =
"""This tool is working better based on a treadmill walk/run cycle.

 1 - With the root control, give the characer a broad motion according to your needs.

 2 - Then, with the root selected, press "create path".

     It will create a motion path curve, based on the root animation. 

 3 - Do the same step 1 and 2 with the character's hip controller selected.
    
     It will create a motion path curve for the hip.

 4 - Click on "Hook to paths".

     It will link the controllers to the motion path 
     The base animation speed should be quite similar.

blah blah """
# ------------------------------------------------------------

import maya.cmds as cmds


def build_motion_path(control):

    # start_key = cmds.playbackOptions(q=True, animationStartTime=True)

    # qkkcmds.currentTime(start_key)

    trans_lst = []

    # Get the list of the keysframes where keys are set
    # To build the curve_path based on the position of current keys
    # The more keys on the root, the more precise the curve will be.
    key_list = cmds.keyframe(control, attribute="translate", query=True, time=())
    kl = list(dict.fromkeys(key_list))
    kl.sort()

    for key in kl:

        # Set current time to the first key
        cmds.currentTime(key, edit=True)

        trans = cmds.xform(control, q=True, translation=True)

        trans_lst.append(tuple(trans))

    path_curve_name = f"path_curve_{control}"
    if cmds.objExists(path_curve_name):
        cmds.delete(path_curve_name)

    # Build the path curve.
    cmds.curve(
        name=path_curve_name,
        d=2,
        point=trans_lst,
    )


def main():
    print("Build the curve")

    root_ctl = cmds.ls(sl=True)[0]

    build_motion_path(root_ctl)
