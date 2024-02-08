"""
##########################################################################################################
######								Wesley's Screen Tracker script									######
######									heywesley@gmail.com											######
##########################################################################################################

A simple and fast way to see your spacing and arcs.	
Just like drawing dots on your monitor, except so much faster.
It also updates as you scrub your timeline!					
Select the object you want to track. Then load the camera, and	
create your tracker!  You can also move the main tracker.  For 	
example, if you selected the head control, you can move the tracker
to the nose. 														

v1.6  - Get to choose color instead of random

v1.5  - Added Annotations. Removed auto-bake first time.  

v1.4  - Added auto bake for first time
	  - Added random color attribute for multiple coloring	

v1.3  - Now conformed the curve to only be 1 object.  Much faster in creation time.	
	  - Added timeline adjustment, for start frame and end frame	

v1.2  - Curve created, Using skinBind to have it follow.
	  - Further updates will have just one curve to be faster,
	    on creation. (Thanks to Thiago Martins and Sebastian Trujillo for the ideas and help!!!)

v1.1  - Curve created, but using scriptJob to update

v1.0  - Uses joints, and sets your viewport to view joints with xray
	  - Updates by scrubbing your timeline.  Best is to press play on every frame. 	

##########################################################################################################
"""

import maya.cmds as cmds
import maya.mel as mel

#Gather Imports
from . import wesUtils
import importlib
importlib.reload(wesUtils)
from .wesUtils import setActiveWindow
from .wesUtils import editAttrChannels
from .wesUtils import chosenModifiers

usr_timeline = True

def runWesTracker(whatCommand, chooseColor=1):
	tmp_camera_name = cmds.textField("cameraTextField", q=True, text=True)
	tmp_object_track = cmds.textField("objectTextField", q=True, text=True)
	arc_size = float(cmds.intField("wa_size", q=True, value=True))

	#Just in case world_space got deleted
	if tmp_camera_name == "world_space":
		if not cmds.objExists("world_space"):
			world_obj = cmds.createNode('transform', name="world_space")

	#No need to check if its deleting
	if not whatCommand == "delete":
		if tmp_camera_name == "":
			cmds.confirmDialog(message="Eddie thinks you're an idiot because you didn't load a camera to follow, just select one. =)")
			return

		if tmp_object_track == "":
			cmds.confirmDialog(message="Eddie thinks you're an idiot because you didn't load an object to track, just select one. =)")
			return

	#RUN THE MOTHER FUCKING COMMAND! WOOHOOO!
	wesTracker(tmp_object_track, tmp_camera_name,arc_size, theCommand=whatCommand, chooseColor=chooseColor)

	#To set it to a small joint size as a start
	cmds.jointDisplayScale(0.01)
	
	setActiveWindow()
def setFrameRange():
	global usr_timeline

	start_fr = int(cmds.playbackOptions(q=True, minTime=True))
	end_fr = int(cmds.playbackOptions(q=True, maxTime=True))

	if usr_timeline:
		cmds.button("butt_timeline", edit=True, l="custom", bgc=[0.8,0.8,0.8])
		cmds.button("usr_start_fr", edit=True, l=start_fr, en=True)
		cmds.button("usr_end_fr", edit=True, l=end_fr, en=True)
		usr_timeline = False
	else:
		cmds.button("butt_timeline", edit=True, l="timeline", bgc=[0.4,0.4,0.4])
		cmds.button("usr_start_fr", edit=True, l="", en=False)
		cmds.button("usr_end_fr", edit=True, l="", en=False)
		usr_timeline = True


def finishSetupOnce():

	viewports = cmds.getPanel(type='modelPanel')
	cmds.playbackOptions(e=True,playbackSpeed=0, maxPlaybackSpeed=1)
	# cmds.playbackOptions(e=True, minTime=save_start)    
	# cmds.playbackOptions(e=True, maxTime=save_end)
	# print save_start
	# print save_end
	for vp in viewports:
		#cmds.isolateSelect(vp, state=False)
		cmds.modelEditor(vp,edit=True, joints=True, jointXray=True)

def runSetupOnce(start_fr,end_fr,item):

	viewports = cmds.getPanel(type='modelPanel')
	cmds.select(item)

	for vp in viewports:
	   	#cmds.isolateSelect(vp, state=True)
		cmds.isolateSelect(vp, addSelected=True)

	save_start = int(cmds.playbackOptions(q=True, min=True))
	save_end = int(cmds.playbackOptions(q=True, max=True))
	print(" in run setup once :  " + str(save_start))
	print(" in run setup once :  " + str(save_end))

	cmds.playbackOptions(e=True, min=start_fr)    
	cmds.playbackOptions(e=True, max=end_fr)
	
	cmds.playbackOptions(e=True,playbackSpeed=0, maxPlaybackSpeed=0)
	cmds.currentTime(start_fr)
	cmds.play( record=True )


	#We have to evalDeferred this so after its done playing once, it will run the rest of the command
	cmds.evalDeferred("wesAnimTools.wesScreenTracker.finishSetupOnce()")
	
def makeWorldSpace():
	if not cmds.objExists("world_space"):
		world_obj = cmds.createNode('transform', name="world_space")
	else:
		world_obj = "world_space"
	cmds.textField("cameraTextField", e=True, text=world_obj)


def updateCameraSelect():
	
	#SPECIAL FUNCTION TO MAKE IT WORLD SPACE
	#Ctrl Key is On
	if chosenModifiers(kind="Ctrl") == True:
		cameras = cmds.ls(type="camera")

		cam = [x for x in cameras if "cameraShape" in x]


		if cam == [] or len(cam) > 1:
			cmds.confirmDialog(message="Couldn't find one camera, found too many, I'm confused! O_o")
		else:

			cam = cam[0].replace("Shape","")
			cmds.textField("cameraTextField", e=True, text=cam)
		setActiveWindow()
		return



	#Regular Case:

	sel = cmds.ls(sl=True)

	#Check if its only one selected
	if len(sel) != 1:
		cmds.confirmDialog(message="Comon.. just select one camera!")
		setActiveWindow()
		return	

	#Check if its a camera
	if not "cam" in sel[0].lower():	

		user_choose_space = cmds.confirmDialog( title='Confirm', \
			message="Marilyn Marcotte.. \n\n this isn't a camera.  Are you sure you want it in this space? =)", \
			button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )

		if user_choose_space == "No":
			setActiveWindow()
			return




	cmds.textField("cameraTextField", e=True, text=sel[0])

	setActiveWindow()


def updateObjectSelect():
	sel = cmds.ls(sl=True)


	# if ".e[" in sel[0]:
	# 	print "Edges are selected!!"
	# 	mel.eval("rivet;")
	# 	new_rivet = cmds.ls(sl=True)
	# 	cmds.



	if sel == [] or len(sel) > 1:
		cmds.confirmDialog(message="Dude... just select an object to track!")
		return
	

	cmds.textField("objectTextField", e=True, text=sel[0])
	setActiveWindow()

def selectWATracker(tracker):
	track_object = cmds.textField("objectTextField", q=True, text=True)
	mf_track_object = mayaCleanName(track_object)
	curve_name = "wes_"+mf_track_object+"_marker"
	marker_tracker = curve_name+"_TRACKER"
	if tracker == True:
		cmds.select(marker_tracker)
	else:
		cmds.select(track_object)

def updateWASize():
	arc_size = cmds.intField("wa_size", q=True, value=True)
	camera_name = cmds.textField("cameraTextField", q=True, text=True)
	track_object = cmds.textField("objectTextField", q=True, text=True)

	mf_track_object = mayaCleanName(track_object)
	curve_name = "wes_"+mf_track_object+"_marker"
	marker_tracker = curve_name+"_TRACKER"
	#Official Names
	#MF means Maya Friendly.  For Naming convention
	mf_track_object = mayaCleanName(track_object)
	mf_camera_name = mayaCleanName(camera_name)
	tracker_frame_grp = mf_track_object+"_"+mf_camera_name+"_GRP"


	cmds.setAttr(marker_tracker+".radius", float(arc_size)*1.35)
	the_joints = cmds.listRelatives(tracker_frame_grp, children=True, type="joint")

	setActiveWindow()

	for jnt in the_joints:
		print(jnt)
		cmds.setAttr(jnt+".radius", float(arc_size))

	setActiveWindow()

def mayaCleanName(inputName):
	new_name = inputName.replace("|","_")
	new_name = new_name.replace(":","_")
	return new_name


def wesTracker(track_object,camera_name, arc_size, theCommand, chooseColor):


	#Official Names
	#MF means Maya Friendly.  For Naming convention
	mf_track_object = mayaCleanName(track_object)
	mf_camera_name = mayaCleanName(camera_name)

	curve_name = "wes_"+mf_track_object+"_marker"
	tracker_frame_grp = mf_track_object+"_"+mf_camera_name+"_GRP"
	curve_frame_grp = mf_track_object+"_"+mf_camera_name+"_curve_GRP"
	curve_frame = mf_track_object+"_"+mf_camera_name+"_curve"
	marker_tracker = curve_name+"_TRACKER"
	marker_tracker_grp = curve_name+"_TRACKER_GRP"

	master_group = "wesTracker_"+mf_track_object

	list_of_markers = []

	color_scheme = {1 : [22, 21],
					2 : [12,20],
					3 : [29, 28],
					4 : [23, 29]}

	
	if not cmds.button("usr_start_fr", q=True, l=True) == "":
		start_fr = int(cmds.button("usr_start_fr", q=True, l=True))
		end_fr = int(cmds.button("usr_end_fr", q=True, l=True))
	else:
		start_fr = int(cmds.playbackOptions(q=True, minTime=True))
		end_fr = int(cmds.playbackOptions(q=True, maxTime=True))

	def createMarker(kind,naming,color=[12,20], cv_amount=2):
		#Joints:
		if kind == "joints":
			cmds.select(clear=True)
			tmp_name = cmds.joint(position=[0,0,0], radius=arc_size)

			#Change color
			cmds.setAttr(tmp_name+".overrideEnabled",1)
			cmds.setAttr(tmp_name+".overrideColor",color[0])

		#Curve
		if kind == "curve":
			pos_amount = []
			key_amount = []
			for point in range(cv_amount):
				pos_amount.append((0,0,0))
				key_amount.append(point)

			tmp_name = cmds.curve(d=1, p=pos_amount, k=key_amount)
			#Change color
			cmds.setAttr(tmp_name+".overrideEnabled",1)
			cmds.setAttr(tmp_name+".overrideColor",color[1])

		cmds.rename(tmp_name,naming)
		return naming


	def createTracker():

		#Check to see if theres one that exists
		if cmds.objExists(marker_tracker) == True:
			cmds.confirmDialog(message="You already created one for this object and for this camera. =)")
			return


		#Create Master Curve
		createMarker("joints", marker_tracker,)
		cmds.setAttr(marker_tracker+".scaleX", keyable=False, lock=True)
		cmds.setAttr(marker_tracker+".scaleY", keyable=False, lock=True)
		cmds.setAttr(marker_tracker+".scaleZ", keyable=False, lock=True)
		cmds.setAttr(marker_tracker+".overrideEnabled",1)
		cmds.setAttr(marker_tracker+".overrideColor",14)
		cmds.setAttr(marker_tracker+".visibility", lock=True)
		cmds.setAttr(marker_tracker+".radius", float(arc_size)*1.35)
		cmds.group(marker_tracker, name=marker_tracker_grp)
		cmds.parentConstraint(track_object, marker_tracker_grp)


		#Create Groups:
		cmds.group(empty=True,name=master_group)
		cmds.group(empty=True,name=curve_frame_grp)
		cmds.group(empty=True,name=tracker_frame_grp)
		#Make sure this group follows so the joints show at camera space?
		cmds.parentConstraint(camera_name, tracker_frame_grp, maintainOffset=False)
		cmds.parent(tracker_frame_grp,master_group)
		cmds.parent(curve_frame_grp,master_group)
		cmds.parent(marker_tracker_grp,master_group)


		for frame in range(start_fr,end_fr):

			marker_frame = curve_name+"_"+str(frame)
			createMarker("joints", marker_frame, color=color_scheme[chooseColor])


			#Constrain and key on and off
			tmp_constraint = cmds.parentConstraint(marker_tracker, marker_frame, maintainOffset=False)
			cmds.setAttr(tmp_constraint[0]+".enableRestPosition",0)
			cmds.setKeyframe(tmp_constraint[0]+".w0", time=(frame-1), value=0)
			cmds.setKeyframe(tmp_constraint[0]+".w0", time=frame, value=1)
			cmds.setKeyframe(tmp_constraint[0]+".w0", time=(frame+1), value=0)
			cmds.scaleConstraint(marker_tracker, marker_frame, offset=[0.8,0.8,0.8])

			list_of_markers.append(marker_frame)
			#Lock markers
			editAttrChannels(marker_frame,zeroOut=True)

			#Add to the group
			cmds.parent(marker_frame,tracker_frame_grp)


		#Ctrl Key is On
		if chosenModifiers(kind="Ctrl") == True:
			#Create one single curve for all the joints:
			##############################################################################################
			length_of_curve = end_fr - start_fr
			createMarker("curve",curve_frame,cv_amount=length_of_curve,color=color_scheme[color_choice])


			#Connect Curve to Joints
			counter = start_fr
			for cv_num in range(length_of_curve):
				current_marker = curve_name+"_"+str(counter)
				tmp_target = cmds.xform(current_marker, query=True, t=True, ws=True)
				cmds.xform(curve_frame+".cv["+str(cv_num)+"]", t=tmp_target)
				counter += 1

			tmp_skinCluster = cmds.skinCluster(list_of_markers,curve_frame)[0]

			counter = start_fr
			for cv_num in range(length_of_curve):
				current_marker = curve_name+"_"+str(counter)
				cmds.skinPercent(tmp_skinCluster, curve_frame+".cv["+str(cv_num)+"]",tv=(current_marker,1))
				counter += 1

			cmds.parent(curve_frame,curve_frame_grp)
			#############################################################################################
			#This is to bake out the position
			#runSetupOnce(start_fr,end_fr,master_group)

		finishSetupOnce()
		cmds.currentTime(start_fr)
		cmds.select(marker_tracker)

	def deleteTracker():
		#Ctrl Key is On
		if chosenModifiers(kind="Ctrl") == True:
			cmds.delete("wesTracker_*")
			#SET THE SETTINGS
			viewports =  cmds.getPanel( type='modelPanel' )
			for vp in viewports:
				cmds.modelEditor(vp,edit=True, joints=False, jointXray=False)
			return
		


		else:
			if cmds.objExists(master_group):
				cmds.delete(master_group)

				#if other tracker does not exists:
				if not cmds.objExists("wesTracker_*"):
					#SET THE SETTINGS
					viewports =  cmds.getPanel( type='modelPanel' )
					for vp in viewports:
						cmds.modelEditor(vp,edit=True, joints=False, jointXray=False)

					#If you want to bring it back to real time.
					#cmds.playbackOptions(edit=True, playbackSpeed=1, maxPlaybackSpeed=0)
			else:
				cmds.confirmDialog(message="Sorry, I can't find it.  But you can always go into outliner to manually delete the group node. =)")


	if theCommand == "create":
		createTracker()
	if theCommand == "delete":
		deleteTracker()


def addCurrentStartTime():
	value = int(cmds.currentTime(q=True))
	cmds.button("usr_start_fr", edit=True, l=value)

def addCurrentEndTime():
	value = int(cmds.currentTime(q=True))
	cmds.button("usr_end_fr", edit=True, l=value)



def UI(parentWindow=None, user_width=180, user_height=17, frameClosed=False):
	if not parentWindow:
		if cmds.window("wesScreenTrackerCustomUI", exists=True, resizeToFitChildren=True):
			cmds.deleteUI("wesScreenTrackerCustomUI")

		wesAnimToolsUI = cmds.window('wesScreenTrackerCustomUI', title="wesScreenTracker", sizeable=True, width=user_width)
		cmds.showWindow(wesAnimToolsUI)
		parentWindow = 'wesScreenTrackerCustomUI'

	cmds.frameLayout(collapsable=True, label="Screen Tracker", collapse=frameClosed, parent=parentWindow,width=user_width)

	cmds.rowColumnLayout(numberOfColumns=2)
	cmds.button(l="Load Object  :", bgc=[.8,.8,.8], command=lambda x:updateObjectSelect(), width=user_width*.5, height=user_height*1.3, annotation="Load object to track.")
	cmds.textField("objectTextField", ed=False, width=user_width*.5, height=user_height*1.3)#, text="majorThermopticA:rp:r_handFKA_CTRL") #<------------remove this later (, text="majorThermopticA:rp:r_handFKA_CTRL")
	cmds.setParent('..')

	cmds.rowColumnLayout(numberOfColumns=3)
	cmds.button(l="w", bgc=[.8,.8,.8], command=lambda x:makeWorldSpace(), width=user_width*.1, height=user_height*1.3, annotation="track in World Space!")
	cmds.button(l="Load Cam:", bgc=[.8,.8,.8], command=lambda x:updateCameraSelect(), width=user_width*.4, height=user_height*1.3, annotation="Ctrl + Click = Try to find a Camera")
	cmds.textField("cameraTextField", ed=False, width=user_width*.5, height=user_height*1.3)#, text="camera1") #<-------------remove (, text="camera1")
	cmds.setParent('..')

	cmds.rowColumnLayout(numberOfColumns=3)
	cmds.button("butt_timeline", l="timeline", bgc=[.4,.4,.4], command=lambda x:setFrameRange(), width=user_width*.33, height=user_height*1, annotation="Choose by timeline or selected frameRange")
	cmds.button("usr_start_fr", l="", width=user_width*.33, height=user_height*1, command=lambda x:addCurrentStartTime(), en=False, annotation="click to change to current frame")
	cmds.button("usr_end_fr",l="",width=user_width*.33, height=user_height*1, command=lambda x:addCurrentEndTime(), en=False, annotation="click to change to current frame")
	cmds.setParent('..')

	cmds.rowColumnLayout(numberOfColumns=2)
	cmds.button(l="Create Arc", command=lambda x:runWesTracker("create", chooseColor=1), width=user_width*.5, height=user_height, bgc=[.3,.6,.3], annotation="Ctrl = Adds a curve line.  Please play through once to view properly.")
	cmds.popupMenu()
	cmds.menuItem('Yellow', command=lambda x:runWesTracker("create", chooseColor=1))
	cmds.menuItem('Red', command=lambda x:runWesTracker("create", chooseColor=2))
	cmds.menuItem('Blue', command=lambda x:runWesTracker("create", chooseColor=3))
	cmds.menuItem('Green', command=lambda x:runWesTracker("create", chooseColor=4))

	cmds.button(l="Delete Arc", command=lambda x:runWesTracker("delete"), width=user_width*.5, height=user_height,bgc=[.6,.3,.3], annotation="Ctrl = delete all Arcs")
	cmds.button(l="Update Size  :", bgc=[.4,.4,.4], command=lambda x:updateWASize(), width=user_width*.5, height=user_height)
	cmds.intField("wa_size", ed=True, value=10, width=user_width*.5, height=user_height, enterCommand=lambda x:updateWASize(), annotation="Update current joint size.")
	cmds.setParent('..')


	cmds.rowColumnLayout(numberOfColumns=1)
	cmds.button(l="Select Tracker", command=lambda x:selectWATracker(tracker=True), width=user_width, height=user_height, bgc=[.5,.5,.7], annotation="You can move the tracker to another part of the body, such as the tip of the nose if you are tracking the head.")
	#cmds.button(l="Select Object", command=lambda x:selectWATracker(tracker=False), width=user_width, height=user_height, bgc=[.3,.3,.6])
	cmds.setParent('..')



	cmds.setParent('..')