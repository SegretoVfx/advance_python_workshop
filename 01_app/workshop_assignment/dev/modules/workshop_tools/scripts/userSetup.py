import maya.utils


def custom_import():
    print("Hello from workshop userSetup")
    # import shelfBase
    import anim_shelf_creator


maya.utils.executeDeferred(custom_import)
