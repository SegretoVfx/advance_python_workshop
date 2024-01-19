import maya.utils


def custom_import():
    # import j_animShelf
    import juls_anim_shelf

    print("Hello World")
    # j_animShelf
    juls_anim_shelf.AnimShelf()


maya.utils.executeDeferred(custom_import)
