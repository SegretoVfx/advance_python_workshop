'''
segretoShelfFunctions.py


Description:
All the callback to my scripts

How To:

    
Author:
Julien Segreto 

Release:
Feb 2021
'''

import maya.cmds as cmds
import maya.mel as mel
import sys
import os
import webbrowser
import importlib

# import scripts
# importlib.reload(scripts)



## definite Functions for scripts import

    
def loadSaveTool(tool, *args):
    if tool == 'save':
        from dcc_menu_api import gui_utils
        gui_utils.execute('''from save_load.apps import maya_funcs;'''
                          '''maya_funcs.create_save_panel();''', 'save_load')
    elif tool == 'load':
        from dcc_menu_api import gui_utils
        gui_utils.execute('''from save_load.apps import maya_funcs;'''
                          '''maya_funcs.create_load_panel();''', 'save_load')
    elif tool == 'sgload':
        from scripts import PXO_ShotgunLoader
        PXO_ShotgunLoader.run()

    elif tool == 'content':    
        from dcc_menu_api import gui_utils
        gui_utils.execute('''from maya_file_handling import maya_menu;''' 
                          '''maya_menu.SceneContent()''', '')
    elif tool == 'asset':    
        from dcc_menu_api import gui_utils
        gui_utils.execute('''from maya_file_handling import maya_menu; '''
                          '''maya_menu.AssetLoad()''', '')
    else:
        cmds.error("Unable to load Pixo loadSaveTool")


def loadDefaultSave(*args):
    from scripts import defaultSave
    importlib.reload(defaultSave)
    defaultSave.main()


def loadCacheUI(*args):
    print("importing cache loader")
    import maya_lighting_tools.tools.cache_loader.main as cache_loader
    cache_loader.run()




def open_shot_folder(*args):
    from dcc_menu_api import gui_utils; gui_utils.execute('''import maya.mel; maya.mel.eval('pxm_exploreToProject();')''', 'maya_scripts')


def open_shot_images_folder(*args):
    from dcc_menu_api import gui_utils; gui_utils.execute('''import maya.mel; maya.mel.eval('pxm_exploreToProjectImages();')''', 'maya_scripts')







def loadPlayblastUi(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('''from maya_playblast import custom_playblast;'''
                      '''obj=custom_playblast.PxoPlayblast();'''
                      '''obj.show(dockable=True, floating=True);''', 
                      'maya_playblast')


def loadPlayblast(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('''from maya_playblast import playblast;'''
                      '''playblast.playblast()''', 'maya_playblast')

def loadPlayblastWitness(*args):
    from dcc_menu_api import gui_utils;
    gui_utils.execute('''from maya_playblast import playblast;''' 
                      '''playblast.playblast(use_camera_name=True);''',
                      'maya_playblast')







def legacy_loadLocalPublish(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('''from legacy_maya_utils import custom_publishes as cp; '''
                      '''cp.custom_publish(cp.CustomShotAnimPublish)''', 
                      'legacy_maya_utils')

def legacy_loadDeadlinePublish(*args):
    from dcc_menu_api import gui_utils;
    gui_utils.execute('from legacy_maya_utils import custom_publishes as cp;'
                      'from legacy_maya_utils.deadline_publishing.publisher import DeadlineAnimPublish;'
                      'cp.custom_publish(DeadlineAnimPublish)',
                      'legacy_maya_utils')

def deadline_pyblish(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('''from pixo_pyblish import start;'''
                      '''from pyblish_maya import show;'''
                      '''start(show, "pxo_maya_deadline", '''
                               '''targets=["deadline"],'''
                               '''window_title="Publish (Deadline)")
                      ''', '')


def local_pyblish(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('''from pixo_pyblish import start;'''
                      '''from pyblish_maya import show;'''
                      '''start(show, "pxo_maya", targets=["local", "local_only"],'''
                      '''window_title="Publish (Local)")''', '')


def loadCameraPublish(*args):
    from dcc_menu_api import gui_utils;
    gui_utils.execute('from legacy_maya_utils import custom_publishes as cp;'
                      'cp.custom_publish(cp.CustomShotCameraPublish)', 
                      'legacy_maya_utils')
                   
    

def open_tag_manager(*args):
    from dcc_menu_api import gui_utils 
    gui_utils.execute('''from maya_file_handling import maya_menu;'''
                      '''maya_menu.TagList()''', '')



def loadStudioLibrary(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('import maya_studio_library_wrapper as msl_wrapper;' 
                      'msl_wrapper.run()',
                      'maya_studio_library_wrapper')

def openWebBrowser(url, *args):
    webbrowser.open(url)


def loadAnimBot(*args):
    print("That tool is supposed to load animbot")
    
def loadATool(*args):
    from scripts import aTools_install
    
    
def loadGraphEditorRedux(status, *args):
    print("load graph Editor Redux")
    # create the module file if needed
    from scripts import graphEditorReduxLoader
    importlib.reload(graphEditorReduxLoader)
    graphEditorReduxLoader.main()
    # launch the plugin
    if status == 'Open':
        cmds.loadPlugin('rb_GraphEditorReduxPlugin.py')
        cmds.GER(l=True)
        cmds.GraphEditor()
    elif status == 'Close':
        cmds.GER(u=True)
    else:
        cmds.error("Can't Load Graph Editor Redux")
    
def loadGraphEditor(*args):
    cmds.GraphEditor()

def loadTweenMachine(*args):
    print("Open the Tween Machine")
    import scripts.tweenMachine
    scripts.tweenMachine.start()
    
def loadWesleyTool(*args):
    from scripts import wesAnimTools
    wesAnimTools.UI()
    

def loadMlTool(sname, *args):
    sname = 'scripts.ml_toolbox_menu.' + sname
    module = importlib.import_module(sname, package=None)
    try:
        module.ui()
    except:
        module.main()

def loadAckTool(*args):
    from scripts import ack_launcherUI
    importlib.reload(ack_launcherUI)
    ack_launcherUI.AckToolsLauncher()
    
    
def loadRed9(*args):
    from scripts import Red9
    importlib.reload(Red9)
    Red9.start()
    
    
def loadAnimSchoolPicker(*args):
    from dcc_menu_api import gui_utils;
    gui_utils.execute('from maya import mel;'
                      'mel.eval("loadPlugin AnimSchoolPicker; AnimSchoolPicker();")', '')

def loadSwitchResolution(res, *args):
    from scripts.segretoTools import segretoSwitchResolution
    importlib.reload(segretoSwitchResolution)
    if res == 'tog':
        segretoSwitchResolution.switcher()
    segretoSwitchResolution.main(res)
    

    
def loadPickWalking(*args):
    print("That tool is supposed to allow pickWalking")

    
def loadSegretoResetAttr(obj, kill, *args):
    from scripts.segretoTools import segretoResetController
    importlib.reload(segretoResetController)
    # apply the rest according to the selected menu
    if obj == 'ctrl':    
        segretoResetController.resetControllers(kill)
        
    elif obj == 'asset':    
        segretoResetController.resetAssets(kill)
        
    elif obj == 'scene':
        segretoResetController.resetScene(kill)
       
    else:
        cmds.error("Error while calling the reset function.")
    
    
    
def loadEasyMotionTrailUI(*args):
    print("Easy Motion Trail")
    from scripts.segretoTools import segretoEasyMotionTrail
    importlib.reload(segretoEasyMotionTrail)
    segretoEasyMotionTrail.main()
    

def loadAdvancedMotionTrailUI(*args):
    print("Loading Advanced Motion Trail UI")
    from scripts.segretoTools import segretoAdvancedMotionTrailUI
    importlib.reload(segretoAdvancedMotionTrailUI)
    #segretoAdvancedMotionTrailUI.main()
    


# def loadSelectAll(obj, selAll, *args):
def loadSelectAll(obj,  *args):
    print("Select All {0}".format(obj))
    from scripts.segretoTools import segretoMayaUtils
    importlib.reload(segretoMayaUtils)

    # get the name of the controllers - not the same for each facilities
    if obj == 'ctrl':
        ojb = segretoMayaUtils.getControllerGlobalName()

    elif obj == 'geo':
        segretoMayaUtils.select_geometry()
        
    segretoMayaUtils.selectAll(obj) 

    
def loadSelectAllKeyed(*args):
    print("Select keyed controllers only")
    from scripts.ml_toolbox_menu import ml_selectKeyed
    from scripts.segretoTools import segretoMayaUtils
    if cmds.ls(sl=1) == []:
        cmds.select('*:*_{0}'.format(segretoMayaUtils.getControllerGlobalName()))
    ml_selectKeyed.main()  
    
    

    


def importReferenceStandardMan(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('from legacy_maya_utils import menu_functions;'
                      'menu_functions.reference_man()', 'legacy_maya_utils')

def removeReferenceStandardMan(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('from legacy_maya_utils import menu_functions;'
                      'menu_functions.remove_all_standard_man()', 'legacy_maya_utils')
                      
                      
                      
                      
                      
                      
def loadLocinate(*args):
    print("Load Segreto Locinate tool")
    from scripts.segretoTools import segretoLocinate
    importlib.reload(segretoLocinate)
    segretoLocinate.main()  

def loadRotationOrderSwitch(*args):
    print("Load Loomis rotation Order Tool")
    from scripts.ml_toolbox_menu import ml_convertRotationOrder
    ml_convertRotationOrder.ui()  

def loadBallisticAnimation(*args):
    print("Load Loomis Ballistic Animation Tool - Gravity Ball")
    from scripts.ml_toolbox_menu import ml_ballisticAnimation
    ml_ballisticAnimation.main() 
    
    
    
def loadWorldBaker(*args):
    print("Load Loomis world baker")
    from scripts.ml_toolbox_menu import ml_worldBake
    ml_worldBake.ui() 

def loadMlArcTracer(*args):
    print("Load Loomis arc Tracer")
    from scripts.ml_toolbox_menu import ml_arcTracer
    ml_arcTracer.ui() 


# def loadIkFkSwitch(option, *args):
#     print("Load Segreto IKFK switch") 
#     if tool == 'one':
#         from scripts.segretoTools import segretoIkFkSwitch
#         importlib.reload(segretoIkFkSwitch)
#         segretoIkFkSwitch.main() 
#     elif tool == 'all':
#         from scripts.segretoTools import segretoIkFkSwitch
#         importlib.reload(segretoIkFkSwitch)
#         segretoIkFkSwitch.main() 
#     elif tool == 'UI':    
#         from scripts.segretoTools import segretoIkFkSwitch
#         importlib.reload(segretoIkFkSwitch)
#         segretoIkFkSwitch.main() 
#     else:
#         cmds.error("Unable to load Segreto IKFK switch")


def loadAlignTool(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('import maya.mel;'
                      'maya.mel.eval("source dsAlignToolUI;");',
                      'maya_scripts')
         
def snap_parent(*args):
        from scripts.segretoTools import segreto_snap_tool
        importlib.reload(segreto_snap_tool)
        segreto_snap_tool.snap_parent() 

def snap_translate(*args):
        from scripts.segretoTools import segreto_snap_tool
        importlib.reload(segreto_snap_tool)
        segreto_snap_tool.snap_translate() 

def snap_rotate(*args):
        from scripts.segretoTools import segreto_snap_tool
        importlib.reload(segreto_snap_tool)
        segreto_snap_tool.snap_rotate() 

def segreto_anim_utils(mode='replaceCompletely', *args):
    from scripts.segretoTools import segreto_anim_utils
    importlib.reload(segreto_anim_utils)
    segreto_anim_utils.copy_paste_keys(mode=mode, attribute=None) 




def loadStickyFeet(*args):
    mel.eval("source gb_matchPlacement;")
         

def loadEasyParentUI(constChoice, mo, *args):
    print("import segreto easy parent UI")
    from scripts.segretoTools import segretoEasyParent
    importlib.reload(segretoEasyParent)
    if constChoice == 'parenting':
        segretoEasyParent.parenting(mo) 
    elif constChoice == 'pointing':
        segretoEasyParent.pointing(mo) 
    elif constChoice == 'orienting':
        segretoEasyParent.orienting(mo) 
    elif constChoice == 'looking':
        segretoEasyParent.looking(mo) 
    elif constChoice == 'rivet':
        segretoEasyParent.rivet(mo) 
    elif constChoice == 'unparenting':
        segretoEasyParent.unparenting() 
    elif constChoice == 'killConst':
        segretoEasyParent.killConst() 
    elif constChoice == 'bakeAnim':
        segretoEasyParent.bakeAnim() 
    elif constChoice == 'UI':
        segretoEasyParent.main() 
    else:
        cmds.error("Problem with constraint tools")
    
def loadSelectConstraint(*args):
    print("Select All constraint")
    from scripts.segretoTools import segretoEasyParent
    importlib.reload(segretoEasyParent)
    segretoEasyParent.main()   



def loadsetFrameRange(cut, *args):

    from legacy_maya_utils import shotgun_utils

    scene_name = cmds.file(q=True, location=True)
    print("Set frame range for scene " + scene_name)
    shotguninfo = shotgun_utils.get_framerange_from_sg(scene_name)
    
    if shotguninfo == []:
        cmds.error('No frame range information available on SG')

    shotStart = shotguninfo[0]
    cutStart  = shotguninfo[1]
    cutEnd    = shotguninfo[2]
    shotEnd   = shotguninfo[3]


    if cut == 'shot':
        # set shot range
        cmds.playbackOptions(animationStartTime=shotStart, 
                             min=shotStart, max=shotEnd,
                             animationEndTime=shotEnd)
    elif cut == 'cut':
        # set cut range
        cmds.playbackOptions(animationStartTime=cutStart,
                             min=cutStart, max=cutEnd,
                             animationEndTime=cutEnd)
    else:
        cmds.error("can't set time range")

        
def setResolutionFromSG(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('from legacy_maya_utils import render_utils;'
                      'render_utils.set_resolution_from_sg()', 'legacy_maya_utils')

def updateAllReference(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('''from legacy_maya_utils import reference_utils;'''
                      '''reference_utils.update_all_references_to_latest()''', 
                      'legacy_maya_utils')

        
        
def loadContext(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('from context_display.apps import maya_entry_point;'
                      'maya_entry_point.main();', '')

def loadChangeContext(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('from change_context.apps import maya_entry_point;'
                      'maya_entry_point.main()', 'change_context')


def loadSGShotNotes(*args):
    print("Open shotgun notes for the shot")
    from dcc_menu_api import gui_utils
    gui_utils.execute('from todo_sticky_note.dccs.maya import maya_mod;' 
                      'maya_mod.start()', 'todo_sticky_note')

def loadSGOpen(dep, *args):
    if dep == 'project':
        webbrowser.open("{}/detail/Project/{}".format(os.environ["PXO_SHOTGUN_URL"], os.environ["PXO_PROJECT_SGID"]))
    elif dep == 'sequence':
        webbrowser.open("{}/detail/Sequence/{}".format(os.environ["PXO_SHOTGUN_URL"], os.environ["PXO_SEQUENCE_SGID"]))
    elif dep == 'shot':
        webbrowser.open("{}/detail/Shot/{}".format(os.environ["PXO_SHOTGUN_URL"], os.environ["PXO_SHOT_SGID"]))
    elif dep == 'task':
        webbrowser.open("{}/detail/Task/{}".format(os.environ["PXO_SHOTGUN_URL"], os.environ["PXO_TASK_SGID"]))
    else:
        cmds.error("Can't open Shotgun page")

def loadSGPanel(*args):
    from scripts import PXO_ShotgunLoader
    PXO_ShotgunLoader.panel()

def loadSGCacheUI(*args):
    print("importing shotgun cache loader")
    import maya_yvr_scripts.scripts as yvr
    yvr.lgt.open_sg.run()

def loadFindTool(what, *args):
    print("import segreto Find tool")
    from scripts.segretoTools import segretoFindTool
    importlib.reload(segretoFindTool)
    segretoFindTool.main(what)
    
def loadSpeedometer(*args):
    from scripts import tkSpeedometer
    importlib.reload(tkSpeedometer)



def createObserverCamera(status, *args):
    if status == 'cam':
        from scripts.segretoTools import segretoFollowCamera
        importlib.reload(segretoFollowCamera)
        segretoFollowCamera.main()
    elif status == 'UI':
        from scripts.segretoTools import segretoFollowCameraUI
        importlib.reload(segretoFollowCameraUI)
        segretoFollowCameraUI.buildFollowCamUI()
    else:
        cmds.error("Problem while loading the followCamera script")
        

        

def loadSegretoCreateWitnessCamUI(cam, *args):
    from scripts.segretoTools import segretoCreateWitnessCam
    importlib.reload(segretoCreateWitnessCam)
    if cam == 'Persp':
        segretoCreateWitnessCam.CreateWitnessCamera().buildCam(cam)
    else:
        segretoCreateWitnessCam.CreateWitnessCamera().UI()
 
def loadMoCapsetup(*args):

    mocap_script_path = "V:/Rigging/moCap_script"

    import sys 

    if not mocap_script_path in sys.path:
        sys.path.insert(1, mocap_script_path)

    import moCapSetup_v009
    importlib.reload(moCapSetup_v009)


    # from scripts import moCapSetup
    # importlib.reload(moCapSetup)
    # moCapSetup.show()


       
def loadFixPersp(*args):
    from scripts.wesTools import wesSceneSetup
    importlib.reload(wesSceneSetup)
    wesSceneSetup.fixPerspCamera()
    mel.eval("lookThroughModelPanel persp modelPanel3")

def loadAnnotationUI(annot, *args):
    from scripts.segretoTools import segretoAnnotation
    importlib.reload(segretoAnnotation)
    if annot == 'show':
        # always delete the potential existing HUD before creating a new one 
        segretoAnnotation.CreateAnnotation().delete_heads_up()
        segretoAnnotation.CreateAnnotation().display_annotation()
    elif annot == 'delete':
        segretoAnnotation.CreateAnnotation().delete_heads_up()
        
    
    
def loadDistanceMeter(*args):
    from scripts.segretoTools import segretoDistanceMeter
    importlib.reload(segretoDistanceMeter)
    segretoDistanceMeter.main()
        
def loadHoldoutCreator(nodeType, *args):
    from scripts.segretoTools import segretoHoldoutCreator
    importlib.reload(segretoHoldoutCreator)
    segretoHoldoutCreator.main(nodeType)

 
def loadDisplayLayerCreator(*args):
    print("import segreto Display Layer Creator")
    from scripts.segretoTools import segretoDisplayLayerCreator
    importlib.reload(segretoDisplayLayerCreator)
    segretoDisplayLayerCreator.main()


def loadOutlinerColorManager(*args):
    print("import load Outliner Color Manager UI")
    import maya_lighting_tools.tools.outliner_color_changer.main as outliner_color_changer
    outliner_color_changer.run()

def loadToolSet(*args):
    from dcc_menu_api import gui_utils
    gui_utils.execute('from toolsets.dccs.maya import show_main;'
                      'toolsets_main = show_main()', 'toolsets')


def loadProjectSpecificTool(sname, *args):
    # Dynamically import projects specifics modules
    module = importlib.import_module(sname)
    importlib.reload(module)

    try:
        module.main()
    except:
        cmds.error('Couldn\'t Load module named {0}'.format(module))


        
def loadArShake(*args):
    print("import arShake")
    from scripts import arShake
    importlib.reload(arShake)
    arShake.main()

def loadBhSpeed(*args):
    print('Import bhSpeed')
    mel.eval("source bhSpeed;")
    mel.eval("bh_speedGUIh;")


def loadBhGhost(*args):
    print('Import bhGhost')
    mel.eval("source bhGhost;")
    mel.eval("bhGhost;")


def loadBoSmear(*args):
    print('Import boSmear')
    mel.eval("source boSmear;")
    mel.eval("boSmear;")


def loadPose2Shelf(*args):
    print('Import Pose2Shelf')
    mel.eval("source pose2shelf;")
    mel.eval("pose2shelf;")

def loadAckDeleteRedundant(*args):
    print("import Cleanup Key")
    sel = cmds.ls(sl=True)
    for s in sel:
        cmds.selectKey()
    mel.eval("source ackDeleteRedundant;")
    mel.eval("ackDeleteRedundant;")

def loadChannelBoxPlus(*args):
    mel.eval("source channelBoxPlus;")
    import channelBoxPlus
    channelBoxPlus.install(threshold=0.75)

def loadKeyframeReduction(*args):
    from scripts.keyframeReduction import ui
    ui.show()


def loadCreateAnnotateNode(*args):
    print('Launch CreateAnnotateNode')
    mel.eval("CreateAnnotateNode;")



def loadAnimSnap(*args):
    print('Import animSnap')
    mel.eval("source animSnap;")
    mel.eval("animSnap;")

def loadGbMatchPlacement(*args):
    print('Import gb_matchPlacement')
    mel.eval("source gb_matchPlacement;")
    mel.eval("gb_matchPlacement;")


def loadKTL_smoothKey(*args):
    print('Import KTL_smoothKey')
    mel.eval("source KTL_smoothKey;")
    mel.eval("KTL_smoothKey;")

def loadNP_curveLocalScale(*args):
    print('Import NP_curveLocalScale')
    mel.eval("source NP_curveLocalScale;")
    #mel.eval("NP_curveLocalScale;")

def loadOaSmoothKeys(*args):
    print('Import oaSmoothKeys')
    mel.eval("source oaSmoothKeys;")
    mel.eval("oaSmoothKeys;")


def loadSegretoShiftKeyUI(*args):
    print("import segreto Shift Keys UI")
    from scripts.segretoTools import segretoShiftKeysUI
    importlib.reload(segretoShiftKeysUI)
    segretoShiftKeysUI.shiftKeysUI()


def loadDigitalPoseTest(*args):
    print("import Digital Pose Test")
    import rb_DPT as dpt
    dpt.launch()


def loadBakeCamera(*args):
    print("bake Camera UI")
    from scripts import bakeCamera
    importlib.reload(bakeCamera)

def loadImagePlaneHelper(*args):
    print("Load image plane helper UI")
    from scripts import imagePlaneHelper
    importlib.reload(imagePlaneHelper)
    imagePlaneHelper.pw_imgPlaneUI()



def loadCacheNplay(*args):
    print('Import cacheNplay')
    mel.eval("source cacheNplay;")











