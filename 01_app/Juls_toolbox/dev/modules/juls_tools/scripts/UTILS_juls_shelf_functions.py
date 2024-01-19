# SHELF  **************************************************************
# Description   = This creates the class needed for the shelf creation
# functions.
#
# File name     = juls_shelf_builder.py
# Date of birth = 1/10/2024
#
# Autor   = Juls
# Email   = segretovfx@gmail.com
#
# Usage = This will work only if used with this three other files:
#         juls_shelf_builder
#         juls_shelf_functions
#         juls_shelf_info
#
# *********************************************************************


# Import third-party modules
import maya.cmds as cmds
import pymel.core as pmc
import maya.mel as mel

import webbrowser


def kill_existing_app(windowName):
    """Kill the app if it's running.

    Args:
        windowName (str): Window object name of the app.
    """
    if cmds.window(windowName, exists=True, q=True):
        cmds.deleteUI(windowName)


def show_help():
    """
    Opens the Documentation of the script.
    """
    help_path = "https://wiki.pixomondo.com/en/departments/animation/internal_tools/camretarget"

    webbrowser.open(help_path, new=0, autoraise=True)


def load_cam():
    """
    Function for setting the text field meant for a camera
    Args:
        button_args=None: placeholder for arguments given by pressing a button
    """
    # try to get camera node
    cam = check_camera_name()
    # if it does not work, warn user & stop
    if cam is None:
        cmds.warning('No camera or viewport selected.')
        return
    # if cam was found, return the camera name
    return cam

def check_camera_name():
    """
    Function for returning the name of the selected camera
    either selectiong it`s shape, it`s tansform or a model panel (viewport)
    Args:
        None
    Returns:
        string: A string of the active camera
    """
    # get list of selected objects
    current_sel = cmds.ls(selection=True)
    # something selected, check first selected obj if valid
    if current_sel:
        obj_name = current_sel[0]
        # if it is a transform node
        if cmds.nodeType(obj_name) == 'transform':
            # get it's shapes
            shape = cmds.listRelatives(obj_name, shapes=True)
            # if it has shapes
            if shape:
                # check if the first shape is a camera, if so,
                # return transform and shape node
                if cmds.nodeType(shape[0]) == 'camera':
                    cam_transform = obj_name
                    cam_shape = shape
                    return [cam_transform, cam_shape]
                # if shape is no camera, try the active viewport
                else:
                    return check_viewport_cam()
            # if it doesn't have shapes, try the active viewport
            else:
                return check_viewport_cam()
        # if it is a camera, return its transform and shape
        elif cmds.nodeType(obj_name) == 'camera':
            cam_transform = cmds.listRelatives(obj_name, parent=True)[0]
            cam_shape = obj_name
            return [cam_transform, cam_shape]
        # if it neither a camera nor a transform, try the cative viewport
        else:
            return check_viewport_cam()
    # nothing selected, get active viewport
    else:
        return check_viewport_cam()

def check_viewport_cam():
    """
    Function for returning the name of the selected camera
    if that doesn`t work return the camera of the selected viewport
    otherwise return None
    Args:
        None
    Returns:
        string: A string containing the selected camera transform and
        it`s shape
    """
    # get camera name of active viewport
    cam_transform = get_active_viewport_cam()

    # check for its transform and shape, else return None
    if cam_transform:
        shape = cmds.listRelatives(cam_transform, shapes=True)
        if shape:
            return [cam_transform, shape[0]]
        else:
            return None
    else:
        return None

def get_active_viewport_cam():
    """
    Function for returning the camera of the active viewport if it is a
    model panel
    Args:
        None
    Returns:
        string: A string of the camera name if valid, otherwise None
    """
    # query active panel
    active_panel = cmds.getPanel(withFocus=True)

    # if it is a model panel retun the cam name, otherwies return None
    if cmds.getPanel(typeOf=active_panel) == 'modelPanel':
        cam = cmds.modelPanel(active_panel, query=True, camera=True)
        return cam
    else:
        return None

def validate_space_obj(sel=pmc.ls(sl=1)):
    # check if only a single object is selected
    if len(sel) == 1:
        # ToDo more error checking needs to be done
        return sel[0]
    else:
        pmc.warning("Please Select one Object only!")

def switch_cam_space(camera=None, source=None, target=None, use_point_constraint=False):

    # check if auto key is enabled, if yes > disable
    autokey_was_on = False



    # disable viewport
    mel.eval("paneLayout -e -manage false $gMainPane")

    if pmc.autoKeyframe(state=True, query=True):
        pmc.autoKeyframe(state=False)
        autokey_was_on = True

    # get current time slider range
    start_frame = pmc.playbackOptions(minTime=True, query=True)
    end_frame = pmc.playbackOptions(maxTime=True, query=True)

    if camera:
        # duplicate cam & keep original

        og_cam = pmc.PyNode(camera)
        cam_name = str(og_cam) + "_RETARGET"
        cam = pmc.duplicate(og_cam, ic=True, name=cam_name)

        # unlock all attributes of cam
        attr_list = pmc.listAttr(cam, locked=True)
        for attr in attr_list:
            pmc.setAttr(str(cam[0]) + "." + attr, lock=False)
    else:
        pmc.warning("Please select a valid camera first!")
        return
    if source:
        source_space_obj = pmc.PyNode(source)
    else:
        pmc.warning("Please select a valid source object first!")
        return
    if target:
        target_space_obj = pmc.PyNode(target)
    else:
        pmc.warning("Please select a valid target object first!")
        return
    # parent contraint a new locator to the original cam, and bake it's animation
    original_cam_loc_name = str(og_cam) + "_LOC"
    original_cam_loc = pmc.spaceLocator(name = original_cam_loc_name)

    og_cam_pc = pmc.parentConstraint(cam, original_cam_loc, maintainOffset=False)
    pmc.bakeResults(original_cam_loc, simulation=True, t=(start_frame, end_frame), dic=True)
    pmc.delete(og_cam_pc)

    # parent constraint a new locator to the source obj, and bake it's animation
    source_space_loc_name = str(source_space_obj) + "_LOC"
    source_space_loc = pmc.spaceLocator(name=source_space_loc_name)

    source_space_pc = pmc.parentConstraint(source_space_obj, source_space_loc, maintainOffset=False)
    pmc.bakeResults(source_space_loc, simulation=True, t=(start_frame, end_frame), dic=True)
    pmc.delete(source_space_pc)

    # parent the original cam under the source space locator
    pmc.parent(cam, source_space_loc)

    # parent constraint the cam to the og_cam locator and bake the animation -> cam is now in local space of the source obj
    cam_to_source_pc = pmc.parentConstraint(original_cam_loc, cam, maintainOffset=False)
    pmc.bakeResults(cam, simulation=True, t=(start_frame, end_frame), dic=True)
    pmc.delete(cam_to_source_pc)

    # create a new loc for the target space -> here the parentConstraint stays live
    target_space_loc_name = str(target_space_obj) + "_LOC"
    target_space_loc = pmc.spaceLocator(name=target_space_loc_name)

    # add an offset loc to the target one here
    target_offset_loc_name = str(target_space_obj) + "_offset_LOC"
    target_offset_loc = pmc.spaceLocator(name=target_offset_loc_name)
    pmc.parent(target_offset_loc, target_space_loc)
    target_space_pc = pmc.parentConstraint(target_space_obj, target_space_loc, maintainOffset=False)

    # finally parent constraint the source space loc to the target space offset loc
    # if use_point_constraint is on, use point instead of parent constraint
    if use_point_constraint:
        source_to_target_pc = pmc.pointConstraint(target_offset_loc, source_space_loc, maintainOffset=False)
    else:
        source_to_target_pc = pmc.parentConstraint(target_offset_loc, source_space_loc, maintainOffset=False)


    if autokey_was_on:
        pmc.autoKeyframe(state=True)

    # re activate viewport
    mel.eval("paneLayout -e -manage true $gMainPane")