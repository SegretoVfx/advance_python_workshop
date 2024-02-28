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

Select front paws and chest >>
Same for rear paws hip

Create locators baked with anim
Patented inside the front mo_loc (local)

The anim of the limbs is connected to the front loc

Manage the path

Add speed control on mo_loc

Add rotation control on mo_loc all axis (when the grind isn't flat)
blah blah """
# ------------------------------------------------------------

from functools import partial

from maya import cmds


def viewport_togg_decorator(func):
    def wrapper(*args, **kwargs):
        # cmds.refresh(suspend=True)
        cmds.PauseViewportEval()
        func(*args, **kwargs)
        # cmds.refresh(suspend=False)
        cmds.PauseViewportEval()

    return wrapper


def close_window(window_id, window=None, arg=None):
    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id, window=True)


def delete_if_exists(obj: str):
    if cmds.objExists(obj):
        cmds.delete(obj)


def get_playback_info():
    time_min = cmds.playbackOptions(q=True, min=True)
    time_max = cmds.playbackOptions(q=True, max=True)

    return time_min, time_max


def bake_anim(ctrl, time_min, time_max):
    cmds.bakeResults(ctrl, t=(time_min, time_max), sm=True)


def get_ctrl_position(control_name):
    pos_lst = []
    time_min = cmds.playbackOptions(q=True, min=True)
    time_max = cmds.playbackOptions(q=True, max=True)

    cmds.select(control_name, replace=True)
    cmds.keyTangent(inTangentType="spline", outTangentType="spline")
    cmds.setInfinity(preInfinite="linear")
    cmds.setInfinity(postInfinite="linear")

    # Subtracts 20 frames at the start to have a longer motion path
    cmds.currentTime(time_min - 20, edit=True)
    trans = cmds.xform(control_name, q=True, translation=True)
    pos_lst.append(tuple(trans))

    # List all the frames with a translate key.
    keys_list = list(
        dict.fromkeys(
            cmds.keyframe(
                control_name,
                q=True,
                at="translate",
                t=(time_min, time_max),
            )
        )
    )
    keys_list.sort()

    for key in keys_list:
        cmds.currentTime(key, edit=True)
        trans = cmds.xform(control_name, q=True, translation=True)
        pos_lst.append(tuple(trans))

    # add 20 frame at the end to have a motion path longer than the frame range.
    cmds.currentTime(time_max + 20, edit=True)
    trans = cmds.xform(control_name, q=True, translation=True)
    pos_lst.append(tuple(trans))

    return pos_lst


@viewport_togg_decorator
def build_path_curve(path_name, control_pos, *kwargs):
    delete_if_exists(path_name)

    cmds.curve(
        name=path_name,
        d=2,
        point=control_pos,
    )


def build_locators_structure(ctrl_name, size, *args):
    placements = {
        "front": 4,
        "mid": 13,
        "tail": 12,
    }
    molocs = {}

    def _build_hierarchie(place, spot, c):
        grp = f"{ctrl_name}_moloc_{place}_{spot}_grp"
        offset_grp = f"{ctrl_name}_moloc_{place}_{spot}_offset"
        locator = f"{ctrl_name}_moloc_{place}_{spot}_ctrl"

        delete_if_exists(grp)
        # the baked hierarchie is not selectable
        if spot == "main":
            cmds.spaceLocator(name=locator)
            cmds.setAttr(f"{locator}Shape.localScaleX", 1 * size)
            cmds.setAttr(f"{locator}Shape.localScaleY", 3 * size)
            cmds.setAttr(f"{locator}Shape.localScaleZ", 5 * size)
            cmds.setAttr(f"{locator}Shape.overrideEnabled", 1)
            cmds.setAttr(f"{locator}Shape.overrideColor", c)
        elif spot == "sub":
            cmds.circle(name=locator)
            cmds.setAttr(f"{locator}.visibility", 0)
            cmds.setAttr(f"{locator}Shape.overrideEnabled", 1)
            cmds.setAttr(f"{locator}Shape.overrideColor", c)
        elif spot == "baked":
            cmds.group(name=locator, empty=True)

        # Build offset hierarchy
        cmds.group(locator, name=offset_grp)
        cmds.group(offset_grp, name=grp)

        return grp, offset_grp, locator

    for place, col in placements.items():
        main_hierarchie = _build_hierarchie(place, "main", col)
        sub_hierarchie = _build_hierarchie(place, "sub", col)
        baked_hierarchie = _build_hierarchie(place, "baked", col)

        cmds.parent(sub_hierarchie[0], main_hierarchie[2])
        cmds.parent(baked_hierarchie[0], sub_hierarchie[2])

        # nested dictionnary for molocs values
        molocs[place] = {}
        molocs[place].update({"main": main_hierarchie})
        molocs[place].update({"sub": sub_hierarchie})
        molocs[place].update({"baked": baked_hierarchie})

    return molocs


def find_nearest_point_on_mopath(mopath, moloc, target):
    moloc_mid_main_ctrl = f"{moloc['mid']['main'][2]}"
    npoc_name = f"{moloc['mid']['main'][0]}_npoc1"
    mopath_shape = cmds.listRelatives(
        mopath, shapes=True
    )  # MAY BE YOU WILL NEED TO RENAME THIS SHIT BEFORE USING IT
    t_min, t_max = get_playback_info()

    cmds.currentTime(t_min)
    # Snap a locator to the position of the target (to get WS pos)
    temp_loc = cmds.spaceLocator(n="temp_loc")[0]
    cmds.delete(cmds.parentConstraint(target, temp_loc))

    # Create a nearestPointOnCurve node and rename it
    npoc = cmds.createNode("nearestPointOnCurve", name=npoc_name)

    cmds.connectAttr(f"{temp_loc}.translateX", f"{npoc}.inPositionX")
    cmds.connectAttr(f"{temp_loc}.translateY", f"{npoc}.inPositionY")
    cmds.connectAttr(f"{temp_loc}.translateZ", f"{npoc}.inPositionZ")
    cmds.connectAttr(f"{mopath_shape[0]}.worldSpace[0]", f"{npoc}.inputCurve")

    # Get the output parameter value from the node
    param = cmds.getAttr(f"{npoc}.parameter")
    cmds.setAttr(f"{moloc_mid_main_ctrl}.move_along", param)
    cmds.setKeyframe(f"{moloc_mid_main_ctrl}.move_along", t=t_min)

    cmds.delete(npoc)
    cmds.delete(temp_loc)

    cmds.currentTime(t_max)
    # Snap a locator to the position of the target (to get WS pos)
    temp_loc = cmds.spaceLocator(n="temp_loc")[0]
    cmds.delete(cmds.parentConstraint(target, temp_loc))

    # Create a nearestPointOnCurve node and rename it
    npoc = cmds.createNode("nearestPointOnCurve", name=npoc_name)

    cmds.connectAttr(f"{temp_loc}.translateX", f"{npoc}.inPositionX")
    cmds.connectAttr(f"{temp_loc}.translateY", f"{npoc}.inPositionY")
    cmds.connectAttr(f"{temp_loc}.translateZ", f"{npoc}.inPositionZ")
    cmds.connectAttr(f"{mopath_shape[0]}.worldSpace[0]", f"{npoc}.inputCurve")

    # Get the output parameter value from the node
    param = cmds.getAttr(f"{npoc}.parameter")
    cmds.setAttr(f"{moloc_mid_main_ctrl}.move_along", param)
    cmds.setKeyframe(f"{moloc_mid_main_ctrl}.move_along", t=t_min)

    cmds.delete(npoc)
    cmds.delete(temp_loc)


def attach_moloc_to_mopath(path_name, molocs, offset, *args):
    t_min, t_max = get_playback_info()

    for place, _ in molocs.items():
        # for spot, controls_name in molocs[place].items():

        mopath_node = f"{molocs[place]['main'][0]}_mopathnode"
        if place == "front":
            l_shift_val = offset * 2
            r_shift_val = 0
        elif place == "tail":
            l_shift_val = 0
            r_shift_val = offset * 2
        else:
            l_shift_val = offset
            r_shift_val = offset

        cmds.pathAnimation(
            molocs[place]["main"][0],
            name=mopath_node,
            fractionMode=False,
            follow=True,
            followAxis="x",
            upAxis="y",
            worldUpType="scene",
            startTimeU=t_min - l_shift_val,
            endTimeU=t_max + r_shift_val,
            curve=path_name,
        )

        cmds.keyTangent(
            mopath_node,
            inTangentType="spline",
            outTangentType="spline",
        )

    # Add attribute on the main moloc to control the uValue on mopath
    cmds.addAttr(
        molocs["mid"]["main"][2],
        longName="move_along",
        attributeType="double",
        minValue=0.0,
        maxValue=1.0,
        defaultValue=0,
        keyable=True,
    )
    cmds.setKeyframe(
        molocs["mid"]["main"][2],
        attribute="move_along",
        value=0,
        t=t_min - offset,
    )
    cmds.setKeyframe(
        molocs["mid"]["main"][2],
        attribute="move_along",
        value=1,
        t=t_max + offset,
    )

    cmds.keyTangent(
        f"{molocs['mid']['main'][2]}.move_along",
        inTangentType="spline",
        outTangentType="spline",
    )

    cmds.connectAttr(
        f"{molocs['mid']['main'][2]}.move_along",
        f"{molocs['mid']['main'][0]}_mopathnode.uValue",
        force=True,
    )


def attach_control_to_moloc(control, molocs, *args):
    """

    Make the hip_path locators follow the main loc
    remove the two secondaries moloc?
    front and tail moloc follow the main
    but have their own attribute to control placement
    the front and rear paws will be linked with these loc
    """
    # for place, _ in molocs.items():
    #     # for spot, controls_name in molocs[place].items():
    #
    #     mopath_node = f"{molocs['mid']['main'][2]}"

    moloc_mid_main_ctrl = molocs["mid"]["main"][2]
    moloc_front_baked_ctrl = molocs["front"]["baked"][2]
    moloc_mid_baked_ctrl = molocs["mid"]["baked"][2]

    cmds.pointConstraint(moloc_mid_baked_ctrl, control, weight=1)

    cmds.aimConstraint(
        moloc_front_baked_ctrl,
        control,
        weight=1,
        aimVector=(0, 0, 1),
        offset=(0, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 1, 0),
    )


# Locinate your controllers - Select the controls you want to locinate
# @viewport_togg_decorator
def bake_to_worldspace(object_to_bake, *args):
    t_min, t_max = get_playback_info()

    # create worldspace_locator for all selected controllers
    worldspace_name = f"{object_to_bake}_worldspace"

    # Create the worldspace locators
    worldspace_locator = cmds.spaceLocator(n=worldspace_name)
    # cmds.setAttr(f"{worldspace_name}Shape.localScaleX", 3 * size)
    # cmds.setAttr(f"{worldspace_name}Shape.localScaleY", 1 * size)
    # cmds.setAttr(f"{worldspace_name}Shape.localScaleZ", 3 * size)
    #
    # set_color(worldspace_name, 1)

    # constraint the locator to the animated controller
    cmds.parentConstraint(object_to_bake, worldspace_locator, mo=False, w=1)

    # bake loci to save controllers animation
    bake_anim(worldspace_name, t_min, t_max)

    # delete the constraint between controllers and locators
    worldspace_constraint = cmds.listRelatives(
        worldspace_name,
        type="constraint",
    )
    cmds.delete(worldspace_constraint)

    # Constraint the controller to the worldspace
    cmds.parentConstraint(worldspace_locator, object_to_bake, mo=False, w=1)


# Locinate your Locators - Select ALL locators auto-created earlier
@viewport_togg_decorator
def bake_to_controller(*args):
    # select the worldspace_locator you want animation to be injected
    worldspace_lst = cmds.ls(selection=True)

    # Check if selection is True
    if worldspace_lst == []:
        create_window(
            "Error2",
            title="Selection error",
            label="Please Select at least one worldspace locator to bake",
        )
        raise ValueError("No worldspace locator selected")

    else:
        t_min, t_max = get_playback_info()
        # create worldspace_locator for all selected controllers
        for worldspace in worldspace_lst:
            ctl_name = worldspace.removesuffix("_worldspace")
            # bake loci to save controllers animation
            bake_anim(ctl_name, t_min, t_max)

            # delete the locators
            cmds.delete(worldspace)

        create_window(
            "Completed2",
            title="Step Completed",
            label="Animation baked back to controllers",
        )


def create_window(window_name, title, label, *kwargs):
    win_width = 600

    close_window(window_name)

    window = cmds.window(window_name, title=title, s=True, rtf=True)
    cmds.paneLayout(w=win_width)
    cmds.text(label=label)
    cmds.separator(style="in", height=10)
    cmds.button(label="Close", command=partial(close_window, window_name))
    cmds.setParent("..")
    cmds.showWindow(window)
    cmds.window(window, e=True, width=win_width, height=1)


def get_selection_position():
    sel = cmds.ls(sl=True)
    if sel:
        return cmds.xform(
            q=True,
            translation=True,
            abssolute=True,
        )
    else:
        cmds.error("select the rig control you want to track.")


def query_txt_cmd_label(text_cmd_name, *args):
    q_label = cmds.text(text_cmd_name, query=True, label=True)
    return q_label


def change_text_label(text_cmd_name, control_name, *args):
    get_first_selected()
    cmds.text(
        text_cmd_name,
        edit=True,
        label=control_name,
        backgroundColor=(1, 1, 0.3),
    )


def on_checkbox_toggled(*args):
    print(args)
    print(f"Checkbox is checked: {args[0]}")


def on_button_click(*args):
    print(args)
    # Don't forget the *args
    cmds.polySphere()


# my_button = cmds.button(command=partial(my_button_on_click_handler, arg1, arg2))
#
#
# def my_button_on_click_handler(arg1, arg2):
#     # call all your functions and do stuff here
#     my_other_func1(arg1)
#     my_other_func2(arg2)


def press_gros_button_process(text_label, pressed_btn, *args):
    pass


def get_first_selected():
    if cmds.ls(sl=True):
        return cmds.ls(sl=True)[0]
    else:
        cmds.error("You must select a controller.")


def press_build_mopath(
    txt_store_root_ctrl, txt_store_hip_ctrl, txt_store_chest_ctrl, *args
):
    root_ctrl = query_txt_cmd_label(txt_store_root_ctrl)
    hip_ctrl = query_txt_cmd_label(txt_store_hip_ctrl)
    chest_ctrl = query_txt_cmd_label(txt_store_chest_ctrl)

    if cmds.objExists(root_ctrl):
        print("build the root")
        press_root_track_process(root_ctrl)

    if cmds.objExists(hip_ctrl):
        print("build the hip")
        press_hip_track_process(hip_ctrl, root_ctrl)

    if cmds.objExists(chest_ctrl):
        print("build the chest")
        print(chest_ctrl)


@viewport_togg_decorator
def press_root_track_process(root_ctrl, *args):
    root_path_name = f"{root_ctrl}_mo_path"
    root_ctrl_pos = get_ctrl_position(root_ctrl)
    molocs = build_locators_structure(root_ctrl, 1)
    # molocs is a nested dictionnary
    """
    {
        "front": {
            "main": (
                "moloc_front_main_grp",
                "moloc_front_main_offset",
                "moloc_front_main_ctrl",
            ),
            "sub": (
                "moloc_front_sub_grp",
                "moloc_front_sub_offset",
                "moloc_front_sub_ctrl",
            ),
            "baked": (
                "moloc_front_baked_grp",
                "moloc_front_baked_offset",
                "moloc_front_baked_ctrl",
            ),
        },
        "mid": {
            "main": (
                "moloc_mid_main_grp",
                "moloc_mid_main_offset",
                "moloc_mid_main_ctrl",
            ),
            "sub": (
                "moloc_mid_sub_grp",
                "moloc_mid_sub_offset",
                "moloc_mid_sub_ctrl",
            ),
            "baked": (
                "moloc_mid_baked_grp",
                "moloc_mid_baked_offset",
                "moloc_mid_baked_ctrl",
            ),
        },
        "tail": {
            "main": (
                "moloc_tail_main_grp",
                "moloc_tail_main_offset",
                "moloc_tail_main_ctrl",
            ),
            "sub": (
                "moloc_tail_sub_grp",
                "moloc_tail_sub_offset",
                "moloc_tail_sub_ctrl",
            ),
            "baked": (
                "moloc_tail_baked_grp",
                "moloc_tail_baked_offset",
                "moloc_tail_baked_ctrl",
            ),
        },
    }"""

    build_path_curve(root_path_name, root_ctrl_pos)
    attach_moloc_to_mopath(root_path_name, molocs, 40)
    attach_control_to_moloc(root_ctrl, molocs)


@viewport_togg_decorator
def press_hip_track_process(hip_ctrl, root_ctrl, *args):
    hip_path_name = f"{hip_ctrl}_mo_path"
    root_path_name = f"{root_ctrl}_mo_path"
    hip_control_pos = cmds.xform(
        hip_ctrl,
        worldSpace=True,
        translation=True,
        query=True,
    )
    hip_molocs = build_locators_structure(hip_ctrl, 1)

    delete_if_exists(hip_path_name)
    cmds.duplicate(root_path_name, name=hip_path_name)
    cmds.xform(hip_path_name, t=[0, hip_control_pos[1], 0])
    attach_moloc_to_mopath(hip_path_name, hip_molocs, 40)

    find_nearest_point_on_mopath(hip_path_name, hip_molocs, hip_ctrl)

    # attach_control_to_moloc(hip_control_name, hip_locators)


def press_change_label(text_label, *args):
    control_name = get_first_selected()

    change_text_label(text_label, control_name)


@viewport_togg_decorator
def press_bake_to_worldspace(
    front_right,
    front_left,
    rear_right,
    rear_left,
    *args,
):
    list_to_bake = []

    cmds.group(n="front_paws_parent_grp", e=True)

    frt_r_ctrl = query_txt_cmd_label(front_right)
    frt_l_ctrl = query_txt_cmd_label(front_left)
    rear_r_ctrl = query_txt_cmd_label(rear_right)
    rear_l_ctrl = query_txt_cmd_label(rear_left)

    if cmds.objExists(frt_r_ctrl):
        bake_to_worldspace(frt_r_ctrl)
    if cmds.objExists(frt_l_ctrl):
        list_to_bake.append(frt_l_ctrl)
    if cmds.objExists(rear_r_ctrl):
        list_to_bake.append(rear_r_ctrl)
    if cmds.objExists(rear_l_ctrl):
        list_to_bake.append(rear_l_ctrl)

    for obj in list_to_bake:
        (obj)


def create_ui(window_name, *kwargs):
    close_window(window_name)

    win_width = 600
    tmp_row_width = [win_width * 0.3, win_width * 0.4, win_width * 0.3]

    window = cmds.window(
        window_name,
        title="motion path tool",
        width=win_width,
    )

    main_layout = cmds.columnLayout()
    main_raw_layout = cmds.rowLayout(
        w=win_width,
        numberOfColumns=1,
        columnWidth1=win_width,
        rowAttach=(2, "top", 0),
    )
    cmds.columnLayout(width=win_width)
    cmds.text(
        label="",
    )
    cmds.text(
        label="Controllers to track",
        font="boldLabelFont",
        align="center",
        w=win_width,
        backgroundColor=(1, 0.8, 1),
    )
    cmds.text(label="")

    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- Root control section ---
    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmp_row_width)

    # cmds.checkBox(
    #     label="Insert on 2's", parent=main_layout, changeCommand=on_checkbox_toggled
    # )
    lbl_store_root_ctrl = cmds.text(
        "Root name",
        label="Root name",
        align="center",
        width=tmp_row_width[0],
    )
    txt_store_root_ctrl = cmds.text(
        "Select Root ",
        label="Select control ",
        align="center",
        backgroundColor=(0.5, 1, 1),
        width=tmp_row_width[1],
    )

    btn_store_root_ctrl = cmds.button(
        "track root ",
        annotation="Select the root controller and press [track root ctrl]",
        width=tmp_row_width[2],
        command=partial(press_change_label, txt_store_root_ctrl),
    )

    cmds.setParent("..")

    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- hip control section ---

    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmp_row_width)

    lbl_store_hip_ctrl = cmds.text(
        "Hip name",
        label="Hip name",
        align="center",
        width=tmp_row_width[0],
    )
    txt_store_hip_ctrl = cmds.text(
        "Select Hip ",
        label="Select Hip ",
        align="center",
        backgroundColor=(0.5, 1, 1),
        width=tmp_row_width[1],
    )

    btn_store_hip_ctrl = cmds.button(
        "track hip ",
        annotation="Select the hip controller and press [track hip ctrl]",
        width=tmp_row_width[2],
        command=partial(
            press_change_label,
            txt_store_hip_ctrl,
        ),
    )
    cmds.setParent("..")

    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- chest control section ---

    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmp_row_width)

    lbl_store_chest_ctrl = cmds.text(
        "chest name",
        label="chest name",
        align="center",
        width=tmp_row_width[0],
    )
    txt_store_chest_ctrl = cmds.text(
        "Select chest",
        label="Select chest",
        align="center",
        backgroundColor=(0.5, 1, 1),
        width=tmp_row_width[1],
    )
    btn_store_chest_ctrl = cmds.button(
        "track chest ",
        annotation="Select the chest controller and press [track chest ctrl]",
        width=tmp_row_width[2],
        command=partial(press_change_label, txt_store_chest_ctrl),
    )

    cmds.setParent("..")
    cmds.button(
        "Build motion path",
        width=win_width,
        command=partial(
            press_build_mopath,
            txt_store_root_ctrl,
            txt_store_hip_ctrl,
            txt_store_chest_ctrl,
        ),
    )
    # cmds.setParent("..")

    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    main_raw_layout = cmds.rowLayout(
        w=win_width, numberOfColumns=1, columnWidth1=win_width, rowAttach=(2, "top", 0)
    )
    cmds.columnLayout(
        w=win_width
    )  # create a columnLayout under the first row of main_raw_layout
    cmds.text(label="")
    cmds.text(
        label="Paws controllers to track",
        font="boldLabelFont",
        align="center",
        w=win_width,
        backgroundColor=(1, 0.8, 1),
    )
    cmds.text(label="")
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- front Right control section ---

    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmp_row_width)

    lbl_store_front_right_ctrl = cmds.text(
        "front Right",
        label="front Right",
        align="center",
        width=tmp_row_width[0],
    )
    txt_front_right_ctrl = cmds.text(
        "Select front_right",
        label="Select front_right",
        align="center",
        backgroundColor=(0.5, 1, 1),
        width=tmp_row_width[1],
    )
    btn_store_front_right_ctrl = cmds.button(
        "track front_right ",
        annotation="Select the front_right controller and press [track front_right ctrl]",
        width=tmp_row_width[2],
        command=partial(press_change_label, txt_front_right_ctrl),
    )
    cmds.setParent("..")
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- front_left control section ---

    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmp_row_width)

    lbl_store_front_left_ctrl = cmds.text(
        "front_left",
        label="front_left",
        align="center",
        width=tmp_row_width[0],
    )
    txt_front_left_ctrl = cmds.text(
        "Select front_left",
        label="Select front_left",
        align="center",
        backgroundColor=(
            0.5,
            1,
            1,
        ),
        width=tmp_row_width[1],
    )
    btn_store_front_left_ctrl = cmds.button(
        "track front_left ",
        annotation="Select the front_left controller and press [track front_left ctrl]",
        width=tmp_row_width[2],
        command=partial(press_change_label, txt_front_left_ctrl),
    )
    cmds.setParent("..")
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- rear_right control section ---

    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmp_row_width)

    lbl_store_rear_right_ctrl = cmds.text(
        "rear_right",
        label="rear_right",
        align="center",
        width=tmp_row_width[0],
    )
    txt_rear_right_ctrl = cmds.text(
        "Select rear_right",
        label="Select rear_right",
        align="center",
        backgroundColor=(
            0.5,
            1,
            1,
        ),
        width=tmp_row_width[1],
    )
    btn_store_rear_right_ctrl = cmds.button(
        "track rear_right ",
        annotation="Select the rear_right controller and press [track rear_right ctrl]",
        width=tmp_row_width[2],
        command=partial(press_change_label, txt_rear_right_ctrl),
    )
    cmds.setParent("..")
    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- rear_left control section ---

    cmds.rowLayout(numberOfColumns=3, columnWidth3=tmp_row_width)

    lbl_store_rear_left_ctrl = cmds.text(
        "rear_left",
        label="rear_left",
        align="center",
        width=tmp_row_width[0],
    )
    txt_rear_left_ctrl = cmds.text(
        "Select rear_left",
        label="Select rear_left",
        align="center",
        backgroundColor=(
            0.5,
            1,
            1,
        ),
        width=tmp_row_width[1],
    )
    btn_store_rear_left_ctrl = cmds.button(
        "track rear_left ",
        annotation="Select the rear_left controller and press [track rear_left ctrl]",
        width=tmp_row_width[2],
        command=partial(press_change_label, txt_rear_left_ctrl),
    )
    cmds.setParent("..")
    cmds.button(
        "Bake to worldspace",
        width=win_width,
        command=partial(
            press_bake_to_worldspace,
            txt_front_right_ctrl,
            txt_front_left_ctrl,
            txt_rear_right_ctrl,
            txt_rear_left_ctrl,
        ),
    )
    cmds.setParent(
        ".."
    )  # this will exit the rowLayout back to the main_raw_layout, same as cmds.setParent(main_raw_layout)

    # ------------------------------------------------------------

    # ------------------------------------------------------------
    # --- bottom window section ---

    cmds.setParent(main_layout)  # set UI pointer back under the main columnLayout

    cmds.text(label="")
    cmds.separator()
    cmds.button(label="full window width button", width=win_width, height=40)

    cmds.showWindow(window)
    cmds.window(window, e=True, width=win_width, height=1)


def main():
    # UI

    create_ui(
        "mopathWindow",
    )
