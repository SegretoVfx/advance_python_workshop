"""
#####################################################################################
#######                        Wes Scene Setup                                #######
#####################################################################################

    v1.7 - custom gravity ball settings

    v1.6 - fast/slow switching is based on reference files.  Set up to be editable by animator.

    v1.5 - Changing snap to to be able to do multiple objects.

    v1.4 - snapTo is updated - trying to skip certain attributes
         - Added right-click rotate and translate

    v1.3 - fix snapTo when keyed. so that it will drop a key on each attribute.

    v1.2 - change gravityBall button

    v1.1 - change gravity ball to a calculated script.

    v1.0 - First basic tools for scene Setup

    Any questions please contact me at heywesley@gmail.com

"""
import maya.cmds as cmds
import maya.mel as mel
import json


import py.wesTools.wesUtils

from py.wesTools.wesUtils import setActiveWindow
from py.wesTools.wesUtils import chosenModifiers


# "Setup"
def wesCreateLayer():
    selected = cmds.ls(sl=True)

    layer_lock = False
    layer_visible = True

    # Shift key is on
    if chosenModifiers(kind="Shift") == True:
        layer_lock = True

    # Ctrl Key is On
    if chosenModifiers(kind="Ctrl") == True:
        layer_visible = False

    result = cmds.promptDialog(
        title="Layer Name",
        message="Layer Name without _lyr:",
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel",
    )

    if result == "OK":
        input_name = cmds.promptDialog(query=True, text=True)
    else:
        input_name = selected[-1]

    layer_name = input_name + "_lyr"

    if layer_lock == True:
        disTyp = 2
    else:
        disTyp = 0

    the_layer = cmds.createDisplayLayer(selected, name=layer_name, noRecurse=True)
    cmds.setAttr(the_layer + ".visibility", layer_visible)
    cmds.setAttr(the_layer + ".displayType", disTyp)


def wesSimpleConstraint(cons_type):
    maintainOffsetChoice = True
    retain_selection = False
    # Shift key is on
    if chosenModifiers(kind="Shift") == True:
        retain_selection = True

    # Ctrl Key is On
    if chosenModifiers(kind="Ctrl") == True:
        maintainOffsetChoice = False

    objects_sel = cmds.ls(sl=True)
    master = objects_sel[1:]
    slave = objects_sel[:1]

    if cons_type == "point":
        cmds.pointConstraint(master, slave, maintainOffset=maintainOffsetChoice)

    if cons_type == "orient":
        cmds.orientConstraint(master, slave, maintainOffset=maintainOffsetChoice)

    if cons_type == "parent":
        cmds.parentConstraint(master, slave, maintainOffset=maintainOffsetChoice)

    if retain_selection == False:
        cmds.select(slave)


def wesGravity(
    speed, numFrames=49, velocity=-98.07, frame_rate=24, placement=0, frame=1001
):
    tmp_sphere = cmds.polySphere()[0]
    print(tmp_sphere)

    def gravCalculator(
        obj, numFrames=49, velocity=-98.07, frame_rate=24, placement=0, frame=1001
    ):
        grav = 98.07

        for time in range(numFrames):
            cmds.setKeyframe(obj, attribute="ty", value=placement, time=(frame, frame))

            final_velocity = velocity + (grav * (1.000 / frame_rate))
            displacement = 0.5 * (velocity + final_velocity) * (1.000 / frame_rate)
            velocity = final_velocity
            placement = placement - displacement
            frame = frame + 1

    if speed == "1sec":
        gravCalculator(tmp_sphere)
        cmds.setAttr(tmp_sphere + ".translateY", lock=True)

        cmds.rename(tmp_sphere, "OneFoot_Ball_1SecondDrop_16FeetHeight")
        cmds.select("OneFoot_Ball_1SecondDrop_16FeetHeight")

    if speed == "4sec":
        gravCalculator(tmp_sphere, numFrames=192, velocity=-392)
        cmds.setAttr(tmp_sphere + ".translateY", lock=True)
        cmds.setAttr(tmp_sphere + ".scaleX", 10)
        cmds.setAttr(tmp_sphere + ".scaleY", 10)
        cmds.setAttr(tmp_sphere + ".scaleZ", 10)

        cmds.rename(tmp_sphere, "ThreeFeet_Ball_4SecondDrop_257FeetHeight")
        cmds.select("ThreeFeet_Ball_4SecondDrop_257FeetHeight")

    if speed == "10sec":
        gravCalculator(tmp_sphere, numFrames=480, velocity=-980)
        cmds.setAttr(tmp_sphere + ".translateY", lock=True)
        cmds.setAttr(tmp_sphere + ".scaleX", 100)
        cmds.setAttr(tmp_sphere + ".scaleY", 100)
        cmds.setAttr(tmp_sphere + ".scaleZ", 100)

        cmds.rename(tmp_sphere, "SixFeet_Ball_10SecondDrop_1608FeetHeight")
        cmds.select("SixFeet_Ball_10SecondDrop_1608FeetHeight")

    if speed == "custom":
        gravCalculator(
            tmp_sphere,
            numFrames=numFrames,
            velocity=velocity,
            frame_rate=frame_rate,
            placement=placement,
            frame=frame,
        )
        cmds.rename(tmp_sphere, "wesGravityBall")
        cmds.select("wesGravityBall")


def wesGravityUI(user_width=200, user_height=20):
    if cmds.window("wesGravityUI", exists=True):
        cmds.deleteUI("wesGravityUI")
        cmds.windowPref("wesGravityUI", removeAll=True)

    wesRetimeUI = cmds.window(
        "wesGravityUI",
        title="Update the Character Values",
        sizeable=True,
        width=user_width,
        height=100,
    )
    cmds.showWindow(wesRetimeUI)
    parentWindow = "wesGravityUI"

    cmds.frameLayout("wesGravity UI Settings", lv=False, bv=False, mw=7, mh=7)

    # speed, numFrames=49, velocity=-98.07, frame_rate=24, placement=0, frame=1001

    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.text("Frame Rate:", width=user_width * 0.7)
    cmds.textField(
        "frameRateTextField",
        ed=True,
        width=user_width * 0.3,
        height=user_height * 1,
        text=24,
    )
    cmds.text("Velocity:", width=user_width * 0.7)
    cmds.textField(
        "velocityTextField",
        ed=True,
        width=user_width * 0.3,
        height=user_height * 1,
        text=-98.07,
    )
    cmds.text("placement:", width=user_width * 0.7)
    cmds.textField(
        "placementTextField",
        ed=True,
        width=user_width * 0.3,
        height=user_height * 1,
        text=0,
    )
    cmds.text("Starting Frame:", width=user_width * 0.7)
    cmds.textField(
        "startingFrameTextField",
        ed=True,
        width=user_width * 0.3,
        height=user_height * 1,
        text=1001,
    )
    cmds.text("Length of Frames:", width=user_width * 0.7)
    cmds.textField(
        "lengthFramesTextField",
        ed=True,
        width=user_width * 0.3,
        height=user_height * 1,
        text=49,
    )
    cmds.setParent("..")

    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(
        l="Create Custom Gravity Ball",
        command=lambda x: wesGravityUIRun(update=True),
        width=user_width * 0.8,
        height=user_height,
        bgc=[0.3, 0.6, 0.3],
    )
    cmds.button(
        l="Cancel",
        command=lambda x: wesGravityUIRun(update=False),
        width=user_width * 0.2,
        height=user_height,
        bgc=[0.6, 0.3, 0.3],
    )
    cmds.setParent("..")

    cmds.setParent("..")

    cmds.setParent("..")


def wesGravityUIRun(update):
    if update == False:
        cmds.deleteUI("wesGravityUI")
        cmds.windowPref("wesGravityUI", removeAll=True)
        return

    # speed, numFrames=49, velocity=-98.07, frame_rate=24, placement=0, frame=1001
    frame_rate = int(cmds.textField("frameRateTextField", q=True, text=True))
    velocity = float(cmds.textField("velocityTextField", q=True, text=True))
    placement = float(cmds.textField("placementTextField", q=True, text=True))
    frame = int(cmds.textField("startingFrameTextField", q=True, text=True))
    numFrames = int(cmds.textField("lengthFramesTextField", q=True, text=True))

    wesGravity(
        "custom",
        numFrames=numFrames,
        velocity=velocity,
        frame_rate=frame_rate,
        placement=placement,
        frame=frame,
    )

    cmds.deleteUI("wesGravityUI")
    cmds.windowPref("wesGravityUI", removeAll=True)


def fixPerspCamera():
    camera_name = mel.eval('findStartUpCamera( "persp" );')
    camera_new = cmds.camera(name="persp", hc="viewSet -p %camera")

    cmds.camera(camera_name, edit=True, startupCamera=False)
    cmds.delete("persp")
    cmds.setAttr(camera_new[0] + ".visibility", 0)
    cmds.rename(camera_new[0], "persp")
    cmds.camera("persp", edit=True, startupCamera=True)


"Misc"


def colorTicks(tick):
    if tick == "on":
        cmds.keyframe(tickDrawSpecial=1)
    if tick == "off":
        cmds.keyframe(tickDrawSpecial=0)
    setActiveWindow()


def toggleImageplane():
    # Find all viewports
    panels = cmds.getPanel(type="modelPanel")

    imageplanes = cmds.ls(type="cachedImagePlane")
    imageplanes.extend(cmds.ls(type="imagePlane"))

    if cmds.modelEditor(panels[0], q=True, imagePlane=True):
        for ea in panels:
            cmds.modelEditor(ea, e=True, imagePlane=0)
            cmds.modelEditor(ea, e=True, displayTextures=0)
        for im in imageplanes:
            cmds.setAttr(im + ".type", 1)

        if chosenModifiers(kind="Ctrl"):
            if cmds.objExists("env_lyr"):
                cmds.setAttr("env_lyr.visibility", 1)
            if cmds.objExists("anim_lyr"):
                cmds.setAttr("anim_lyr.visibility", 1)
            if cmds.objExists("daily_lyr"):
                cmds.setAttr("daily_lyr.visibility", 0)

    else:
        for ea in panels:
            cmds.modelEditor(ea, e=True, imagePlane=1)
            cmds.modelEditor(ea, e=True, displayTextures=1)
        for im in imageplanes:
            if ".MOV" in str(cmds.getAttr(im + ".imageName")).upper():
                cmds.setAttr(im + ".type", 2)
            else:
                cmds.setAttr(im + ".type", 0)

        if chosenModifiers(kind="Ctrl"):
            if cmds.objExists("env_lyr"):
                cmds.setAttr("env_lyr.visibility", 0)
            if cmds.objExists("anim_lyr"):
                cmds.setAttr("anim_lyr.visibility", 0)
            if cmds.objExists("daily_lyr"):
                cmds.setAttr("daily_lyr.visibility", 1)

    setActiveWindow()


def fastSlowUpdater(user_width=240, user_height=18):
    # {"slow": 2, "controller": "global_CTRL", "medium": 1, "attribute_name": "modelDisplayLevel", "fast": 0}

    # Find the file path
    script_path = __file__
    script_path = script_path.replace("\\", "/")
    script_path = script_path[: script_path.rindex("/") + 1]
    script_path += "wesSceneSetup_CHARACTER.json"

    # Read from Char File
    with open(script_path) as info_file:
        char_info = json.load(info_file)

    if cmds.window("fastSlowUpdater", exists=True):
        cmds.deleteUI("fastSlowUpdater")
        cmds.windowPref("fastSlowUpdater", removeAll=True)

    wesFastSlowUpdater = cmds.window(
        "fastSlowUpdater",
        title="Update the Character Values",
        sizeable=True,
        width=user_width,
        height=100,
    )
    cmds.showWindow(wesFastSlowUpdater)
    parentWindow = "fastSlowUpdater"

    cmds.frameLayout("fastSlow Updater", lv=False, bv=False, mw=7, mh=7)

    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.text("Controller Name:", width=user_width * 0.5)
    cmds.textField(
        "controllerTextField",
        ed=True,
        width=user_width * 0.5,
        height=user_height * 1,
        text=char_info["controller"],
    )
    cmds.text("Attribute Name:", width=user_width * 0.5)
    cmds.textField(
        "attributeTextField",
        ed=True,
        width=user_width * 0.5,
        height=user_height * 1,
        text=char_info["attribute_name"],
    )
    cmds.text("Fast Mode:", width=user_width * 0.5)
    cmds.textField(
        "fastTextField",
        ed=True,
        width=user_width * 0.5,
        height=user_height * 1,
        text=char_info["fast"],
    )
    cmds.text("Medium Mode:", width=user_width * 0.5)
    cmds.textField(
        "mediumTextField",
        ed=True,
        width=user_width * 0.5,
        height=user_height * 1,
        text=char_info["medium"],
    )
    cmds.text("Slow Mode:", width=user_width * 0.5)
    cmds.textField(
        "slowTextField",
        ed=True,
        width=user_width * 0.5,
        height=user_height * 1,
        text=char_info["slow"],
    )
    cmds.setParent("..")

    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(
        l="Save Settings",
        command=lambda x: fastSlowWriter(script_path, update=True),
        width=user_width * 0.5,
        height=user_height,
        bgc=[0.3, 0.6, 0.3],
    )
    cmds.button(
        l="Cancel",
        command=lambda x: fastSlowWriter(script_path, update=False),
        width=user_width * 0.5,
        height=user_height,
        bgc=[0.6, 0.3, 0.3],
    )
    cmds.setParent("..")

    cmds.setParent("..")

    cmds.setParent("..")


def fastSlowWriter(script_path, update):
    if update == False:
        cmds.deleteUI("fastSlowUpdater")
        cmds.windowPref("fastSlowUpdater", removeAll=True)
        return

    attr_name = cmds.textField("attributeTextField", q=True, text=True)
    if "." in attr_name:
        attr_name = attr_name.replace(".", "")

    char_info = {
        "controller": cmds.textField("controllerTextField", q=True, text=True),
        "attribute_name": attr_name,
        "fast": cmds.textField("fastTextField", q=True, text=True),
        "medium": cmds.textField("mediumTextField", q=True, text=True),
        "slow": cmds.textField("slowTextField", q=True, text=True),
    }

    print(char_info)

    # Write to Char File
    with open(script_path, "w") as info_file:
        json.dump(char_info, info_file)

    cmds.deleteUI("fastSlowUpdater")
    cmds.windowPref("fastSlowUpdater", removeAll=True)


def fastSlowSwitcher(user_mode):
    """This will toggle all rigPuppets in the scene to switch fast and slow"""

    # Ctrl Key is On, set to medium
    if chosenModifiers(kind="Ctrl") == True:
        user_mode = "medium"

    # Find the file path
    script_path = __file__
    script_path = script_path.replace("\\", "/")
    script_path = script_path[: script_path.rindex("/") + 1]
    script_path += "wesSceneSetup_CHARACTER.json"

    # Read from Char File
    with open(script_path) as info_file:
        char_info = json.load(info_file)

    reference_objs = cmds.ls(references=True)

    for ref_obj in reference_objs:
        # Check if the reference is loaded or not before continueing
        if cmds.referenceQuery(ref_obj, isLoaded=True):
            name_space = cmds.referenceQuery(ref_obj, namespace=True)

            # #Remove weird ":" at the start of the name space...
            # if name_space[0] == ":":
            #     name_space = name_space[1:]
            print(name_space)

            try:
                cmds.setAttr(
                    name_space
                    + ":"
                    + char_info["controller"]
                    + "."
                    + char_info["attribute_name"],
                    int(char_info[user_mode]),
                )
            except:
                print(
                    "Unable to switch spaces... Are you sure this is the attribute you want to update? --> "
                    + name_space
                    + ":"
                    + char_info["controller"]
                    + "."
                    + char_info["attribute_name"]
                )

    # Viewport settings
    viewports = cmds.getPanel(type="modelPanel")

    if user_mode == "fast":
        for vp in viewports:
            cmds.modelEditor(vp, edit=True, rendererName="base_OpenGL_Renderer")

    for vp in viewports:
        if "_camera" in cmds.modelEditor(vp, q=True, camera=True):
            if chosenModifiers(kind="Shift") == True:
                cmds.modelEditor(vp, edit=True, rendererName="vp2Renderer")

    # #Old way of finding puppets
    # top_nodes =  cmds.ls(assemblies=True)
    # rig_puppets = [x for x in top_nodes if ":rp" in x]
    # for puppet in rig_puppets:
    #   global_ctrl = [x for x in cmds.listRelatives(puppet, children=True) if "global_CTRL" in x]
    #   try:
    #       cmds.setAttr(global_ctrl[0] + ".modelDisplayLevel", user_mode)
    #   except:
    #       print(str(puppet) + " and " + str(global_ctrl) + " did not have a switcher"

    setActiveWindow()


def snapTo(which="transrot"):
    # To snap to with constraints
    master = cmds.ls(sl=True)[-1:]
    slave = cmds.ls(sl=True)[:-1]

    if not slave:
        print("Select something to snap to! =)")
        return

    if len(slave) > 1:
        for each in slave:
            print("each slave = " + str(slave))
            snapToCommand(master, each, which)
        return
    else:
        snapToCommand(master[0], slave[0], which)


def snapToCommand(master, slave, which):
    print("master:  " + str(master))
    print("slave:  " + str(slave))

    transManips = [".translateX", ".translateY", ".translateZ"]
    rotsManips = [".rotateX", ".rotateY", ".rotateZ"]

    trans_skip = []
    rots_skip = []

    for tmanip in transManips:
        if not cmds.getAttr(slave + tmanip, settable=True):
            trans_skip.append(tmanip[-1:].lower())

    for rmanip in rotsManips:
        if not cmds.getAttr(slave + rmanip, settable=True):
            rots_skip.append(rmanip[-1:].lower())

    print("locked translates: " + str(trans_skip))
    print("locked rotates: " + str(rots_skip))

    if trans_skip == ["x", "y", "z"] and rots_skip == ["x", "y", "z"]:
        print("Translate and Rotates maybe locked or stuckeded!")
        cmds.headsUpMessage("Translate and Rotates maybe locked or stuckeded!", time=3)
        return

    if which == "transrot":
        temp_cns = cmds.parentConstraint(
            master,
            slave,
            skipTranslate=trans_skip,
            skipRotate=rots_skip,
            maintainOffset=False,
        )
    elif which == "trans":
        temp_cns = cmds.pointConstraint(
            master, slave, skip=trans_skip, maintainOffset=False
        )
    elif which == "rots":
        temp_cns = cmds.orientConstraint(
            master, slave, skip=rots_skip, maintainOffset=False
        )

    # Drop a keyframe if there is one
    print("ALL KEYFRAMES CURVES : " + str(cmds.keyframe(slave, query=True, name=True)))
    if cmds.keyframe(slave, query=True, name=True):
        for ea in cmds.keyframe(slave, query=True, name=True):
            if "translateX" in ea:
                cmds.setKeyframe(slave, attribute="tx")
                print("Added a keyframe for " + str(ea) + ".tx")
            if "translateY" in ea:
                cmds.setKeyframe(slave, attribute="ty")
                print("Added a keyframe for " + str(ea) + ".ty")
            if "translateZ" in ea:
                cmds.setKeyframe(slave, attribute="tz")
                print("Added a keyframe for " + str(ea) + ".tz")

            if "rotate" in ea:
                if "X" == ea[-1:]:
                    cmds.setKeyframe(slave, attribute="rx")
                    print("Added a keyframe for " + str(ea) + ".rx")
            if "rotate" in ea:
                if "Y" == ea[-1:]:
                    cmds.setKeyframe(slave, attribute="ry")
                    print("Added a keyframe for " + str(ea) + ".ry")
            if "rotate" in ea:
                if "Z" == ea[-1:]:
                    cmds.setKeyframe(slave, attribute="rz")
                    print("Added a keyframe for " + str(ea) + ".rz")

    cmds.delete(temp_cns)
    cmds.select(slave)


def UI(parentWindow=None, user_width=180, user_height=17, frameClosed=False):
    if not parentWindow:
        wesAnimToolsUI = cmds.window(
            "wesSceneSetupCustomUI",
            title="wes SceneSetup",
            sizeable=True,
            width=user_width,
        )
        cmds.showWindow(wesAnimToolsUI)
        parentWindow = "wesSceneSetupCustomUI"

    cmds.frameLayout(
        collapsable=True,
        label="Setup",
        collapse=frameClosed,
        parent=parentWindow,
        width=user_width,
    )

    cmds.rowColumnLayout(numberOfColumns=1)
    cmds.button(
        l="Create Layer",
        command=lambda x: wesCreateLayer(),
        width=user_width,
        height=user_height * 1.4,
        bgc=[0.9, 0.5, 0.5],
        annotation="Creates a display layer.  Shift=Lock.  Ctrl=Hide.",
    )
    cmds.button(
        l="Gravity Ball (Decimeters)",
        command=lambda x: wesGravity("1sec"),
        width=user_width,
        height=user_height,
        bgc=[0.2, 0.4, 0.3],
        annotation="Right-click for more options",
    )
    cmds.popupMenu()
    cmds.menuItem(
        l="Custom Settings",
        command=lambda x: wesGravityUI(),
        annotation="Make your own settings for the gravity ball",
    )
    cmds.menuItem(
        l="1 Sec",
        command=lambda x: wesGravity("1sec"),
        annotation="Creates a sphere with proper gravity applied in decimeters",
    )
    cmds.menuItem(
        l="4 Secs",
        command=lambda x: wesGravity("4sec"),
        annotation="Creates a sphere with proper gravity applied in decimeters",
    )
    cmds.menuItem(
        l="10 Secs",
        command=lambda x: wesGravity("10sec"),
        annotation="Creates a sphere with proper gravity applied in decimeters",
    )

    cmds.button(
        l="Fix Persp Cam",
        command=lambda x: fixPerspCamera(),
        width=user_width,
        height=user_height,
        annotation="If your persp camera is broken in anyway, this will make a fresh one",
    )
    cmds.setParent("..")

    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(
        l="Green Ticks",
        command=lambda x: colorTicks("on"),
        width=user_width * 0.5,
        height=user_height,
        bgc=[0, 0.4, 0],
        annotation="Adds special tick color in timeline to selected keys.",
    )
    cmds.button(
        l="Red Ticks",
        command=lambda x: colorTicks("off"),
        width=user_width * 0.5,
        height=user_height,
        bgc=[0.4, 0, 0],
        annotation="Removes special tick color in timeline to selected keys.",
    )

    cmds.separator(style="in", height=10)
    cmds.separator(style="in", height=10)

    cmds.button(
        l="Fast",
        command=lambda x: fastSlowSwitcher("fast"),
        width=user_width * 0.5,
        height=user_height * 1.5,
        bgc=[0.5, 0.95, 0],
        annotation="'CTRL' for medium / 'SHIFT' for VP2.0 on _camera",
    )
    cmds.popupMenu()
    cmds.menuItem(
        l="Change Default Naming Convention", command=lambda x: fastSlowUpdater()
    )
    cmds.button(
        l="Slow",
        command=lambda x: fastSlowSwitcher("slow"),
        width=user_width * 0.5,
        height=user_height * 1.5,
        bgc=[1, 0.4, 0.2],
        annotation="'CTRL' for medium / 'SHIFT' for VP2.0 on _camera",
    )
    cmds.popupMenu()
    cmds.menuItem(
        l="Change Default Naming Convention", command=lambda x: fastSlowUpdater()
    )

    cmds.setParent("..")

    cmds.rowColumnLayout(numberOfColumns=1)
    cmds.button(
        l="Imageplanes On/Off",
        command=lambda x: toggleImageplane(),
        width=user_width,
        height=user_height * 1.5,
        bgc=[0.9, 0.9, 0],
        annotation="if you create an 'env_lyr' in display layer. Hold 'CTRL' to hide the env_lyr and show imageplanes and vice versa.",
    )
    cmds.rowColumnLayout(numberOfColumns=1)

    cmds.setParent("..")
    cmds.button(
        l="Snap To",
        command=lambda x: snapTo(),
        width=user_width,
        height=user_height * 1.5,
        bgc=[0.5, 0.5, 0.5],
        annotation="Shift select object to snap to.  If there is a key it will key",
    )
    cmds.popupMenu()
    cmds.menuItem(l="Translate Only", command=lambda x: snapTo(which="trans"))
    cmds.menuItem(l="Rotates Only", command=lambda x: snapTo(which="rots"))
    cmds.setParent("..")

    cmds.rowColumnLayout(numberOfColumns=3)
    cmds.button(
        l="point",
        command=lambda x: wesSimpleConstraint("point"),
        width=user_width * 0.333,
        height=user_height,
        bgc=[0.4, 0.5, 0.5],
        annotation="Ctrl = Constrain without any offsets.",
    )
    cmds.button(
        l="orient",
        command=lambda x: wesSimpleConstraint("orient"),
        width=user_width * 0.333,
        height=user_height,
        bgc=[0.5, 0.4, 0.5],
        annotation="Ctrl = Constrain without any offsets.",
    )
    cmds.button(
        l="parent",
        command=lambda x: wesSimpleConstraint("parent"),
        width=user_width * 0.333,
        height=user_height,
        bgc=[0.5, 0.5, 0.4],
        annotation="Ctrl = Constrain without any offsets.",
    )
    cmds.setParent("..")

    cmds.setParent("..")
