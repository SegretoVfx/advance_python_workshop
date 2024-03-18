# ------------------------------------------------------------
# --- juls anim motion path ui ---
# Description = A ui providing easy to use motion trail for animators
#
# Please note that this tool was created during a training workshop and is
# has been solely done and tested for quadruped animation!
#
# Date   = 2024 - 03
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage =
# The purpose of this tool is to help animators to develop a cycle animation along
# an animation path.
# The root controller, the hip and the chest are following a motion path which
# can be edited. The animator can change the direction, motion or speed of the
# animation all in keeping the original cycle animation, up until the end of the
# process.
# Once the finale animation done, the controllers can be baked for a safer polish.
#
# The tool is composed with two files : juls_anim_motion_path_ui and
# juls_anim_motion_path_functions.
# Both need to be placed into the same folder, which its PATH needs to be listed
# into your Maya script paths,
#
# To launch the tool simply write and launch this lines onto Maya script editor:
#
#     import juls_anim_motion_path_ui
#     juls_anim_motion_path_ui.load()
#
#
# The Ui is supposed to open.
#
# --------------------------------------------------
# I'll explain all the Ui usage along with a theoretical example:
#
# You will have to start with a cycle animation looped into the quadruped rig
# you are using.
# Using the main root controller, give the character a rough blocking placing
# keys on the controller at certain time which seems to you relevant.
# You don't have to be super precise, but the more you place keys on the root
# controller and the more the tool will be precise.
# Once you are happy with this first pass, launch the Ui.
#
# > Select the root controller (the same you used to create the rough blocking)
# > On the juls_anim_motion_path_ui tool, under the ROOT tab
# >> press "track root".
#     The name of the selected controller will display above
# >> press "build path"
#     the motion path will be created but the controller won't be constraint yet.
#
#     Here you can choose where you want to display of hide some element of the
#     motion path, using the checkboxes.
#
# >> Under the "constraint Root to mopath option" section, you can attach or
#     snap the root controller to the motion path.
# >> Click on "attach root to mopath": The root will snap and follow the curve.
#     The animation speed should be approximately the same as you had before.
# >> You can decide to leave it as is and animate the rotation of the root
#     controller manually, or you can choose an orientation axis and click on "Aim
#     to front locator" (or "Aim to back locator") to have the root controller
#     anticipate the direction.
#
# > The options under the Hip and Chest tabs are based on the same pattern,
#     so you can go ahead and create the motion path for the hip and the chest,
#     following the same
#     steps as previously but selecting the Hip and Chest controllers.
#
# NOTE : You must keep the order ROOT > Hip > CHEST to create the paths as each
#     limb are created relative to the previous one.
#
# It is preferable to start by setting up all the motion paths and constraints
# before starting to adit the paths.
#
# Once you are cool with you motion, speed and direction:
# Under the Worldspace tab, you can create a worldspace locator which will
# constraint the selected controllers. Doing so allow you to have a controller
# following the worldspace rules to animate them "detached" from the original
# rig. This tool is pretty useful to snap the paws to the ground.
#
# >> Select all teh paws IK controllers
# >> click in "bake selection to worldspace".
# >> Now select the created locators and clean the animation as you would.
# >> Once you are happy with the animation of the paws, you can bake it back
# to the original controller:
# >> Select the controllers you want to bake to local space and click on
# "bake worldspace to controllers".
#
# You also have this option under the other tabs to bake all the parts back to
# their local space.
#
#
# ------------------------------------------------------------

import os
import importlib

from functools import partial

from PySide2 import QtWidgets, QtCore, QtUiTools
from shiboken2 import wrapInstance
from maya import cmds
from maya import OpenMayaUI as omui

import juls_anim_motion_path_functions as mop

importlib.reload(mop)

# ------------------------------------------------------------
# --- global variables ---
FILE_NAME = os.path.splitext(os.path.basename(__file__))[0]
PATH_UI = rf"{os.path.dirname(__file__)}\ui\{FILE_NAME}.ui"


# Keep window on top
def maya_main_window():
    """Return the Maya main window widget as a Python object"""
    main_window_pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_pointer), QtWidgets.QWidget)


class AnimMotionPath(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(AnimMotionPath, self).__init__(parent)

        # ------------------------------------------------------------
        # --- VARIABLES ---
        self.ui = None
        self.root_mopath = None
        self.root_molocs = None
        self.root_control = None
        self.root_worldspace_grp = None
        self.root_worldspace_loc = None
        self.root_molocs_mid_baked = None
        self.hip_molocs = None
        self.hip_mopath = None
        self.hip_control = None
        self.hip_worldspace_grp = None
        self.hip_worldspace_loc = None
        self.hip_molocs_mid_baked = None
        self.chest_mopath = None
        self.chest_molocs = None
        self.chest_control = None
        self.chest_worldspace_grp = None
        self.chest_worldspace_loc = None
        self.chest_molocs_mid_baked = None

        # ------------------------------------------------------------
        # --- INIT ---
        self.init_ui()
        self.create_connections()

    def init_ui(self):
        # load the ui - qtDesigner generated
        f = QtCore.QFile(PATH_UI)
        f.open(QtCore.QFile.ReadOnly)

        self.ui = QtUiTools.QUiLoader().load(f, parentWidget=self)
        f.close()

    def create_connections(self):
        """
        This is where the Ui buttons, checkbox, labels... are linked to the
        functions.
        :return: None
        """
        # ------------------------------------------------------------
        # --- ROOT TAB ---
        # ------------------------------------------------------------
        # --- MOTION PATH ---
        self.ui.btn_track_root.clicked.connect(
            partial(
                self.press_change_label,
                self.ui.lbl_root_ctrl_name,
            )
        )
        self.ui.btn_build_root_mopath.clicked.connect(
            self.build_root_mopath,
        )
        self.ui.checkbox_root_mopath.stateChanged.connect(
            self.toggle_root_mopath_visibility,
        )
        self.ui.checkbox_root_molocs.stateChanged.connect(
            self.toggle_root_molocs_visibility,
        )
        self.ui.checkbox_root_markers.stateChanged.connect(
            self.toggle_root_markers_visibility,
        )

        # ------------------------------------------------------------
        # --- CONSTRAINT ---
        self.ui.btn_constraint_root_to_mopath.setCheckable(True)
        self.ui.btn_constraint_root_to_mopath.toggled.connect(
            self.point_const_root_to_mid_moloc,
        )

        self.ui.btn_delete_root_constraints.clicked.connect(
            partial(
                self.delete_constraint,
                child=self.root_control,
                point=True,
                aim=True,
            )
        )
        # ---
        self.ui.btn_aim_root_axis_to_front.setCheckable(True)
        self.ui.btn_aim_root_axis_to_front.toggled.connect(
            partial(self.aim_root_to_front_molocs)
        )
        # ---
        self.ui.btn_aim_root_axis_to_tail.setCheckable(True)
        self.ui.btn_aim_root_axis_to_tail.toggled.connect(
            partial(self.aim_root_to_tail_molocs)
        )

        # ------------------------------------------------------------
        # --- bake ---
        self.ui.btn_bake_root_ctrl.clicked.connect(self.bake_root_ctrl)

        # ------------------------------------------------------------
        # --- HIP TAB ---
        # ------------------------------------------------------------
        # --- MOTION PATH ---
        self.ui.btn_track_hip.clicked.connect(
            partial(
                self.press_change_label,
                self.ui.lbl_hip_ctrl_name,
            )
        )
        self.ui.btn_build_hip_mopath.clicked.connect(
            self.build_hip_mopath,
        )
        self.ui.checkbox_hip_mopath.stateChanged.connect(
            self.toggle_hip_mopath_visibility,
        )
        self.ui.checkbox_hip_molocs.stateChanged.connect(
            self.toggle_hip_molocs_visibility,
        )
        self.ui.checkbox_hip_markers.stateChanged.connect(
            self.toggle_hip_markers_visibility,
        )

        # ------------------------------------------------------------
        # --- CONSTRAINT ---
        self.ui.btn_constraint_hip_to_mopath.setCheckable(True)
        self.ui.btn_constraint_hip_to_mopath.toggled.connect(
            self.point_const_hip_to_mid_moloc,
        )
        self.ui.btn_delete_hip_constraints.clicked.connect(
            cmds.delete(self.hip_worldspace_grp)
        )
        # ---
        self.ui.btn_aim_hip_axis_to_front.setCheckable(True)
        self.ui.btn_aim_hip_axis_to_front.toggled.connect(
            self.aim_hip_to_front_molocs,
        )
        # ---
        self.ui.btn_aim_hip_axis_to_tail.setCheckable(True)
        self.ui.btn_aim_hip_axis_to_tail.toggled.connect(
            self.aim_hip_to_tail_molocs,
        )

        # ------------------------------------------------------------
        # --- bake ---
        self.ui.btn_bake_hip_ctrl.clicked.connect(self.bake_hip_ctrl)

        # ------------------------------------------------------------
        # --- CHEST TAB ---
        # ------------------------------------------------------------
        # --- MOTION PATH ---
        self.ui.btn_track_chest.clicked.connect(
            partial(
                self.press_change_label,
                self.ui.lbl_chest_ctrl_name,
            )
        )
        self.ui.btn_build_chest_mopath.clicked.connect(
            self.build_chest_mopath,
        )
        self.ui.checkbox_chest_molocs.stateChanged.connect(
            self.toggle_chest_molocs_visibility,
        )
        self.ui.checkbox_chest_markers.stateChanged.connect(
            self.toggle_chest_markers_visibility,
        )

        # ------------------------------------------------------------
        # --- CONSTRAINT ---
        self.ui.btn_constraint_chest_to_mopath.setCheckable(True)
        self.ui.btn_constraint_chest_to_mopath.toggled.connect(
            self.point_const_chest_to_mid_moloc,
        )
        self.ui.btn_delete_chest_constraints.clicked.connect(
            cmds.delete(self.chest_worldspace_grp)
        )
        # ---
        self.ui.btn_aim_chest_axis_to_front.setCheckable(True)
        self.ui.btn_aim_chest_axis_to_front.toggled.connect(
            partial(self.aim_chest_to_front_molocs)
        )
        # ---
        self.ui.btn_aim_chest_axis_to_tail.setCheckable(True)
        self.ui.btn_aim_chest_axis_to_tail.toggled.connect(
            partial(self.aim_chest_to_tail_molocs)
        )

        # ------------------------------------------------------------
        # --- bake ---
        self.ui.btn_bake_chest_ctrl.clicked.connect(self.bake_chest_ctrl)

        # ------------------------------------------------------------
        # --- WORLDSPACE TAB ---
        # ------------------------------------------------------------

        # --- BAKE TO WORLD ---
        self.ui.btn_bake_to_worldspace.clicked.connect(
            self.bake_selection_to_worldspace,
        )
        # ------------------------------------------------------------
        # --- BAKE TO CONTROL ---
        self.ui.btn_bake_to_controller.clicked.connect(
            self.bake_worldspace_to_controller
        ),

    # ------------------------------------------------------------
    # --- EXEC FUNCTIONS ---
    # ------------------------------------------------------------
    # --- toggle ---
    # --- ROOT ---
    def toggle_root_mopath_visibility(self):
        mop.toggle_mopath_visibility(
            self.root_mopath, self.ui.checkbox_root_mopath.isChecked()
        )

    def toggle_root_molocs_visibility(self):
        mop.toggle_molocs_visibility(
            self.root_molocs, self.ui.checkbox_root_molocs.isChecked()
        )

    def toggle_root_markers_visibility(self):
        mop.toggle_markers_visibility(
            self.root_mopath, self.ui.checkbox_root_markers.isChecked()
        )

    # --- HIP ---
    def toggle_hip_mopath_visibility(self):
        mop.toggle_mopath_visibility(
            self.hip_mopath, self.ui.checkbox_hip_mopath.isChecked()
        )

    def toggle_hip_molocs_visibility(self):
        mop.toggle_molocs_visibility(
            self.hip_molocs, self.ui.checkbox_hip_molocs.isChecked()
        )

    def toggle_hip_markers_visibility(self):
        mop.toggle_markers_visibility(
            self.hip_mopath, self.ui.checkbox_hip_markers.isChecked()
        )

    # --- CHEST ---

    def toggle_chest_molocs_visibility(self):
        mop.toggle_molocs_visibility(
            self.chest_molocs, self.ui.checkbox_chest_molocs.isChecked()
        )

    def toggle_chest_markers_visibility(self):
        mop.toggle_markers_visibility(
            self.hip_mopath, self.ui.checkbox_chest_markers.isChecked()
        )

    # ------------------------------------------------------------
    # --- BAKE FUNCTION CALL ---
    def bake_selection_to_worldspace(self):
        """
        Transfer the current animation to a locator place under a group.
        Every time you'll use this function, the created group will be placed
        under the same global group for convenience.
        :return:None
        """
        parent_grp = "master_worldspace_grp"

        selections = cmds.ls(sl=True)

        bake_on_one = self.ui.checkbox_bake_on_one.isChecked()
        for selection in selections:
            sel_grp = f"{selection}_worldspace_grp"
            sel_loc = f"{selection}_worldspace_loc"

            mop.bake_to_worldspace(selection, sel_grp, sel_loc, bake_on_one)

            mop.group_children(parent_grp, [sel_grp])

    def bake_worldspace_to_controller(self):
        """
        Transfer the animation back from the worldspace locator (created with
        the above function) to the selected controller.
        :return:None
        """
        controllers = cmds.ls(sl=True)

        bake_on_one = self.ui.checkbox_bake_on_one.isChecked()
        for controller in controllers:
            mop.bake_anim(controller, bake_on_one)
            cmds.delete(f"{controller}_worldspace_grp")

    def bake_root_ctrl(self):
        """
        Transfer the animation from the motion path back to the root controller
        specifically
        :return:None
        """
        bake_on_one = self.ui.cb_bake_root_on_one.isChecked()
        mop.bake_anim(self.root_control, bake_on_one)
        cmds.delete(self.root_worldspace_grp)

    def bake_hip_ctrl(self):
        """
        Transfer the animation from the motion path back to the hip controller
        specifically
        :return:None
        """
        bake_on_one = self.ui.cb_bake_hip_on_one.isChecked()
        mop.bake_anim(self.hip_control, bake_on_one)
        cmds.delete(self.hip_worldspace_grp)

    def bake_chest_ctrl(self):
        """
        Transfer the animation from the motion path back to the chest controller
        specifically
        :return:None
        """
        bake_on_one = self.ui.cb_bake_chest_on_one.isChecked()
        mop.bake_anim(self.chest_control, bake_on_one)
        cmds.delete(self.chest_worldspace_grp)

    # ------------------------------------------------------------
    # --- BUILD ---
    def build_root_mopath(self):
        """
        Create the motion pass for the root controller
        Create the motion path locators (used for snapping the controller)
        create the class variables
        update the Ui to display the controller's name, and change the color
        of the label.
        :return:None
        """
        # set variables based on the controller's name
        self.root_control = self.ui.lbl_root_ctrl_name.text()
        self.root_mopath = f"{self.root_control}_mopath"
        self.root_molocs = mop.build_moloc_structure(self.root_control, 1)
        self.root_molocs_mid_baked = self.root_molocs["mid"]["baked"][2]
        mop.press_root_track_process(
            self.root_control,
            self.root_mopath,
            self.root_molocs,
        )
        self.ui.btn_build_root_mopath.setStyleSheet(
            "QPushButton {background-color: #282a36; color: #000}"
        )
        self.ui.btn_build_root_mopath.setText("Path built")

    def build_hip_mopath(self):
        """
        Create the motion pass for the hip controller
        Create the motion path locators (used for snapping the controller)
        create the class variables
        update the Ui to display the controller's name, and change the color
        of the label.
        :return:None
        """
        # set variables based on the controller's name
        self.hip_control = self.ui.lbl_hip_ctrl_name.text()
        self.hip_mopath = f"{self.hip_control}_mopath"
        self.hip_molocs = mop.build_moloc_structure(self.hip_control, 0.05)
        self.hip_molocs_mid_baked = self.hip_molocs["mid"]["baked"][2]
        mop.press_hip_track_process(
            self.hip_control,
            self.hip_mopath,
            self.hip_molocs,
            self.root_mopath,
        )
        self.ui.btn_build_hip_mopath.setStyleSheet(
            "QPushButton {background-color: #282a36; color: #000}"
        )
        self.ui.btn_build_hip_mopath.setText("Path built")

    def build_chest_mopath(self):
        """
        Create the motion pass for the chest controller
        Create the motion path locators (used for snapping the controller)
        create the class variables
        update the Ui to display the controller's name, and change the color
        of the label.
        :return:None
        """
        self.chest_control = self.ui.lbl_chest_ctrl_name.text()
        self.chest_mopath = f"{self.chest_control}_mopath"
        self.chest_molocs = mop.build_moloc_structure(self.chest_control, 0.05)
        self.chest_molocs_mid_baked = self.chest_molocs["mid"]["baked"][2]
        mop.press_chest_track_process(
            self.chest_control,
            self.hip_mopath,
            self.chest_molocs,
        )
        self.ui.btn_build_chest_mopath.setStyleSheet(
            "QPushButton {background-color: #282a36; color: #000}"
        )
        self.ui.btn_build_chest_mopath.setText("Path built")

    def point_const_root_to_mid_moloc(self, checked):
        """
        Snap the root controller to the locator attached to motion path.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        time_min, _ = mop.get_playback_info()
        cmds.currentTime(time_min)
        if checked:
            # create worldspace_locator for all selected controllers
            self.root_worldspace_grp = f"{self.root_control}_worldspace_grp"
            self.root_worldspace_loc = f"{self.root_control}_worldspace_loc"
            # Create the worldspace locators
            cmds.spaceLocator(n=self.root_worldspace_loc)
            cmds.group(
                self.root_worldspace_loc,
                name=self.root_worldspace_grp,
            )
            # bake hip animation to a group and parent to moloc:
            mop.point_const(
                self.root_worldspace_loc,
                self.root_control,
            )

            mop.point_const(
                self.root_molocs["mid"]["baked"][2],
                self.root_worldspace_grp,
            )

        else:
            cmds.delete(self.root_worldspace_grp)

    def point_const_hip_to_mid_moloc(self, checked):
        """
        Snap the hip controller to the locator attached to motion path.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        time_min, _ = mop.get_playback_info()
        cmds.currentTime(time_min)
        if checked:
            # create worldspace_locator for all selected controllers
            self.hip_worldspace_grp = f"{self.hip_control}_worldspace_grp"
            self.hip_worldspace_loc = f"{self.hip_control}_worldspace_loc"
            # bake hip animation to a group and parent to moloc
            mop.bake_to_mopath(
                self.hip_control,
                self.hip_molocs["mid"]["baked"][2],
                self.hip_worldspace_grp,
                self.hip_worldspace_loc,
            )

        else:
            cmds.delete(self.hip_worldspace_grp)

    def point_const_chest_to_mid_moloc(self, checked):
        """
        Snap the chest controller to the locator attached to motion path.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        if checked:
            # create worldspace_locator for all selected controllers
            self.chest_worldspace_grp = f"{self.chest_control}_worldspace_grp"
            self.chest_worldspace_loc = f"{self.chest_control}_worldspace_loc"
            # bake hip animation to a group and parent to moloc
            mop.bake_to_mopath(
                self.chest_control,
                self.chest_molocs["mid"]["baked"][2],
                self.chest_worldspace_grp,
                self.chest_worldspace_loc,
            )

        else:
            cmds.delete(self.chest_worldspace_grp)

    def aim_root_to_front_molocs(self, checked):
        """
        aim the root toward the position of the front locator according to
        the axis selected in the drop-down menu.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        if checked:
            # remove previous aim constraint to tail moloc if any
            if self.query_aim_orient(self.ui.btn_aim_root_axis_to_tail):
                self.delete_constraint(child=self.root_control, point=False, aim=True)
                self.ui.btn_aim_root_axis_to_tail.setChecked(False)

            axis = self.ui.cb_aim_root_axis_to_front.currentText()
            mop.aim_const(
                self.root_molocs["front"]["baked"][2],
                self.root_control,
                axis,
            )
        else:
            self.delete_constraint(child=self.root_control, point=False, aim=True)

    def aim_root_to_tail_molocs(self, checked):
        """
        aim the root toward the position of the tail locator according to
        the axis selected in the drop-down menu. use to have the character
        going backward.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        if checked:
            # remove previous aim constraint to front moloc if any
            if self.query_aim_orient(self.ui.btn_aim_root_axis_to_front):
                self.delete_constraint(child=self.root_control, point=False, aim=True)
                self.ui.btn_aim_root_axis_to_front.setChecked(False)

            axis = self.ui.cb_aim_root_axis_to_tail.currentText()
            mop.aim_const(
                self.root_molocs["tail"]["baked"][2],
                self.root_control,
                axis,
            )
        else:
            self.delete_constraint(child=self.root_control, point=False, aim=True)

    def aim_hip_to_front_molocs(self, checked):
        """
        aim the hip toward the position of the front locator according to
        the axis selected in the drop-down menu.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        if checked:
            # remove previous aim constraint to tail moloc if any
            if self.query_aim_orient(self.ui.btn_aim_hip_axis_to_tail):
                self.delete_constraint(
                    child=self.hip_worldspace_grp, point=False, aim=True
                )
                self.ui.btn_aim_hip_axis_to_tail.setChecked(False)

            axis = self.ui.cb_aim_hip_axis_to_front.currentText()
            mop.aim_const(
                self.hip_molocs["front"]["baked"][2],
                self.hip_molocs["mid"]["baked"][2],
                axis,
            )
        else:
            self.delete_constraint(child=self.hip_worldspace_grp, point=False, aim=True)

    def aim_hip_to_tail_molocs(self, checked):
        """
        aim the hip toward the position of the tail locator according to
        the axis selected in the drop-down menu. use to have the character
        going backward.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        if checked:
            # remove previous aim constraint to front moloc if any
            if self.query_aim_orient(self.ui.btn_aim_hip_axis_to_front):
                self.delete_constraint(
                    child=self.hip_worldspace_grp, point=False, aim=True
                )
                self.ui.btn_aim_hip_axis_to_front.setChecked(False)

            axis = self.ui.cb_aim_hip_axis_to_tail.currentText()
            mop.aim_const(
                self.hip_molocs["tail"]["baked"][2],
                self.hip_molocs["mid"]["baked"][2],
                axis,
            )
        else:
            self.delete_constraint(child=self.hip_worldspace_grp, point=False, aim=True)

    def aim_chest_to_front_molocs(self, checked):
        """
        aim the chest toward the position of the front locator according to
        the axis selected in the drop-down menu.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        if checked:
            # remove previous aim constraint to tail moloc if any
            if self.query_aim_orient(self.ui.btn_aim_chest_axis_to_tail):
                self.delete_constraint(child=self.chest_control, point=False, aim=True)
                self.ui.btn_aim_chest_axis_to_tail.setChecked(False)

            axis = self.ui.cb_aim_chest_axis_to_front.currentText()
            mop.aim_const(
                self.chest_molocs["front"]["baked"][2],
                self.chest_molocs["mid"]["baked"][2],
                axis,
            )
        else:
            self.delete_constraint(
                child=self.chest_molocs["mid"]["baked"][2],
                point=False,
                aim=True,
            )

    def aim_chest_to_tail_molocs(self, checked):
        """
        aim the hip toward the position of the tail locator according to
        the axis selected in the drop-down menu. use to have the character
        going backward.
        :param checked: Bool, detect if ui button is checked
        :return:None
        """
        if checked:
            # remove previous aim constraint to front moloc if any
            if self.query_aim_orient(self.ui.btn_aim_chest_axis_to_front):
                self.delete_constraint(child=self.chest_control, point=False, aim=True)
                self.ui.btn_aim_chest_axis_to_front.setChecked(False)

            axis = self.ui.cb_aim_chest_axis_to_tail.currentText()
            mop.aim_const(
                self.chest_molocs["tail"]["baked"][2],
                self.chest_molocs["mid"]["baked"][2],
                axis,
            )
        else:
            self.delete_constraint(
                child=self.chest_molocs["mid"]["baked"][2],
                point=False,
                aim=True,
            )

    # ------------------------------------------------------------
    # --- FUNCTIONS ---
    def press_change_label(self, label_to_change):
        """
        Action to change the label displaying the name of the controller
        :param label_to_change: Object, the class of the label to change
        :return:None
        """
        new_label = mop.get_selection_list()[0]
        label_to_change.setText(new_label)
        label_to_change.setStyleSheet(
            "QLabel {background-color: #d0c858; " "color: #000}",
        )

    # --- call to  Delete constraint function ---
    def delete_constraint(self, child, point, aim):
        """
        Delete the point or aim constraint of the node
        :param child: Obj, constrained object to unconstrain
        :param point: Bool, Delete point constraint if true, else don't delete.
        :param aim: Bool, Delete aim constraint if true, else don't delete.
        :return:None
        """
        mop.delete_constraint(child, point, aim)

    def query_aim_orient(self, checkbox_to_query):
        return checkbox_to_query.isChecked()


def load():
    global anim_mopath_ui

    # close existing instance of the ui
    try:
        print("helo")
        anim_mopath_ui.close()
        anim_mopath_ui.deleteLater()
        print("helo")
    except (RuntimeError, TypeError, NameError):
        pass
    anim_mopath_ui = AnimMotionPath()
    anim_mopath_ui.show()
