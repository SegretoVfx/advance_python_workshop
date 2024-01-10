import sys
import maya.api.OpenMaya as om

sys.path.append("..")

from juls_tools.scripts import juls_anim_shelf

def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using the Maya Python API 2.0.
    """
    pass


# command
class LaunchJulsShelfCmd(om.MPxCommand):
    kPluginCmdName = "LaunchJulsAnimShelf"

    def __init__(self):
        om.MPxCommand.__init__(self)

    @staticmethod
    def cmdCreator():
        return LaunchJulsShelfCmd()

    def doIt(self, args):
        print("Hello World!")
        juls_anim_shelf.AnimShelf()
        print("Hello World!")


# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.registerCommand(
            LaunchJulsShelfCmd.kPluginCmdName, LaunchJulsShelfCmd.cmdCreator
        )
    except AssertionError as err:
        sys.stderr.write(
            f"Failed to register command: {LaunchJulsShelfCmd.kPluginCmdName}\n"
        )
        raise


# Uninitialized the plug-in
def uninitializePlugin(plugin):
    pluginFn = om.MFnPlugin(plugin)
    try:
        pluginFn.deregisterCommand(LaunchJulsShelfCmd.kPluginCmdName)
    except AssertionError as err:
        sys.stderr.write(
            f"Failed to unregister command: {LaunchJulsShelfCmd.kPluginCmdName}\n"
        )
        raise
