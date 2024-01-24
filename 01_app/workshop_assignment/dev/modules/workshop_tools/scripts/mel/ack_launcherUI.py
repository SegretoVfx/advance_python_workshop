"""
segretoAnnotationUI.py

Julien Segreto 

march 2021

   Usage:
        
"""

import maya.mel as mel
import maya.cmds as cmds
from functools import partial

from os import walk, path


class AckToolsLauncher(object):
    def __init__(self):
        # Global Variables
        # self.UI()
        self.curScriptDir = f"{path.dirname(__file__)}/ack_toolbox_menu"
        self.viewport_option_ui()

    def close_win(self, window=None, arg=None):
        if cmds.window(self.win, exists=True):
            cmds.deleteUI(self.win, window=True)

    def launch_mel_script(self, melName, option, *args):
        """Read the mel script from it's mel file and launch it"""
        file = open("{0}/{1}.mel".format(self.curScriptDir, melName))
        content = file.read()  # .replace('\n',' ')
        file.close()
        # print(content)
        # Load the script
        # Call the script with some variation if any
        if melName == "ackSetup":
            mel.eval("{0}".format(content))
            mel.eval("{1} {2};".format(content, melName, option))
        elif melName == "ackToggleCams":
            if option == "setup":
                mel.eval("{0}; {1}_{2};".format(content, melName, option))
            else:
                mel.eval("{0}; {1};".format(content, melName, option))
        elif (
            melName == "ackMoveKeys"
            or melName == "ackConvergeBuffer"
            or melName == "ackSpreadSqueezeTiming"
            or melName == "ackPushPull"
        ):
            mel.eval("{0}".format(content))
            mel.eval("{0} {1};".format(melName, option))
        else:
            mel.eval("{0};".format(content))
            mel.eval("{0};".format(melName))

    def viewport_option_ui(self, *args):
        windowID = "ack_viewportOptionUI"
        winName = "Aaron Koressel viewport options UI"
        if cmds.uiTemplate(windowID, exists=True):
            cmds.deleteUI(windowID, uiTemplate=True)

        self.ui = cmds.uiTemplate(windowID)
        self.button = cmds.button(
            defineTemplate=windowID, width=100, height=20, align="center"
        )
        self.frLay = cmds.frameLayout(
            defineTemplate=windowID, borderVisible=True, labelVisible=False, mh=5, mw=5
        )
        self.txtFld = cmds.textFieldGrp(defineTemplate=windowID, width=100, height=40)
        self.intSli = cmds.intSlider(defineTemplate=windowID, min=0, max=10, step=1)

        self.win = cmds.window(
            winName, s=True, menuBar=True, menuBarVisible=True, rtf=True
        )

        cmds.setUITemplate(windowID, pushTemplate=True)

        cmds.columnLayout(
            p=self.win, numberOfChildren=1, columnAttach=("both", 5), columnWidth=280
        )
        # frame 1
        cmds.frameLayout()

        cmds.rowLayout(numberOfColumns=2)
        cmds.text(label="General")
        # cmds.setParent('..')

        # cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="ack tool setup", c=partial(self.launch_mel_script, "ackSetup", "setup")
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Toggle camera view on current viewport")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, cl2=("right", "left"))
        self.button = cmds.button(
            l="setup Tog View",
            c=partial(self.launch_mel_script, "ackToggleCams", "setup"),
        )
        self.button = cmds.button(
            l="Toggle view", c=partial(self.launch_mel_script, "ackToggleCams", "")
        )
        cmds.setParent("..")
        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Toggle Visibility")
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=4)
        self.button = cmds.button(
            l="Curves",
            c=partial(self.launch_mel_script, "ackToggleNURBSCurves", ""),
            w=50,
        )
        self.button = cmds.button(
            l="Geo", c=partial(self.launch_mel_script, "ackToggleModel", ""), w=50
        )
        # cmds.setParent('..')

        # cmds.rowLayout(numberOfColumns=2, cl2=('right','left'))
        self.button = cmds.button(
            l="ImgPlane",
            c=partial(self.launch_mel_script, "ackToggleImagePlane", ""),
            w=50,
        )
        self.button = cmds.button(
            l="Highlght",
            c=partial(self.launch_mel_script, "ackToggleHighlight", ""),
            w=50,
        )
        cmds.setParent("..")
        # cmds.setParent('..')

        cmds.separator(style="in", height=10)
        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Manipulator mode:")
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2, cl2=("right", "left"))
        self.button = cmds.button(
            l="Translate Mode",
            c=partial(self.launch_mel_script, "ackToggleTranslateMode", ""),
        )
        self.button = cmds.button(
            l="Rotate Mode",
            c=partial(self.launch_mel_script, "ackToggleRotateMode", ""),
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1, cl1=("center"))
        cmds.text(label="Shortcuts")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2, cl2=("right", "left"))
        self.button = cmds.button(
            l="Go to Time", c=partial(self.launch_mel_script, "ackGotoTime", "")
        )
        self.button = cmds.button(
            l="Open Graph Editor",
            c=partial(self.launch_mel_script, "ackNewGraphEditor", ""),
        )
        cmds.setParent("..")
        cmds.setParent("..")

        # frame 1 window 2
        cmds.frameLayout()

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Edit anim curve tangents")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Tangents Type", c=partial(self.launch_mel_script, "ackCycleTangents", "")
        )
        self.button = cmds.button(
            l="Break / Unify",
            c=partial(self.launch_mel_script, "ackToggleTangentType", ""),
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Edit keys")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Zero keys", c=partial(self.launch_mel_script, "ackZeroOutKeys", "")
        )
        self.button = cmds.button(
            l="Keys all channel",
            c=partial(self.launch_mel_script, "ackTimingFramework", ""),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Delete keys", c=partial(self.launch_mel_script, "ackDeleteKey", "")
        )
        self.button = cmds.button(
            l="Delete redundant",
            c=partial(self.launch_mel_script, "ackDeleteRedundant", ""),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Keys color", c=partial(self.launch_mel_script, "ackToggleKeyColor", "")
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Swap 2 keys", w=200, c=partial(self.launch_mel_script, "ackSwapKeys", "")
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Add key", c=partial(self.launch_mel_script, "ackSliceCurves", "")
        )
        self.button = cmds.button(
            l="Add in between", c=partial(self.launch_mel_script, "ackSteppedTween", "")
        )

        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Move keys")
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Move keys left", c=partial(self.launch_mel_script, "ackMoveKeys", "left")
        )
        self.button = cmds.button(
            l="Move keys right",
            c=partial(self.launch_mel_script, "ackMoveKeys", "right"),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Move keys up", c=partial(self.launch_mel_script, "ackMoveKeys", "up")
        )
        self.button = cmds.button(
            l="Move keys down", c=partial(self.launch_mel_script, "ackMoveKeys", "down")
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Converge left",
            c=partial(self.launch_mel_script, "ackMoveKeys", "convergeLeft"),
        )
        self.button = cmds.button(
            l="Converge right",
            c=partial(self.launch_mel_script, "ackMoveKeys", "convergeRight"),
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Push key value", c=partial(self.launch_mel_script, "ackPushPull", "push")
        )
        self.button = cmds.button(
            l="Pull key value", c=partial(self.launch_mel_script, "ackPushPull", "pull")
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Spread timing",
            c=partial(self.launch_mel_script, "ackSpreadSqueezeTiming", "spread"),
        )
        self.button = cmds.button(
            l="Squeeze timing",
            c=partial(self.launch_mel_script, "ackSpreadSqueezeTiming", "squeeze"),
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Away buffer",
            c=partial(self.launch_mel_script, "ackConvergeBuffer", "away"),
        )
        self.button = cmds.button(
            l="Toward buffer",
            c=partial(self.launch_mel_script, "ackConvergeBuffer", "toward"),
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Snap to buffer",
            w=200,
            c=partial(self.launch_mel_script, "ackConvergeBuffer", "snap"),
        )
        cmds.setParent("..")

        cmds.setParent("..")
        # cmds.separator(style="in", height=10)

        cmds.frameLayout()

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Animation managment")
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Create Cycle",
            w=200,
            c=partial(self.launch_mel_script, "ackSnapEndKeyValues", ""),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Snap value", c=partial(self.launch_mel_script, "ackSnapKeyValues", "")
        )
        self.button = cmds.button(
            l="Connect Anim", c=partial(self.launch_mel_script, "ackSnapAnimation", "")
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Mirror key",
            w=200,
            c=partial(self.launch_mel_script, "ackNegateKeys", ""),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Move keys to cursor",
            w=200,
            c=partial(self.launch_mel_script, "ackSnapToTime", ""),
        )
        cmds.setParent("..")
        cmds.setParent("..")

        # cmds.separator(style="in", height=10)

        # frame 3
        # cmds.rowLayout(numberOfColumns=1, cl1=('center'))
        # cmds.text(label='Quick playblast selected frames')
        # cmds.setParent('..')

        # self.button = cmds.button(label = 'playblast',
        # command = partial(self.launch_mel_script, 'ackPlayblastSelectedKeys', ''))

        # cmds.separator(style="in", height=10)
        # frame 3

        self.button = cmds.button(
            label="close", command=partial(self.close_win, self.win)
        )
        cmds.setParent("..")

        cmds.showWindow(self.win)


# second UI with graph editor related options
class AckGraphToolsLauncher(object):
    def __init__(self):
        # Global Variables
        # self.UI()
        self.curScriptDir = "{0}/ack_toolbox_menu".format(path.dirname(__file__))
        self.viewport_option_ui()

    def close_win(self, window=None, arg=None):
        if cmds.window(self.win, exists=True):
            cmds.deleteUI(self.win, window=True)

    def launch_mel_script(self, melName, option, *args):
        """Read the mel script from it's mel file and launch it"""
        file = open("{0}/{1}.mel".format(self.curScriptDir, melName))
        content = file.read()  # .replace('\n',' ')
        file.close()
        # print(content)
        # Load the script
        # Call the script with some variation if any

        if (
            melName == "ackMoveKeys"
            or melName == "ackConvergeBuffer"
            or melName == "ackSpreadSqueezeTiming"
            or melName == "ackPushPull"
        ):
            mel.eval("{0}".format(content))
            mel.eval("{0} {1};".format(melName, option))
        else:
            mel.eval("{0};".format(content))
            mel.eval("{0};".format(melName))
            # cmds.error("Error while reading ack scripts")

    def viewport_option_ui(self, *args):
        windowID = "ack_graphEditorOptionUI"
        winName = "Aaron Koressel Graph Editor options UI"
        if cmds.uiTemplate(windowID, exists=True):
            cmds.deleteUI(windowID, uiTemplate=True)

        self.ui = cmds.uiTemplate(windowID)
        self.button = cmds.button(
            defineTemplate=windowID, width=100, height=20, align="center"
        )
        self.frLay = cmds.frameLayout(
            defineTemplate=windowID, borderVisible=True, labelVisible=False, mh=5, mw=5
        )
        self.txtFld = cmds.textFieldGrp(defineTemplate=windowID, width=100, height=40)
        self.intSli = cmds.intSlider(defineTemplate=windowID, min=0, max=10, step=1)

        self.win = cmds.window(
            winName, s=True, menuBar=True, menuBarVisible=True, rtf=True
        )

        cmds.setUITemplate(windowID, pushTemplate=True)

        cmds.columnLayout(
            p=self.win, numberOfChildren=1, columnAttach=("both", 5), columnWidth=230
        )

        # frame 1 window 2
        cmds.frameLayout()

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Edit anim curve tangents")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Tangents Type", c=partial(self.launch_mel_script, "ackCycleTangents", "")
        )
        self.button = cmds.button(
            l="Break / Unify",
            c=partial(self.launch_mel_script, "ackToggleTangentType", ""),
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Manage keys")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Zero keys", c=partial(self.launch_mel_script, "ackZeroOutKeys", "")
        )
        self.button = cmds.button(
            l="Keys all channel",
            c=partial(self.launch_mel_script, "ackTimingFramework", ""),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Delete keys", c=partial(self.launch_mel_script, "ackDeleteKey", "")
        )
        self.button = cmds.button(
            l="Delete redundant",
            c=partial(self.launch_mel_script, "ackDeleteRedundant", ""),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Keys color", c=partial(self.launch_mel_script, "ackToggleKeyColor", "")
        )
        cmds.setParent("..")

        cmds.setParent("..")
        # cmds.separator(style="in", height=10)

        cmds.frameLayout()

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Edit Keys")
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Swap 2 keys", w=200, c=partial(self.launch_mel_script, "ackSwapKeys", "")
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Add key", c=partial(self.launch_mel_script, "ackSliceCurves", "")
        )
        self.button = cmds.button(
            l="Add in between", c=partial(self.launch_mel_script, "ackSteppedTween", "")
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Move keys")
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Move keys left", c=partial(self.launch_mel_script, "ackMoveKeys", "left")
        )
        self.button = cmds.button(
            l="Move keys right",
            c=partial(self.launch_mel_script, "ackMoveKeys", "right"),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Move keys up", c=partial(self.launch_mel_script, "ackMoveKeys", "up")
        )
        self.button = cmds.button(
            l="Move keys down", c=partial(self.launch_mel_script, "ackMoveKeys", "down")
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Converge right",
            c=partial(self.launch_mel_script, "ackMoveKeys", "convergeRight"),
        )
        self.button = cmds.button(
            l="Converge left",
            c=partial(self.launch_mel_script, "ackMoveKeys", "convergeLeft"),
        )
        cmds.setParent("..")

        cmds.separator(style="in", height=10)

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Push key value", c=partial(self.launch_mel_script, "ackPushPull", "push")
        )
        self.button = cmds.button(
            l="Pull key value", c=partial(self.launch_mel_script, "ackPushPull", "pull")
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Spread timing",
            c=partial(self.launch_mel_script, "ackSpreadSqueezeTiming", "spread"),
        )
        self.button = cmds.button(
            l="Squeeze timing",
            c=partial(self.launch_mel_script, "ackSpreadSqueezeTiming", "squeeze"),
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Toward buffer",
            c=partial(self.launch_mel_script, "ackConvergeBuffer", "toward"),
        )
        self.button = cmds.button(
            l="Away buffer",
            c=partial(self.launch_mel_script, "ackConvergeBuffer", "away"),
        )
        cmds.setParent("..")

        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Snap to buffer",
            w=200,
            c=partial(self.launch_mel_script, "ackConvergeBuffer", "snap"),
        )
        cmds.setParent("..")

        cmds.setParent("..")
        # cmds.separator(style="in", height=10)

        cmds.frameLayout()

        cmds.rowLayout(numberOfColumns=1)
        cmds.text(label="Animation managment")
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Create Cycle",
            w=200,
            c=partial(self.launch_mel_script, "ackSnapEndKeyValues", ""),
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=2)
        self.button = cmds.button(
            l="Snap value", c=partial(self.launch_mel_script, "ackSnapKeyValues", "")
        )
        self.button = cmds.button(
            l="Connect Anim", c=partial(self.launch_mel_script, "ackSnapAnimation", "")
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Miror key", w=200, c=partial(self.launch_mel_script, "ackNegateKeys", "")
        )
        cmds.setParent("..")
        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            l="Move to cursor",
            w=200,
            c=partial(self.launch_mel_script, "ackSnapToTime", ""),
        )
        cmds.setParent("..")
        cmds.setParent("..")

        cmds.frameLayout(borderVisible=False, mh=5, mw=5)

        cmds.rowLayout(numberOfColumns=1)
        self.button = cmds.button(
            label="close", w=200, command=partial(self.close_win, self.win)
        )
        cmds.setParent("..")

        cmds.showWindow(self.win)
