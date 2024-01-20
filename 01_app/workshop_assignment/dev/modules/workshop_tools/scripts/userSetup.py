import maya.utils


def custom_import():
    print("Hello from workshop userSetup")
    import shelfBase


maya.utils.executeDeferred(custom_import)
