# ------------------------------------------------------------
# --- juls anim motion path ---
# Description   = Creates a path followed by the selecte character
#
# Date   = 2024 - 02
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage =
"""
This tool is intended to be used with  a treadmill walk/run cycle animation.
- Select the root control of the animated character.
- In the UI Click on the [>>] button next to the root control label to set the
    name of the root control to the textField.
- Select the hip control of the animated character.
- In the UI Click on the [>>] button next to the hip control label to set the
    name of the hip control to the textField.

- Give the character a broad motion.
    NOTE : The more keys you set to the root control, the more precise the
    motion path will be.
    
- In the UI, click on [create paths].
    This will magically create the motion paths for the root and the hip
    Based on the animation you gave earlier.
    By default, it'll create a few locators constrained on the paths.
    You'll see later how to use these locators.
 

- Now Click on [Hook to paths].
     It will link the controllers to the appropriate motion paths.
     The base animation speed should be quite similar.

blah blah """
# ------------------------------------------------------------

from maya import cmds


def get_ctrl_position(control):
    """List the position of the selected controller for each key

    Args:
        control (str): Name of the controller to use as as guide for motion pass creation

    Returns:
        lst(str): _description_
    """
    # ------------------------------------------------------------
    # --- Get controller's translation data ---
    pos_lst = []

    # Filter the key list
    keys_lst = list(
        dict.fromkeys(
            cmds.keyframe(
                control,
                q=True,
                at="translate",
                t=(),
            )
        )
    )
    keys_lst.sort()

    for key in keys_lst:

        # Set current time to the current key
        cmds.currentTime(key, edit=True)

        # Take translate data from the controller
        trans = cmds.xform(control, q=True, translation=True)

        pos_lst.append(tuple(trans))

    return pos_lst


def build_motion_path(control):

    position_lst = get_ctrl_position(control)
    # ------------------------------------------------------------
    # --- Trace curve motion path ---
    path_curve_name = f"path_curve_{control}"
    if cmds.objExists(path_curve_name):
        cmds.delete(path_curve_name)

    # Build the path curve.
    cmds.curve(
        name=path_curve_name,
        d=2,
        point=position_lst,
    )


def main():
    print("Build the curve")

    root_ctl = cmds.ls(sl=True)[0]

    build_motion_path(root_ctl)