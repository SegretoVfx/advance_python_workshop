"""
#####################################################################################
#######                        Wes Image Planes                               #######
#####################################################################################
	To run, place script in scripts folder, then enter this python command:
	
	import wesImagePlanes
	reload(wesImagePlanes)
	wesImagePlanes.UI()
	
	v1.4b - reset Scale

	v1.4a - Supports .mov files

	v1.4 - creating Imageplane is now a drop down menu!
		 - Will say what imageplane depth it is


	v1.3 - Make Depth and Offsets Adjustment Dynamic
		 - Added reset button for X and Y when pressing right click.
		 - centerized the depth control

	v1.2 - added transparency UI feature

	v1.1 - Refined imagePlane setup to work with rest of the tools.  Cleaned up general things.



	v1.0 -  First build, to manage imageplanes attached to cameras


	Any questions please contact me at heywesley@gmail.com

"""


import maya.cmds as cmds
import maya.mel as mel
from functools import partial


def createIM(file_path="", im_name="", frame_offset=0, *args):
    # FilePath

    if not file_path:
        file_path = cmds.fileDialog(mode=0, title="Select ImageSequence")

    print("THIS IS THE FILE PATH!" + str(file_path))
    if file_path == "":
        return

    # Camera
    cameras_shape = cmds.ls(type="camera")
    cameras = []
    for ea in cameras_shape:
        cameras.extend(cmds.listRelatives(ea, parent=True))

    # Making camera selection with UI
    if cmds.window("wesCameraChooser", exists=True):
        cmds.deleteUI("wesCameraChooser")
        cmds.windowPref("wesCameraChooser", removeAll=True)

    user_width = 200
    user_height = 20

    wesCameraUI = cmds.window(
        "wesCameraChooser",
        title="Attach ImagePlane to...",
        sizeable=True,
        width=user_width,
        height=50,
    )
    cmds.showWindow(wesCameraUI)
    parentWindow = "wesCameraChooser"

    cmds.rowColumnLayout(numberOfColumns=1)

    cmds.separator(style="none", height=16)

    cmds.optionMenu("cameraChoices", label="Choose:")
    for camera in cameras:
        cmds.menuItem(label=camera)

    cmds.separator(style="none", height=8)

    cmds.setParent("..")

    cmds.rowColumnLayout(numberOfColumns=2)
    cmds.button(
        l="Cancel",
        command=lambda x: createIMPartTwo(update=False),
        width=user_width * 0.5,
        height=user_height,
        bgc=[0.6, 0.3, 0.3],
    )
    cmds.button(
        l="Choose This!",
        command=lambda x: createIMPartTwo(update=True),
        width=user_width * 0.5,
        height=user_height,
        bgc=[0.3, 0.6, 0.3],
    )
    cmds.setParent("..")

    cmds.textField("filePath", text=file_path, visible=False)
    cmds.textField("imName", text=im_name, visible=False)
    cmds.textField("frameOffset", text=frame_offset, visible=False)

    cmds.setParent("..")


def createIMPartTwo(update, *args):
    if update == False:
        if cmds.window("wesCameraChooser", exists=True):
            cmds.deleteUI("wesCameraChooser")
            cmds.windowPref("wesCameraChooser", removeAll=True)
        return

    # Find info from UI box
    file_path = cmds.textField("filePath", q=True, text=True)
    im_name = cmds.textField("imName", q=True, text=True)
    frame_offset = cmds.textField("frameOffset", q=True, text=True)
    choiceCam = cmds.optionMenu("cameraChoices", q=True, value=True)

    if cmds.window("wesCameraChooser", exists=True):
        cmds.deleteUI("wesCameraChooser")
        cmds.windowPref("wesCameraChooser", removeAll=True)

    # Imageplane Name
    if not im_name:
        result = cmds.promptDialog(
            title="imagePlane Name",
            message="Please name your ImagePlane:",
            button=["OK", "Cancel"],
            defaultButton="OK",
            cancelButton="Cancel",
            dismissString="Cancel",
        )
        if result == "OK":
            im_name = cmds.promptDialog(query=True, text=True)
            if im_name == "":
                im_name = "noNameImagePlane"
        else:
            return

    print(im_name)

    im_name = im_name + "_plate"

    createdImagePlane = cmds.imagePlane(
        camera=choiceCam,
        fileName=file_path,
        name=im_name,
        showInAllViews=False,
        lookThrough=choiceCam,
    )
    cmds.setAttr(createdImagePlane[0] + ".useFrameExtension", 1)
    cmds.setAttr(createdImagePlane[0] + ".displayOnlyIfCurrent", 1)
    cmds.setAttr(createdImagePlane[0] + ".fit", 2)

    # If its a .mov file, set it to type mov!
    if ".MOV" in str(file_path).upper():
        cmds.setAttr(createdImagePlane[0] + ".type", 2)

    cmds.rename(createdImagePlane[0], im_name)
    refreshList()

    # cmds.setAttr(im_name+".frameOffset", frame_offset)

    # cmds.textScrollList("listImagePlanes", selectItem=im_name)
    cmds.select(im_name)


def renameIM():
    try:
        theIM = cmds.textScrollList("listImagePlanes", query=True, selectItem=True)[0]
    except:
        cmds.confirmDialog(message="Please Select an imagePlane from the list")
        return

    result = cmds.promptDialog(
        title="imagePlane Name",
        message="Your new ImagePlane name:",
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel",
    )
    if result == "OK":
        im_name = cmds.promptDialog(query=True, text=True)
        if im_name == "":
            im_name = "noNameImagePlane"
    else:
        return
    print(im_name)

    im_name = im_name + "_plate"

    cmds.rename(theIM, im_name)
    refreshList()


def deleteIM():
    try:
        theIM = cmds.textScrollList("listImagePlanes", query=True, selectItem=True)[0]
    except:
        cmds.confirmDialog(message="Please Select an imagePlane from the list")
        return

    cmds.delete(theIM)
    refreshList()


def connectUI():
    theIM = cmds.textScrollList("listImagePlanes", query=True, selectItem=True)[0]

    if cmds.getAttr(theIM + ".displayMode") == 0:
        cmds.button(
            "IMvisibility", edit=True, label="Visibility Off", bgc=[0.4, 0.3, 0.3]
        )
    else:
        cmds.button(
            "IMvisibility", edit=True, label="Visibilty On", bgc=[0.3, 0.4, 0.3]
        )

    cmds.connectControl("offsetX", theIM + ".offsetX")
    cmds.connectControl("offsetY", theIM + ".offsetY")
    cmds.connectControl("sizeX", theIM + ".sizeY", theIM + ".sizeX")
    cmds.connectControl("depth", theIM + ".depth")

    updateSliders()

    cmds.select(theIM)


def updateSliders(depthChanger=False):
    theIM = cmds.textScrollList("listImagePlanes", query=True, selectItem=True)[0]
    attrs = [".depth", ".offsetX", ".offsetY", ".sizeX"]

    for attr in attrs:
        control_name = attr[1:]
        attr_val = cmds.getAttr(theIM + attr)
        if attr == ".depth":
            min_attr = attr_val / 10
            max_attr = (attr_val - min_attr) + attr_val
        elif attr == ".sizeX":
            min_attr = attr_val / 10
            max_attr = attr_val + 1
        else:
            min_attr = attr_val - 0.1
            max_attr = attr_val + 0.1

        cmds.floatSlider(control_name, edit=True, min=min_attr, max=max_attr)
        cmds.connectControl(control_name, theIM + attr)

    if depthChanger == True:
        depth_val = "Imageplane Depth:  " + str(cmds.getAttr(theIM + ".depth"))[:5]
        cmds.headsUpMessage(depth_val, time=0.5, vo=-250)


def visIM():
    try:
        theIM = cmds.textScrollList("listImagePlanes", query=True, selectItem=True)[0]
    except:
        cmds.confirmDialog(message="Please Select an imagePlane from the list")
        return

    # Turn it On
    if cmds.getAttr(theIM + ".displayMode") == 0:
        cmds.setAttr(theIM + ".displayMode", 3)

        # Check to see if its a .mov file
        if ".MOV" in str(cmds.getAttr(theIM + ".imageName")).upper():
            print("yes")
            cmds.setAttr(theIM + ".type", 2)
        else:
            cmds.setAttr(theIM + ".type", 0)

        cmds.button(
            "IMvisibility", edit=True, label="Visibilty On", bgc=[0.3, 0.4, 0.3]
        )

    # Turn it Off
    else:
        cmds.setAttr(theIM + ".displayMode", 0)
        cmds.setAttr(theIM + ".type", 1)

        cmds.button(
            "IMvisibility", edit=True, label="Visibility Off", bgc=[0.4, 0.3, 0.3]
        )


def refreshCache():
    imageplane_shapes = cmds.ls(type="imagePlane")
    imageplanes = []

    for ea in imageplane_shapes:
        imageplanes.extend(cmds.listRelatives(ea, parent=True))

    if not imageplanes == None:
        for im in imageplanes:
            orig_val = cmds.getAttr(im + ".frameCache")
            cmds.setAttr(im + ".frameCache", 0)
            cmds.setAttr(im + ".frameCache", orig_val)


def loadList():
    imageplane_shapes = cmds.ls(type="imagePlane")
    imageplanes = []

    for ea in imageplane_shapes:
        imageplanes.extend(cmds.listRelatives(ea, parent=True))

    if not imageplanes == None:
        for im in imageplanes:
            # Find only the imageplane name
            # short_im = im[im.rindex("->")+2:]
            # #Button for imageplane
            # print "Short Form ImagePlane:  "+ short_im

            cmds.textScrollList("listImagePlanes", edit=True, append=im)


def refreshList():
    cmds.textScrollList("listImagePlanes", edit=True, removeAll=True)
    loadList()


def transparencyUI(*args):
    user_width = 350
    user_height = 30

    try:
        theIM = cmds.textScrollList("listImagePlanes", query=True, selectItem=True)[0]
    except:
        cmds.confirmDialog(message="Please Select an imagePlane from the list")
        return

    transUI = theIM + "_transparency"
    if cmds.window(transUI, exists=True):
        cmds.deleteUI(transUI)

    wesAnimToolsUI = cmds.window(
        transUI, title=transUI, sizeable=True, width=user_width, height=user_height
    )

    cmds.rowColumnLayout(numberOfColumns=1)
    cmds.floatSlider("transparencySlider", min=0, max=1, width=user_width)
    cmds.connectControl("transparencySlider", theIM + ".alphaGain")
    cmds.setParent("..")
    cmds.setParent("..")
    cmds.showWindow(wesAnimToolsUI)


def reset(whatKind, *args):
    try:
        theIM = cmds.textScrollList("listImagePlanes", query=True, selectItem=True)[0]
    except:
        cmds.confirmDialog(message="Please Select an imagePlane from the list")
        return

    if whatKind == "X":
        cmds.setAttr(theIM + ".offsetX", 0)
    if whatKind == "Y":
        cmds.setAttr(theIM + ".offsetY", 0)

    if whatKind == "Scale":
        cmds.setAttr(theIM + ".fit", 2)
        mel_cmd = "AEinvokeFitRezGate " + theIM + "Shape.sizeX " + theIM + "Shape.sizeY"
        print(mel_cmd)
        mel.eval(mel_cmd)

    connectUI()


def UI(parentWindow=None, user_width=180, user_height=17, frameClosed=False):
    if cmds.window("wesImagePlanes", exists=True):
        cmds.deleteUI("wesImagePlanes")
    if not parentWindow:
        wesAnimToolsUI = cmds.window(
            "wesImagePlanes", title="ImagePlanes", sizeable=True, width=user_width
        )
        cmds.showWindow(wesAnimToolsUI)
        parentWindow = "wesImagePlanes"

    cmds.frameLayout(
        "wesImagePlanesFrames",
        collapsable=True,
        label="ImagePlanes",
        collapse=frameClosed,
        parent=parentWindow,
        width=user_width,
    )

    cmds.rowColumnLayout(parent="wesImagePlanesFrames", numberOfColumns=3)
    cmds.button(
        label="Create",
        command=lambda x: createIM(),
        width=user_width * 0.3333,
        height=user_height * 0.85,
        bgc=[0.5, 0.7, 0.5],
    )
    cmds.button(
        label="Rename",
        command=lambda x: renameIM(),
        width=user_width * 0.3333,
        height=user_height * 0.85,
        bgc=[0.5, 0.5, 0.7],
    )
    cmds.button(
        label="Delete",
        command=lambda x: deleteIM(),
        width=user_width * 0.3333,
        height=user_height * 0.85,
        bgc=[0.7, 0.5, 0.5],
    )
    cmds.setParent("..")

    cmds.textScrollList(
        "listImagePlanes",
        allowMultiSelection=False,
        numberOfRows=8,
        width=user_width,
        selectCommand=partial(connectUI),
    )
    cmds.popupMenu()
    cmds.menuItem("Refresh", command=lambda x: refreshList())
    cmds.menuItem("Clear Cache to Save RAM", command=lambda x: refreshCache())
    cmds.setParent("..")
    loadList()

    cmds.rowColumnLayout(
        "editImagePlane", parent="wesImagePlanesFrames", numberOfColumns=1
    )
    cmds.button(
        "IMvisibility", label="Visibility", width=user_width, command=lambda x: visIM()
    )
    cmds.popupMenu()
    cmds.menuItem("Transparency", command=partial(transparencyUI))
    cmds.text("Offset X")
    cmds.floatSlider(
        "offsetX",
        min=-0.1,
        max=0.1,
        width=user_width,
        changeCommand=lambda x: updateSliders(),
    )
    cmds.popupMenu()
    cmds.menuItem("reset X", command=partial(reset, "X"))
    cmds.text("Offset Y")
    cmds.floatSlider(
        "offsetY",
        min=-0.1,
        max=0.1,
        width=user_width,
        changeCommand=lambda x: updateSliders(),
    )
    cmds.popupMenu()
    cmds.menuItem("reset Y", command=partial(reset, "Y"))
    cmds.text("Depth")
    cmds.floatSlider(
        "depth",
        min=0.1,
        max=100,
        width=user_width,
        changeCommand=lambda x: updateSliders(depthChanger=True),
    )
    cmds.text("Scale")
    cmds.floatSlider(
        "sizeX", min=0, max=3, width=user_width, changeCommand=lambda x: updateSliders()
    )
    cmds.popupMenu()
    cmds.menuItem("reset Scale", command=partial(reset, "Scale"))

    cmds.setParent("..")

    cmds.setParent("..")
