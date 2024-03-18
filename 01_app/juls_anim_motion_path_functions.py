# ------------------------------------------------------------
# --- juls anim motion path functions ---
# Description = Functions required by juls_anim_motion_path script
#
# Date   = 2024 - 02
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage = import this module inside juls_anim_motion_path
#
# ------------------------------------------------------------


from maya import cmds


# ------------------------------------------------------------
# --- utilities functions ---


def deco_toggle_viewport(func):
    def wrapper(*args, **kwargs):
        # cmds.refresh(suspend=True)
        cmds.PauseViewportEval()
        func(*args, **kwargs)
        # cmds.refresh(suspend=False)
        cmds.PauseViewportEval()

    return wrapper


def delete_if_exists(obj: str):
    if cmds.objExists(obj):
        cmds.delete(obj)


def create_if_not_exists(node: str):
    if not cmds.objExists(node):
        cmds.group(name=node, empty=True)


def group_children(parent, children: list):
    """
    If the parent group does not exist/ then create it and place all the
    children under it
    :param parent: str, name of the parent group
    :param children: lst(str), list of all the children to place under parent
    :return:None
    """
    create_if_not_exists(parent)
    for child in children:
        cmds.parent(child, parent)


def change_outliner_color(obj, color=None):
    """
    Give a fancy look to the outliner after creation of the obj node
    :param obj: str, name of the node to change color into the outliner.
    :param color: [int,int,int], RGB value to give to the node in the outliner
    :return:None
    """
    if color is None:
        color = [1, 1, 1]
    cmds.setAttr(f"{obj}.useOutlinerColor", True)
    cmds.setAttr(f"{obj}.outlinerColor", color[0], color[1], color[2])


def toggle_mopath_visibility(mopath, *args):
    cmds.setAttr(f"{mopath}.visibility", args[0])


def toggle_molocs_visibility(molocs, *args):
    for place, _ in molocs.items():
        # for each moloc main group
        moloc = f"{molocs[place]['main'][0]}"

        cmds.setAttr(f"{moloc}.visibility", args[0])


def toggle_markers_visibility(mopath, *args):
    mopath_shape = cmds.listRelatives(
        mopath,
        children=True,
        fullPath=True,
    )
    markers = cmds.listRelatives(
        mopath_shape,
        children=True,
    )

    for marker in markers:
        cmds.setAttr(f"{mopath_shape[0]}->|{marker}.visibility", args[0])


# ------------------------------------------------------------
# --- data functions ---


def get_playback_info():
    time_min = cmds.playbackOptions(query=True, min=True)
    time_max = cmds.playbackOptions(query=True, max=True)

    return time_min, time_max


def get_selection_list():
    sel = cmds.ls(sl=True)
    if sel:
        return sel
    else:
        cmds.error("You must select a controller.")


def get_ctrl_position(control_name):
    pos_lst = []
    time_min, time_max = get_playback_info()

    cmds.select(control_name, replace=True)
    cmds.keyTangent(inTangentType="spline", outTangentType="spline")
    cmds.setInfinity(preInfinite="linear")
    cmds.setInfinity(postInfinite="linear")

    # Subtracts 20 frames at the start to have a longer motion path
    cmds.currentTime(time_min - 20, edit=True)
    trans = cmds.xform(control_name, query=True, translation=True)
    pos_lst.append(tuple(trans))

    # List all the frames with a translate key.
    keys_list = get_keyframes_list(control_name, "translate", time_min, time_max)

    for key in keys_list:
        cmds.currentTime(key, edit=True)
        trans = cmds.xform(control_name, query=True, translation=True)
        pos_lst.append(tuple(trans))

    # add 20 frame at the end to have a motion path longer than the frame range.
    cmds.currentTime(time_max + 20, edit=True)
    trans = cmds.xform(control_name, query=True, translation=True)
    pos_lst.append(tuple(trans))

    return pos_lst


def get_target_position_on_mopath(
    npoc_node,
    mopath_shape,
    target,
    time,
):
    """
    Track the position of the target along the motion path a current time,
    :param npoc_node: str, name of the nearestPositionOnCurve node
    :param mopath_shape: str, name of the motion path shape
    :param target: str, name of the object to localise along the curve
    :param time: int, keyframe to where to find nearest position.
    :return: float, U value of the target position along the curve
    """
    cmds.currentTime(time)
    # Snap a locator to the position of the target (to get WS pos)
    temp_loc = cmds.spaceLocator(n="temp_loc")[0]
    cmds.delete(cmds.parentConstraint(target, temp_loc))

    # Create a nearestPointOnCurve node and rename it
    npoc = cmds.createNode("nearestPointOnCurve", name=npoc_node)

    cmds.connectAttr(f"{temp_loc}.translateX", f"{npoc}.inPositionX")
    cmds.connectAttr(f"{temp_loc}.translateY", f"{npoc}.inPositionY")
    cmds.connectAttr(f"{temp_loc}.translateZ", f"{npoc}.inPositionZ")
    cmds.connectAttr(f"{mopath_shape[0]}.worldSpace[0]", f"{npoc}.inputCurve")

    # Get the output parameter value from the node
    param = cmds.getAttr(f"{npoc}.parameter")

    cmds.delete(npoc)
    cmds.delete(temp_loc)

    return param


def get_keyframes_list(node, attr, time_min, time_max):
    keys = list(
        dict.fromkeys(
            cmds.keyframe(
                node,
                query=True,
                attribute=attr,
                time=(time_min, time_max),
            )
        )
    )
    keys.sort()
    return keys


# ------------------------------------------------------------
# --- animation functions ---


def update_keyframes_values(node, attr, time_min, time_max, value):
    """
    Change the value of the given attribute
    :param node:str, name of the node to apply the change value
    :param attr: str, name of the attribute to change
    :param time_min: int, minimum time
    :param time_max: int, maximum time
    :param value: float, new value to give to the attribute
    :return: None
    """
    keys_list = get_keyframes_list(node, attr, time_min, time_max)

    for key in keys_list:
        cmds.keyframe(
            f"{node}.{attr}",
            edit=True,
            includeUpperBound=True,
            relative=True,
            option="over",
            valueChange=value,
            time=(int(key), int(key)),
        )


@deco_toggle_viewport
def bake_anim(ctrl, bake_on_one=True):
    """
    Bake the ctrl animation with simulation attribute set to True to remove
    constraint.
    :param ctrl: str, name of the controller to bake
    :param bake_on_one:  Bool, bake on one or bake on existing keys
    :return:None
    """
    time_min, time_max = get_playback_info()
    if bake_on_one:
        cmds.bakeResults(ctrl, time=(time_min, time_max), simulation=True)
    else:
        cmds.bakeResults(ctrl, time=(time_min, time_max), simulation=True, smart=True)


def bake_to_mopath(object_to_bake, parent_moloc, worldspace_grp, worldspace_loc):
    """
    Bake the controller animation to the mopath space and constraint
    to molocs
    :param object_to_bake: str, name of the object to bake
    :param parent_moloc:str, name of the moloc to use as parent
    :param worldspace_grp:str, name of the worldspace group
    :param worldspace_loc: str, name of the worldspace locator
    :return:None
    """

    # Create the worldspace locators
    cmds.group(name=worldspace_loc, empty=True)
    cmds.group(worldspace_loc, name=worldspace_grp)

    cmds.parentConstraint(
        parent_moloc,
        worldspace_grp,
        maintainOffset=False,
    )

    # constraint and bake the locator to the animated controller
    cmds.parentConstraint(
        object_to_bake,
        worldspace_loc,
        maintainOffset=False,
    )
    bake_anim(worldspace_loc)
    # delete the constraint between controllers and locators
    cmds.delete(
        cmds.listRelatives(
            worldspace_loc,
            type="constraint",
            fullPath=True,
        ),
    )

    # Constraint the controller to the worldspace
    cmds.parentConstraint(
        worldspace_loc,
        object_to_bake,
        maintainOffset=False,
    )


def bake_to_worldspace(
    object_to_bake,
    worldspace_grp,
    worldspace_loc,
    bake_on_one,
):
    """
    Transfer the animation to a locator in worldspace.
    :param object_to_bake:str, name of object to bake
    :param worldspace_grp:str, name of the worldspace group
    :param worldspace_loc:str, name of the worldspace locator
    :param bake_on_one:Bool,  Bool, bake on one or bake on existing keys
    :return: None
    """
    # Create the worldspace locators
    cmds.spaceLocator(n=worldspace_loc)
    cmds.group(worldspace_loc, n=worldspace_grp)

    # constraint the locator to the animated controller
    cmds.parentConstraint(object_to_bake, worldspace_loc, mo=False, w=1)

    # bake loci to save controllers animation
    bake_anim(worldspace_loc, bake_on_one)

    # delete the constraint between controllers and locators
    cmds.delete(
        cmds.listRelatives(
            worldspace_loc,
            type="constraint",
            fullPath=True,
        )
    )

    # Constraint the controller to the worldspace
    cmds.parentConstraint(worldspace_loc, object_to_bake, mo=False, w=1)


# ------------------------------------------------------------
# --- action functions ---


def build_moloc_structure(ctrl_name, size):
    """
    Build the hierarchy of groups and locators and put them into a
    dictionary for future use.
    :param ctrl_name: str, name of the controller for which to create the molocs
    :param size: float, Quotient of the size of the locators
    :return: dic{dic{lis[str]}}: Dictionary of all created molocs name
    """
    placements = {
        "front": 4,
        "mid": 13,
        "tail": 12,
    }
    molocs = {}

    def _build_hierarchy(placement, spot, color):
        grp = f"{ctrl_name}_moloc_{placement}_{spot}_grp"
        offset_grp = f"{ctrl_name}_moloc_{placement}_{spot}_offset"
        locator = f"{ctrl_name}_moloc_{placement}_{spot}_ctrl"

        delete_if_exists(grp)
        # the baked hierarchy is not selectable
        if spot == "main":
            cmds.spaceLocator(name=locator)
            cmds.setAttr(f"{locator}Shape.localScaleX", 1 * size)
            cmds.setAttr(f"{locator}Shape.localScaleY", 3 * size)
            cmds.setAttr(f"{locator}Shape.localScaleZ", 5 * size)
            cmds.setAttr(f"{locator}Shape.overrideEnabled", 1)
            cmds.setAttr(f"{locator}Shape.overrideColor", color)
        elif spot == "sub":
            cmds.circle(name=locator)
            cmds.setAttr(f"{locator}.visibility", 0)
            cmds.setAttr(f"{locator}Shape.overrideEnabled", 1)
            cmds.setAttr(f"{locator}Shape.overrideColor", color)
        elif spot == "baked":
            cmds.group(name=locator, empty=True)

        # Build offset hierarchy
        cmds.group(locator, name=offset_grp)
        cmds.group(offset_grp, name=grp)

        return grp, offset_grp, locator

    for place, col in placements.items():
        main_hierarchy = _build_hierarchy(place, "main", col)
        sub_hierarchy = _build_hierarchy(place, "sub", col)
        baked_hierarchy = _build_hierarchy(place, "baked", col)

        cmds.parent(sub_hierarchy[0], main_hierarchy[2])
        cmds.parent(baked_hierarchy[0], sub_hierarchy[2])

        # nested dictionary for molocs values
        molocs[place] = {}
        molocs[place].update({"main": main_hierarchy})
        molocs[place].update({"sub": sub_hierarchy})
        molocs[place].update({"baked": baked_hierarchy})

    return molocs


def match_moloc_to_target(
    mopath: str,
    molocs: dict,
    target: str,
    dist_secondary: float,
):
    """
    Align main moloc to controller nearest position on mopath
    :param mopath:str, name of mopath
    :param molocs: dic{dic{list[str]}}: dictionary of molocs name
    :param target: str, name of object to track
    :param dist_secondary: float, distance coefficient between secondary locators
    :return: none
    """

    time_min, time_max = get_playback_info()
    time_min = time_min - 20
    time_max = time_max + 20
    key_spread = 12

    # the constraint scrap the control position if not launched on first frame
    cmds.currentTime(time_min)

    for time in range(int(time_min), int(time_max), key_spread):
        for place, _ in molocs.items():
            moloc_main_grp = f"{molocs[place]['main'][0]}"
            node = f"{moloc_main_grp}_mopathnode"
            npoc_node = f"{molocs[place]['main'][0]}_npoc"
            mopath_shape = cmds.listRelatives(
                mopath,
                shapes=True,
                fullPath=True,
            )

            u_param = get_target_position_on_mopath(
                npoc_node,
                mopath_shape,
                target,
                time,
            )

            cmds.setAttr(f"{node}.uValue", u_param)
            cmds.setKeyframe(f"{node}.uValue", time=time)

    # Adjust moloc position on mopath

    moloc_front_grp = f"{molocs['front']['main'][0]}_mopathnode"
    moloc_tail_grp = f"{molocs['tail']['main'][0]}_mopathnode"

    update_keyframes_values(
        moloc_front_grp,
        "uValue",
        time_min,
        time_max,
        dist_secondary,
    )
    update_keyframes_values(
        moloc_tail_grp,
        "uValue",
        time_min,
        time_max,
        (-dist_secondary),
    )


def attach_moloc_to_mopath(path_name, molocs):
    """
    Snap constraint the moloc hierarchy to the mopath nearest position
    :param path_name:str, name of the motion path
    :param molocs: dic-str, Dictionary of molocs name
    :return: none
    """
    time_min, time_max = get_playback_info()
    time_min = time_min - 20
    time_max = time_max + 20

    for place, _ in molocs.items():
        mopath_node = f"{molocs[place]['main'][0]}_mopathnode"

        cmds.pathAnimation(
            molocs[place]["main"][0],
            name=mopath_node,
            fractionMode=False,
            follow=True,
            followAxis="x",
            upAxis="y",
            worldUpType="scene",
            startTimeU=time_min,
            endTimeU=time_max,
            curve=path_name,
        )

        cmds.keyTangent(
            mopath_node,
            inTangentType="spline",
            outTangentType="spline",
        )


def point_const(parent, child):
    """
    Delete previous Point constraint if any
    Then Create a point constraint between the child to the parent
    :param parent:str, name of the parent
    :param child:str, name of the child
    :return:None
    """

    # Delete former point constraint if any
    delete_constraint(child, point=True, aim=False)
    cmds.pointConstraint(parent, child, weight=1)


def aim_const(parent, child, axis):
    """
    Delete previous aim constraint if any
    Then Create an aim constraint between the child to the parent
    :param parent:str, name of the parent
    :param child:str, name of the child
    :param axis:str, aim vector axis
    :return:None
    """
    # Delete former aim constraint if any
    delete_constraint(child, point=False, aim=True)

    pointing_axis = {
        "X": (1, 0, 0),
        "Y": (0, 1, 0),
        "Z": (0, 0, 1),
        "-X": (-1, 0, 0),
        "-Y": (0, -1, 0),
        "-Z": (-1, 0, -1),
    }

    cmds.aimConstraint(
        parent,
        child,
        weight=1,
        aimVector=pointing_axis[axis],
        offset=(0, 0, 0),
        upVector=(0, 1, 0),
        worldUpType="vector",
        worldUpVector=(0, 1, 0),
    )


def delete_constraint(child, point=True, aim=True):
    """
    Delete the constraint if there's any
    for the point or aim constraint if set to True
    :param child:str, name of the node to remove the constraint
    :param point:Bool, True if you want to delete point constraint
    :param aim:Bool, True if you want to delete aim constraint
    :return:None
    """
    if aim:
        if cmds.aimConstraint(child, q=True) is not None:
            const = cmds.listRelatives(
                child,
                type="aimConstraint",
                fullPath=True,
            )
            cmds.delete(const)
    if point:
        if cmds.pointConstraint(child, q=True) is not None:
            const = cmds.listRelatives(
                child,
                type="pointConstraint",
                fullPath=True,
            )
            cmds.delete(const)


# ------------------------------------------------------------
# --- press button functions ---


@deco_toggle_viewport
def press_root_track_process(root_ctrl, root_mopath, root_molocs):
    """
    Launch the process to create the motion path for the root controller
    :param root_ctrl:str, name of the root controller
    :param root_mopath:str, name of the root motion path
    :param root_molocs:dic{dic{list(str)}}j, name of the root motion locators
    :return:none
    """
    root_ctrl_pos = get_ctrl_position(root_ctrl)

    delete_if_exists(root_mopath)
    cmds.curve(
        name=root_mopath,
        degree=2,
        point=root_ctrl_pos,
    )

    attach_moloc_to_mopath(root_mopath, root_molocs)
    match_moloc_to_target(root_mopath, root_molocs, root_ctrl, 1)

    parent_grp = "root_mopath_master"
    group_children(
        parent_grp,
        [
            root_mopath,
            root_molocs["front"]["main"][0],
            root_molocs["mid"]["main"][0],
            root_molocs["tail"]["main"][0],
        ],
    )
    change_outliner_color(parent_grp, [0.5, 0.5, 1])


@deco_toggle_viewport
def press_hip_track_process(hip_ctrl, hip_mopath, hip_molocs, root_mopath):
    """
    Launch the process to create the motion path for the hip controller
    :param hip_ctrl:str, name of the hip controller
    :param hip_mopath:str, name of the hip motion path
    :param hip_molocs:dic{dic{list(str)}}j, name of the hip motion locators
    :param root_mopath: name of the root motion path
    :return:None
    """
    hip_control_pos = cmds.xform(
        hip_ctrl,
        worldSpace=True,
        translation=True,
        query=True,
    )

    delete_if_exists(hip_mopath)
    cmds.duplicate(root_mopath, name=hip_mopath)
    cmds.xform(hip_mopath, t=[0, hip_control_pos[1], 0])

    attach_moloc_to_mopath(hip_mopath, hip_molocs)
    match_moloc_to_target(hip_mopath, hip_molocs, hip_ctrl, 0.05)

    parent_grp = "hip_mopath_master"
    group_children(
        parent_grp,
        [
            hip_mopath,
            hip_molocs["front"]["main"][0],
            hip_molocs["mid"]["main"][0],
            hip_molocs["tail"]["main"][0],
        ],
    )
    change_outliner_color(parent_grp, [0.5, 0.5, 1])


@deco_toggle_viewport
def press_chest_track_process(
    chest_ctrl,
    chest_mopath,
    chest_molocs,
):
    """
    Launch the process to create the motion path for the chest controller
    :param chest_ctrl:str, name of the chest controller
    :param chest_mopath:str, name of the chest motion path
    :param chest_molocs:dic{dic{list(str)}}j, name of the chest motion locators
    :return:none
    """
    attach_moloc_to_mopath(chest_mopath, chest_molocs)
    match_moloc_to_target(chest_mopath, chest_molocs, chest_ctrl, 0.05)

    parent_grp = "chest_mopath_master"
    group_children(
        parent_grp,
        [
            chest_molocs["front"]["main"][0],
            chest_molocs["mid"]["main"][0],
            chest_molocs["tail"]["main"][0],
        ],
    )
    change_outliner_color(parent_grp, [0.5, 0.5, 1])
