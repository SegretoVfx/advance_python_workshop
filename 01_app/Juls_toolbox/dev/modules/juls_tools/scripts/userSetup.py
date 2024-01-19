import maya.utils


def custom_import():
    print("Hello from userSetup")
    import j_animShelf
    import juls_anim_shelf

    juls_anim_shelf.AnimShelf()


maya.utils.executeDeferred(custom_import)
