import maya.cmds as cmds
cmds.loadPlugin("testplugin.py")


print("This is the userSetup from the module")
cmds.LaunchJulsAnimShelf()