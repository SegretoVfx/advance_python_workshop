import maya.utils


def custom_import():
    # import shelf_builder
    import shelf_builder
    shelf_builder.AnimShelf()


maya.utils.executeDeferred(custom_import)
