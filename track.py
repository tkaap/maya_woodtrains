import maya.cmds as mc
import maya.mel as mm
from math import sqrt, sin, cos, atan,acos
from random import randint
import operator

"""
expression:
trainMoverExp
python("import track; track.moveTrainForward(\"allTrainsGroup\")");


Notes about Trains:
You can replace the geometry on the trains, and even build new trains.  Make sure to calculate/input the new distance-from-front for each axle of the train.  The script just moves each "axle" locator, it doesn't care what else you do to make the train pretty(aim/point constraints, etc)

Notes about Track Pieces:
The letter in the curve's name are important -- it associates that curve with the pegs at the end
The letters in the pegLocator names specify which other pegs connect to this peg using that letter's curve
The number at the end of the pegLocator name specifies if that peg is at the low(0) parametric end of the 
curve or the high(1) end of the curve

The .switch attr on the signpost drives the .switch attr on the peg.

For the "carpet" tracks, you can extend/edit the curve however you want.  Just rebuild it to be a uniform parametric increase from 0-1, and the train will run normally over it.


IDEAS:
Make a "Kludge" track that will procedurally generate a spline to fit between two pegs.
Make a smooth tangent that takes N% of the distance between the pegs,
Build a spline (0-1 param range), extrude some profile along it
Attach/combine/merge the necessary peg end pieces on to it.


NEEDS:
Currently the up/down ramps are M->F only.  Need some F->M up/down ramps

"""

trackLibrary = {
"mediumCurveLeft":"library|medCurveLeftTrack1"
,"mediumCurveRight":"library|medCurveRightTrack1"
,"shortCurveLeft":"library|shortCurveLeftTrack1"
,"shortCurveRight":"library|shortCurveRightTrack1"
,"miniStraight":"library|miniStraightTrack1"
,"shortStraight":"library|shortStraightTrack1"
,"mediumStraight":"library|medStraightTrack1"
,"longStraight":"library|longStraightTrack1"
,"longAscendingStraight":"library|longAscendingTrack1"
,"longDescendingStraight":"library|longDescendingTrack1"
,"bridgeSupportSimple":"library|bridgeSupport1"
,"bridgeSupportStacking":"library|bridgeSupportStackingTrack1"
,"bridgeSupportThinStacking":"library|bridgeSupportThinStackPlastic1"
,"mediumCurveRightSwitch":"library|medCurveRightSwitchTrack1"
,"mediumCurveLeftSwitch":"library|medCurveLeftSwitchTrack1"
,"mediumCurveRightSwitch2":"library|medCurveRightSwitch2Track1"
,"mediumCurveLeftSwitch2":"library|medCurveLeftSwitch2Track1"
,"mediumCurveSwitch":"library|medCurveSwitchTrack1"
,"miniReverseFemaleStraight":"library|miniRevFemaleStraightTrack1"
,"shortReverseFemaleStraight":"library|shortRevFemaleStraightTrack1"
,"medReverseFemaleStraight":"library|medRevFemaleStraightTrack1"
,"longReverseFemaleStraight":"library|longRevFemaleStraightTrack1"
,"miniReverseMaleStraight":"library|miniRevMaleStraightTrack1"
,"shortReverseMaleStraight":"library|shortRevMaleStraightTrack1"
,"medReverseMaleStraight":"library|medRevMaleStraightTrack1"
,"longReverseMaleStraight":"library|longRevMaleStraightTrack1"
,"crossTrack":"library|crossRevTrack1"
,"curveThreeSwitch":"library|curveThreeSplitTrack1"
,"maleStopper":"library|trackMaleStopperTrack1"
,"femaleStopper":"library|trackFemaleStopperTrack1"
,"maleCarpet":"maleCarpetTrack1"
,"femaleCarpet":"femaleCarpetTrack1"
,"TJunction":"longTJunctionTrack1"
}

import woodTrainsControlPanel
reload(woodTrainsControlPanel)

def reverseTrain(trainGroup=None):
	if not trainGroup:
		selection = mc.ls(sl=1,type='transform')
		print selection
		if len(selection) < 0:
			trainGroup = "allTrainsGroup|classicFreightTrainGroup"
		else:
			trainGroup = selection[0]
			
	mc.setAttr(trainGroup+".speed",-1*mc.getAttr(trainGroup+".speed"))

def controlPanel():
	reload(woodTrainsControlPanel)
	woodTrainsControlPanel.createControlPanel()

def checkTrackLibrary():
	#print trackLibrary
	allIsWell = True
	for key in trackLibrary.keys():
		if not mc.objExists(trackLibrary[key]):
			print("library object '"+trackLibrary[key]+"' for key: '"+ key + "' is not found.")
			allIsWell = False
	return allIsWell

def checkTrain(trainGroup):
	# is each axle facing the same way?
	axles = findChildren(trainGroup, "Axle")
	for axle in axles:
		print mc.getAttr(axle+".facingZeroToOneDir")

# creates a test track that uses every piece in the library.
def makeTestTrack():
	addTrackToSelected("mediumCurveRight")
	addTrackToSelected("mediumCurveRight")
	addTrackToSelected("mediumCurveRight")
	addTrackToSelected("mediumCurveRight")
	addTrackToSelected("miniStraight")
	addTrackToSelected("mediumCurveRight")
	addTrackToSelected("mediumCurveRight")
	addTrackToSelected("longStraight")
	addTrackToSelected("longStraight")
	addTrackToSelected("mediumCurveLeft")
	addTrackToSelected("mediumCurveLeft")
	addTrackToSelected("miniStraight")
	addTrackToSelected("mediumCurveLeft")
	addTrackToSelected("mediumCurveLeft")
	addTrackToSelected("mediumCurveLeft")
	addTrackToSelected("mediumCurveLeft")
	addTrackToSelected("longAscendingStraight")
	addTrackToSelected("bridgeSupportSimple")
	addTrackToSelected("shortStraight")
	addTrackToSelected("bridgeSupportSimple")
	addTrackToSelected("longDescendingStraight")
	
def makeTestTrack2():
	for i in range(4):
		addTrackToSelected("longAscendingStraight")
		addTrackToSelected("bridgeSupportStacking")
		addTrackToSelected("longAscendingStraight")
		addTrackToSelected("bridgeSupportStacking")
		addTrackToSelected("longDescendingStraight")
		addTrackToSelected("bridgeSupportSimple")
		addTrackToSelected("longDescendingStraight")
		addTrackToSelected("shortStraight")
		addTrackToSelected("mediumCurveRight")
		addTrackToSelected("mediumCurveRight")
		addTrackToSelected("mediumStraight")
		addTrackToSelected("mediumCurveRight")
		addTrackToSelected("mediumCurveRight")
		addTrackToSelected("mediumStraight")
		addTrackToSelected("mediumStraight")
		addTrackToSelected("miniStraight")
		addTrackToSelected("mediumCurveRight")
		addTrackToSelected("mediumCurveRight")
		addTrackToSelected("shortStraight")
	analyzeTrack()

def bumpDown():
	sel = mc.ls(sl=1)
	mc.move(0,0,.033333,sel, r=1,ws=1)

def bumpUp():
	sel = mc.ls(sl=1)
	mc.move(0,0,-.033333,sel, r=1,ws=1)

def bumpLeft():
	sel = mc.ls(sl=1)
	mc.move(-0.033333,0,0,sel, r=1,ws=1)

def bumpRight():
	sel = mc.ls(sl=1)
	mc.move(0.033333,0,0,sel, r=1,ws=1)
	
def bumpClockwise():
	sel = mc.ls(sl=1)
	mc.rotate(0,-1,0,sel, r=1,ws=1)
	
def bumpCounterClockwise():
	sel = mc.ls(sl=1)
	mc.rotate(0,1,0,sel, r=1,ws=1)
	
def setTrainSpeed(train='allTrainsGroup|classicFreightTrainGroup', speed=1.0,r=False):
	if r:
		try:
			mc.setAttr(train+".speed",mc.getAttr(train+".speed")*speed)
		except TypeError:
			print "Make sure to select a ~TrainGroup object!"
	else:
		try:
			mc.setAttr(train+".speed",speed)
		except TypeError:
			print "Make sure to select a ~TrainGroup object!"
	
# returns first child of target that starts with 'childPrefix'
#("body","left")
#	body
#		leftHand
#		rightHand
#		leftLeg
#
# returns 'leftHand'
#
def findChild(target,childPrefix):
	targetChildren = mc.listRelatives(target,c=True, fullPath=True)
	plen = len(childPrefix)
	for child in targetChildren:
		#print child
		childToken = child.split('|')[-1]
		#print childToken
		if childToken[0:plen] == childPrefix:
			return child
	return None

def findChildSubstring(target, substring):
	targetChildren = mc.listRelatives(target,c=True, fullPath=True)
	for child in targetChildren:
		if substring in child:
			return child
	return None

# returns all children of target that contain searchStr
#("body","left")
#	body
#		leftHand
#		rightHand
#		leftLeg
#
# returns ['leftHand','leftLeg']
#
def findChildren(target,searchStr):
	targetChildren = mc.listRelatives(target,c=True, fullPath=True)
	#plen = len(childPrefix)
	ret = []
	for child in targetChildren:
		#print child
		childToken = child.split('|')[-1]
		#print childToken
		if childToken.find(searchStr) > -1:
			ret.append(child)
	if len(ret) == 0:
		return None
	return ret

	# classify which kind of object is selected
	# "Peg" or other
	#
	# other means this is a piece of track.
	# 	Add new pieces to the 'A' peg outputs of the track 
	# 	in the direction of current track layout
	#
	# "Peg" in the name means that this is a specific output peg of a
	# track piece, and that the layout should continue from this 
	# peg. (possibly inverting the layout of the track to line up), 
	# (possibly switching the 'current direction' flag on the 'library'
	# transform)
	#
	# Do not be concerned with lining up pathCurves at this time
	#
def attachTrack(selObj, newObj):
	selObjName = selObj.split('|')[-1] 
	newObjName = newObj.split('|')[-1]
	
	pegLoc = selObjName.find("Peg")
	attachToMalePeg = False;
	attachMode = None #{StraightThrough, ReverseFemale, ReverseMale}
	Peg = None
	
	if pegLoc >= 0: # This is a peg
		# which kind of peg is it?
		fPos = selObjName.find("female")
		if fPos < 0: #male
			print "using selected male Peg: " + selObj
			attachToMalePeg = True
			mc.setAttr("library.femaleToMaleDirection",1)
		else: #female
			print "using selected female Peg: " + selObj
			attachToMalePeg = False
			mc.setAttr("library.femaleToMaleDirection",0)
		Peg = selObj
		
		# do I need to switch the library facing direction?
		# do I use the normal placement, or the inverse placement?
	else: # This is a track piece transform
		attachToMalePeg = mc.getAttr("library.femaleToMaleDirection")
		
		# Is this a reverse track?  If so, then specify which peg to re-attach to
		if selObjName.find('Rev')>=0:
			print "sel obj name " + selObjName  
			if selObjName.find("Female") >= 0:
				print 'reverse female'
				attachMode = 'ReverseFemale'
				if attachToMalePeg:
					Peg = findChild(selObj,"femalePegA1")
				else:
					Peg = findChild(selObj,"femalePegA0")
				
				newMalePeg = findChild(newObj, "malePeg")
				if not newMalePeg:
					print selObj+" has no male pegs to align"
					return
				
				alignTrackPegs(Peg,newMalePeg)
				mc.setAttr("library.femaleToMaleDirection",0)
				return
				
			else: 
				print "reverse male"
				attachMode = 'ReverseMale'
				if attachToMalePeg:
					Peg = findChild(selObj,"malePegA1")
				else:
					Peg = findChild(selObj,"malePegA0")
				
				newFemalePeg = findChild(newObj, "femalePeg")
				if not newFemalePeg:
					print selObj+" has no female pegs to align to"
					return
					
				alignTrackPegs(Peg,newFemalePeg)
				mc.setAttr("library.femaleToMaleDirection",1)
				return
				
		else: # This is a normal track, detect the first peg of the current gender
			if attachToMalePeg:
				Peg = findChild(selObj,"malePeg")
				if not Peg:
					print "ERROR: couldn't find male peg"
					return
			else:
				Peg = findChild(selObj,"femalePeg")
				if not Peg:
					print "ERROR: couldn't find female peg"
					return
 		
	print "attachTrack - using " + Peg
	pegPos = mc.xform(Peg, query=True, translation=True, ws=True)
	pegRot = mc.xform(Peg, query=True, rotation=True, ws=True)
	#print pegPos
	#print pegRot
	if newObjName.find("Peg") >= 0 :
# 		# both passed-in objects are pegs, (not the automatic usage)
# 		# so ignore their gender, and align the peg locators
# 		#
# 		print "two Pegs"
# 		newPeg = newObj
# 		newTrackObj = mc.listRelatives(newObj,p=1,f=1)[0]
# 		newPegRot = mc.xform(newPeg, query=True, rotation=True, os=True)				
# 		mc.rotate(0,pegRot[1]-newPegRot[1],0,newTrackObj)
# 		newPegWorldPos = mc.xform(newPeg, query=True, translation=True, ws=True)
# 		newObjWorldPos = mc.xform(newTrackObj, query=True, translation=True, ws=True)
# 		newPegLocalOffset = diffList(newObjWorldPos,newPegWorldPos)
# 		#print "new offset"+ str(newPegLocalOffset)
# 		mc.move(pegPos[0]-newPegLocalOffset[0], pegPos[1]-newPegLocalOffset[1], pegPos[2]-newPegLocalOffset[2] ,newTrackObj)		
		alignTrackPegs(Peg, newObj)
				
	else:
		if attachToMalePeg:
			mc.move(pegPos[0], pegPos[1], pegPos[2] ,newObj)
			mc.rotate(0,pegRot[1],0,newObj)
		else: # this is harder...
			# the offset for placing the new piece is the positive offset of the target peg plus the negative local-space offset of the attaching peg on the connecting piece.  
			
			newMalePeg = findChild(newObj, "malePeg")
			if not newMalePeg:
				print "ERROR: Couldn't locate male peg on new track object"
			newPegRot = mc.xform(newMalePeg, query=True, rotation=True, os=True)				
			mc.rotate(0,pegRot[1]-newPegRot[1],0,newObj)
			newMalePegWorldPos = mc.xform(newMalePeg, query=True, translation=True, ws=True)
			newObjWorldPos = mc.xform(newObj, query=True, translation=True, ws=True)
			newMalePegLocalOffset = diffList(newObjWorldPos,newMalePegWorldPos)
			#print "new offset"+ str(newMalePegLocalOffset)
			mc.move(pegPos[0]-newMalePegLocalOffset[0], pegPos[1]-newMalePegLocalOffset[1], pegPos[2]-newMalePegLocalOffset[2] ,newObj)
		

def alignTrackPegs(staticPeg, movingPeg):
	print "alignTrackPegs" 			
	# both passed-in objects are pegs, (not the automatic usage)
	# so ignore their gender, and align the peg locators
	#
	print "two Pegs"
	staticPegPos = mc.xform(staticPeg, query=True, translation=True, ws=True)
	staticPegRot = mc.xform(staticPeg, query=True, rotation=True, ws=True)
	#movingPeg = newObj
	
	newTrackObj = mc.listRelatives(movingPeg,p=1,f=1)[0]
	movingPegRot = mc.xform(movingPeg, query=True, rotation=True, os=True)				
	mc.rotate(0,staticPegRot[1]-movingPegRot[1],0,newTrackObj)
	movingPegWorldPos = mc.xform(movingPeg, query=True, translation=True, ws=True)
	newObjWorldPos = mc.xform(newTrackObj, query=True, translation=True, ws=True)
	movingPegLocalOffset = diffList(newObjWorldPos,movingPegWorldPos)
	#print "new offset"+ str(movingPegLocalOffset)
	mc.move(staticPegPos[0]-movingPegLocalOffset[0], staticPegPos[1]-movingPegLocalOffset[1], staticPegPos[2]-movingPegLocalOffset[2] ,newTrackObj)		
	
def makeNewTrack(key):
	if not mc.objExists('library'):
		mc.file("woodTrainTrackLibrary.ma",i=1)
	newObj = mc.duplicate(trackLibrary[key], un=1)[0]
	return newObj
		
def addTrackToSelected(key):
	sel = mc.ls(sl=1)
	if len(sel) < 1:
		newTrack = makeNewTrack(key)
		mc.move(0,0,0,newTrack)
	else:
		# pass the selected object on to 'attachTrack'
		selectedObj = sel[0]
		newTrack = makeNewTrack(key)
		attachTrack(selectedObj,newTrack)
	mc.select(newTrack,r=1)
	mc.showHidden(newTrack)
	if not mc.objExists("track"):
		mc.group(em=1,n="track")
	mc.parent(newTrack,"track")

def addTrack(key):
	newTrack = makeNewTrack(key)
	mc.parent(newTrack,w=1)
	mc.select(newTrack,r=1)
	
	
def mag(v0,v1):
	return sqrt((v0[0]-v1[0])*(v0[0]-v1[0]) + (v0[1]-v1[1])*(v0[1]-v1[1]) + (v0[2]-v1[2])*(v0[2]-v1[2]))

def diffList(v0,v1):
	return [v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2]]

def analyzeTrack2(trackGroup="track"):
	foundCt = 0
	objs = mc.listRelatives(trackGroup, ad=1,f=1,type="transform")
	malePegList = []
	femalePegList = []
	unmatchedList = []
	for obj in objs:  
		#tmp = obj.find("Peg")
		if obj.find("Peg") >= 0 and obj.find("Track") >= 0:
			if obj.find("female") >= 0:
				femalePegList.append(obj)
			else:
				malePegList.append(obj)
	print "Analyzing " + str(len(malePegList)) + " male pegs, and " + str(len(femalePegList)) + " female pegs."
	
	# reset pegs
	for fPeg in femalePegList:
		mc.setAttr(fPeg+".otherPeg","",type="string")
	for mPeg in malePegList:
		mc.setAttr(mPeg+".otherPeg","",type="string")
	
	threshold = 0.1
	for mPeg in malePegList:
		found = False
		mPegPos = mc.xform(mPeg,ws=1,translation=1,query=1)
		for fPeg in femalePegList:
			fPegPos = mc.xform(fPeg,ws=1,translation=1,query=1)
			distance = mag(mPegPos,fPegPos)
			if distance < threshold:
				mc.setAttr(mPeg+".otherPeg",fPeg,type="string")
				mc.setAttr(fPeg+".otherPeg",mPeg,type="string")
				found = True
				foundCt += 1
		if not found:
			print "didn't find match for " + mPeg
			unmatchedList.append(mPeg)
			
	print "Found " + str(foundCt) + " matching pairs" 
	if len(unmatchedList) > 0:
		mc.select(unmatchedList,r=1)
	else:
		mc.select(cl=1)

# a train object should hold the name of its current track,
#		and its position along that track (range of 0-1)
#   and its current speed
#
#		per-train attributes:			
#			currTrack - string name of track object
#			speed - positive float value of cm/frame of travelling speed
#			frontAxle - a string naming the first axle in the train
#
#		per-axle attributes
#			currTrackParamVal - float [0-1] of progress along current track curve path
#
#
# a track object should be the parent of its pathCurve (one for each exit...),
#		and know its own length.  For each exit/pathCurve, it should know
#		what track object is "next"...
#
#		per-pathCurve attributes
#			trackDistance - float value in cm of the length of this path
#			nextTrack - string name of the track object connecting to the end
#						of this path. (blank for none -- stops train) 
#	
#			
#
def pointOnTrack(trainName):
	# from the track, get its length, and its pathCurve
	# from the train, get its current position
	# for testing, just print this information to the screen.
	print "hello"
	currTrack = mc.getAttr(trainName+".currTrack")
	print currTrack
	currParamVal = mc.getAttr(trainName+".currTrackParamVal")
	print currParamVal
	currPathCurve = (currTrack+"|pathCurve1")
	currPos = mc.pointOnCurve(currPathCurve, pr=currParamVal, p=1)
	print currPos


# find all axles in the train (involves multiple cars),
# and move them each forward by the distance that the front one moves
#
# "Forward" here refers to the direction of the train's current movement,
# not it's actual orientation, or the default orientation of the track
# (which, for refrence, is the zero-to-one direction, (usually female-to-male,
#  where applicable)
#
# IDEA - add an attr to allTrainsGroup to specify how many move steps should be
# computed per frame (as an option to speed up simulation)
#
# IDEA - add an 'acceleration' attr, which can be keyed.  This would then be computed
# to affect the speed attr, allowing trains to smoothly change speeds, and even pause.
#  (And a brake, which would just be a clamped acceleration, which wouldn't throw the speed
# into reverse direction)
#
#
def moveTrainForward(trainName):
	#print "moving train " + trainName
	
	if trainName == "allTrainsGroup":
		#print "calling all trains"
		# this is the group holding all trains, recurse on all children
		for train in mc.listRelatives(trainName, c=1,f=1):
			moveTrainForward(train)
		return
	#else:
	#	print "only seeing one train " + trainName
		
	# just insist on the axles being in rough order under the parent.
	# minmally, the front axle should be first, and the back axle should
	# be last.
	axleList = findChildren(trainName, "Axle")
	trainSpeed = mc.getAttr(trainName+".speed")
	if trainSpeed < 0:
		axleList.reverse()
	mc.setAttr(axleList[0]+".isLastAxle",0)
	mc.setAttr(axleList[-1]+".isLastAxle",1)
	#print axleList	
	
	for axle in axleList:
		result = moveAxleForward2(trainName, axle)
		# if the first can cannot complete its forward movement, it 
		# doesn't move, reverses the speed, and returns None.  
		# Skip calculating the other cars for this frame.
		#
		if None == result:
			mc.setAttr(trainName+".speed",-1*mc.getAttr(trainName+".speed"))
			break

# find current track, trainSpeed, axleDirection along the track
# move the axle the appropriate distance along the appropriate track
# if there is not enough track left, move the axle to the next track,
#   and update the track direction attributes
def moveAxleForward2(trainName, axleName):
	#print "moving "+axleName+" forward2"
	trainSpeed = mc.getAttr(trainName + ".speed")
	currAxleDirection = mc.getAttr(axleName+".facingZeroToOneDir")
	#print currAxleDirection
	currTrack = mc.getAttr(axleName+".currTrack")
	#print currTrack
	currParamVal = mc.getAttr(axleName+".currTrackParamVal")
	#print currParamVal
	currPathCurve = mc.getAttr(axleName+".currTrackCurve")
	#print currPathCurve
	if currPathCurve == None:
		return
	#currTrackDistance = mc.getAttr(currPathCurve+".trackDistance")
	currTrackDistance = mc.arclen(currPathCurve)
	#print currTrackDistance
	distanceFromZeroOnThisTrack = currParamVal * currTrackDistance
	
	if currAxleDirection:
		# add speed
		newDistanceFromZeroOnThisTrack =distanceFromZeroOnThisTrack + trainSpeed 
	else:
		# subtract speed
		newDistanceFromZeroOnThisTrack =distanceFromZeroOnThisTrack - trainSpeed

	newPathCurve = None
	thisEnd = None
	remainingDistance = 0
	switchAxleDirection = False
	if newDistanceFromZeroOnThisTrack > currTrackDistance:
		# move to next track beyond the 1 peg for this pathCurve
		#print "1 " + currPathCurve
		result = getNextPathCurve(currPathCurve, '1',cycle=True,axle=axleName)
		if result:
			[otherPeg, newPathCurve] = result
			if otherPeg[-1] == '1':
				switchAxleDirection = True
				#print "switching " + axleName + "'s facing direction"
				mc.setAttr(axleName+".facingZeroToOneDir",not mc.getAttr(axleName+".facingZeroToOneDir"))
		else:
			return None
		thisEnd = otherPeg[-1]
		remainingDistance = newDistanceFromZeroOnThisTrack - currTrackDistance
	elif newDistanceFromZeroOnThisTrack < 0:
		# move to next track beyond the 0 peg for this pathCurve
		#print "0 " + currPathCurve
		result = getNextPathCurve(currPathCurve, '0',cycle=True, axle=axleName)
		if result:
			[otherPeg, newPathCurve] = result
			if otherPeg[-1] == '0':
				switchAxleDirection = True
				#print "switching " + axleName + "'s facing direction"
				mc.setAttr(axleName+".facingZeroToOneDir",not mc.getAttr(axleName+".facingZeroToOneDir"))
		else:
			return None
		thisEnd = otherPeg[-1]
		remainingDistance = -newDistanceFromZeroOnThisTrack
	
		
	#print "this end: " + str(thisEnd)

	# if I have a new path to use, update the values before calculating the new
	# parameter
	if newPathCurve:
		mc.setAttr(axleName+".currTrackCurve", newPathCurve, type="string")
		currPathCurve = newPathCurve
		currTrackDistance = mc.arclen(newPathCurve)
		
		# hopefully neither of these cases will fail (from taking a step big
		# enough to cross two track boundaries)
		if thisEnd == '0':
			newDistanceFromZeroOnThisTrack = remainingDistance
		else:
			newDistanceFromZeroOnThisTrack = currTrackDistance - remainingDistance
	
	newParamVal = newDistanceFromZeroOnThisTrack / currTrackDistance
	mc.setAttr(axleName+".currTrackParamVal", newParamVal)
	#print "maf2 using " + currPathCurve
	newPos = mc.pointOnCurve(currPathCurve, pr=newParamVal, p=1)
	mc.move(newPos[0], newPos[1], newPos[2], axleName)
	return 1
	

# for an object like "library|trackObj|pathCurveA"
# find the peg on that end of the curve "~PegA0" or "~PegA1" 
# grab its "otherPeg" attr
# find that peg's associated pathCurve*
# return what you find
#
# * this process could involve choosing between several
#  1) follow the 'letter' arg passed-in
#  2) choose one randomly (if 'random' is True)
#  3) If that object has a 'switch' setting, use the path it is directing you
#     towards.
#
def getNextPathCurve(pathCurve, end='1', letter=None, random=False, cycle=False, axle=None):
	#print "getNextPathCurve"
	pathTag = pathCurve.split('|')[-1][9]
	#print "pathTag " + pathTag
	parent = mc.listRelatives(pathCurve, p=1, f=1)
	siblings = mc.listRelatives(parent,c=1,f=1, type="transform")
	peg = None
	for obj in siblings:
		name = obj.split('|')[-1]
		if name.find(pathTag) >= 0 and name.find(end) >= 0:
			peg=obj
			break
	if not peg:
		print "ERROR no matching peg found!"
		return None
	#else:
		#print "using peg " +peg
	otherPeg = mc.getAttr(peg+".otherPeg")
	
	if (not otherPeg) or otherPeg == "":
		# this is a dead end
		#print "This looks like a dead end!"
		return None
			
	#print "initialPeg: " + peg + ", otherPeg: " + otherPeg
	otherPegTags = otherPeg[otherPeg.find("Peg")+3:-1]
	#print "other Peg tags: " + otherPegTags
	numTags = len(otherPegTags)
	parent = mc.listRelatives(otherPeg, p=1, f=1)
	siblingCurves = mc.listRelatives(parent,c=1,f=1, type="transform")
	#print siblingCurves
	
	# choose which track
	wantTag = "A" # for now, always choose 'A'
	if numTags == 0:
		print "ERROR, no tag detected for peg: " + otherPeg
		wantTag = 'A'
	elif numTags == 1:
		wantTag = otherPegTags
	else:
		# there are multiple tags
		
		# if this track piece has a switch enabled, follow it"
		if mc.attributeQuery("switch",node=otherPeg, exists=1):
			switch = mc.getAttr(otherPeg+".switch")
			if switch > -1:
				if switch < len(otherPegTags):
					wantTag = otherPegTags[switch]
				else:
					wantTag = otherPegTags[-1]
			else:
				wantTag = otherPegTags[0]
		if letter:
			wantTag = letter
			
		if random and mc.getAttr(axle+".isLastAxle"):
			if mc.attributeQuery("switch",node=otherPeg, exists=1):
				attr = otherPeg+".switch"
				connections = mc.listConnections(attr,p=1,s=1)
				if connections:
					otherAttr = connections[0]
					try:
						mc.setAttr(otherAttr,randint(0,numTags))
					except RuntimeError:
						# the attr is probably locked, skipping
						pass
					
				else:
					try:
						mc.setAttr(otherPeg+".switch",randint(0,numTags))
					except RuntimeError:
						# the attr is probably locked, skipping
						pass
					


		if cycle and mc.getAttr(axle+".isLastAxle"):
			if mc.attributeQuery("switch",node=otherPeg, exists=1):
				switch = mc.getAttr(otherPeg+".switch")
				attr = otherPeg+".switch"
				connections = mc.listConnections(attr,p=1,s=1)
				newSwitchVal = (switch + 1) % numTags
				if connections:
					otherAttr = connections[0]
					try:
						mc.setAttr(otherAttr,newSwitchVal)
					except RuntimeError:
						# the attr is probably locked, skipping
						pass
					
				else:
					try:
						mc.setAttr(otherPeg+".switch",newSwitchVal)
					except RuntimeError:
						# the attr is probably locked, skipping
						pass
					

	#print "wantTag: " + wantTag
	for obj in siblingCurves:
		splitName = obj.split('|')[-1]
		wantLoc = splitName[9:].find(wantTag)
		#print "checking " + splitName + " wantLoc: " + str(wantLoc)
		
		if splitName.find("pathCurve") >= 0 and splitName[9:].find(wantTag) >= 0:
			#print "started with " + pathCurve +", returning new curve:" + obj
			return [otherPeg, obj]
	print "ERROR - didn't find the right next pathCurve!"
	return None
	
# #track.resetTrain("trainGroup","longStraightTrackPiece3")
# #track.resetTrain("trainGroup")
# IDEA - provide option to stagger the reset, so trains can be aligned back to front
# or reset one train a given space behind another train
# NOTE: resetting trains across switch tracks can be unpredictable, so it unadviseable.
def resetTrain(forward = 1, train="", trackPiece=""):
	if(train == "") and (trackPiece == ""):
		# use selection (user should select train, then track)
		print "Select trainGroup (top level), then track piece" 
		sel = mc.ls(sl=1)
		if len(sel) == 1:
			trackPiece = sel[0]
			if mc.objExists("allTrainsGroup"):
				#mc.select("allTrainsGroup|*",r=1)
				trains = mc.listRelatives("allTrainsGroup",c=1)
				#train = mc.ls(sl=1,type="transform")[-1]
				for train in trains:
					#mc.select(train,r=1)
					#mc.select(trackPiece,add=1)
					resetTrain(forward=1,train=train,trackPiece=trackPiece)
		elif len(sel) == 2:
			train = sel[0]
			trackPiece = sel[1]
		else:
			print "Select trainGroup (top level), then track piece"
			return

	# distFromFront will be positive
	defaultSpeed = 1.0
	mc.setAttr(train+".speed",defaultSpeed)	
	axles = findChildren(train, "Axle")
	#print axles
	pathCurve = trackPiece+"|pathCurveA"
	trackPieceLength = mc.arclen(pathCurve)

	#set all axles to the first or selected track piece
	for axle in axles:
		mc.setAttr(axle+".currTrack",trackPiece,type="string")
		mc.setAttr(axle+".currTrackCurve",pathCurve,type="string")
		mc.setAttr(axle+".currTrackParamVal",0)
		if forward == 1:
			mc.setAttr(axle+".facingZeroToOneDir", 1)
		else:
			mc.setAttr(axle+".facingZeroToOneDir", 0)
	
	# move the train forward until each axle "fits" on the beginning piece,
	# and reset that axle to the beginning of the track piece
	distTraveled = 0.0
	for axle in axles:
		currDistFromFront = mc.getAttr(axle+".distFromFront")
		
		# since speed is reset to 0.1, use that to determine distance traveled
		#while distTraveled < currDistFromFront:
		#	moveTrainForward(train)
		#	distTraveled += defaultSpeed
		stepDistance = currDistFromFront-distTraveled
		mc.setAttr(train+".speed", stepDistance)
		moveTrainForward(train)
		distTraveled += stepDistance	
			
		
		
		
		#print "currDistFromFront %d"%currDistFromFront
		#print "distTraveled %f" % distTraveled
		trackPieceParam = max(0,(distTraveled - currDistFromFront) / trackPieceLength)
		
		#print "trackPieceParam %f"%trackPieceParam
		
		# the axle may have moved off of the first track piece, so reset it.
		mc.setAttr(axle+".currTrack",trackPiece,type="string") 
		mc.setAttr(axle+".currTrackCurve",pathCurve,type="string")
		mc.setAttr(axle+".currTrackParamVal",trackPieceParam)
		if forward == 1:
			mc.setAttr(axle+".facingZeroToOneDir", 1)
		else:
			mc.setAttr(axle+".facingZeroToOneDir", 0)

	
	mc.setAttr(train+".speed", defaultSpeed)
	# bump the train forward one more movement to finish resetting the final car
	moveTrainForward(train)	

# For the given train, set the distFromFront attribute on each axle
# This should only need to be done once when the train is being created.
# If this is done on a train that is mangled, it can make the train unusable.
#
# This assumes that trains are created facing the -Z axis, so the attr is set to be
# the Z-axis distance (usually the caboose is farther along Z than the engine...)
#
# The lead axle should be the first Axle of the children in DAG order (Outliner order).
def measureAxleDistances(train):
	children = mc.listRelatives(train, c=1,f=1,type='transform')
	leadAxle = None
	leadAxleZLoc = None
	for child in children:
		if 'Axle' in child: #this is an axle
			if not leadAxle: # set this as the lead axle
				leadAxle = child
				mc.setAttr(child+'.distFromFront',0.0)
				leadAxlePos = mc.xform(child, q=1,ws=1,translation=1)
				#print leadAxlePos
				leadAxleZLoc = leadAxlePos[2]
			else:
				axlePos = mc.xform(child, q=1,ws=1,translation=1)
				zDist = axlePos[2] - leadAxleZLoc 
				mc.setAttr(child+'.distFromFront',zDist)
				
			

	
def switchTracksToWoodShader(inTrackGroup="track"):
	switchTracksToShader(trackGroup=inTrackGroup, shader='woodShader2')

def switchTracksToShader(trackGroup="track", shader=None):
	print "switchTracksToWoodShader("+trackGroup+")"
	# 1) grab all mesh objects in group 'trackGroup' named "Track"
	# and not labeled "Plastic"
	objs = mc.listRelatives(trackGroup, c=1, f=1, ad=1)
	tracks = []
	for obj in objs:
		print obj
		if mc.nodeType('mesh'):
			if not obj.find('Track') >= 0:
				if obj.find('Plastic') >= 0:
					tracks.append(obj)
	print tracks
	#woodShadingGroup
	for track in tracks:
		#mc.set(track, set=woodshadingGroup, add=1)
		print "add " + track + " to woodShader ShadingGroup (blinn3SG?)"
		#blinn3SG, for the current track scene
				
		
	# 2) Assign them to the woodShader

	# 3) TODO - create a new woodShader for each object, and randomize
	# the 3dTexturePlacement object's position and orientation for
	# each piece.	
		
		
# the KludgeTrack is a flexible custom track piece that will fit into any remaining gap in
# the track layout.
# This lets you specify any two pegs, and a track piece will be generated
# along a spline between the two pegs
"""
fromPeg = selection[0]
toPeg = selection[1]
track.buildKludgeTrack()
"""
def buildKludgeTrack(fromPeg=None,toPeg=None):
	if fromPeg == None and toPeg == None:
		selection = mc.ls(sl=1,type='transform')
		if len(selection) < 2:
			raise RuntimeError, "Select at least two pegs between which to create a kludge track"
		fromPeg = selection[0]
		toPeg = selection[1]

	#fromGender is the gender of the existing fromPeg, so the new fromPeg should be the opposite.
	fromGender = 'Female' if "female" in fromPeg else 'Male'
	fromLoc = mc.xform(fromPeg,q=1,translation=1,ws=1)
	fromRot = mc.xform(fromPeg,q=1,rotation=1,ws=1)
	fromRotY = mc.xform(fromPeg,q=1,rotation=1,ws=1)[1]
	#print "fromRot %s, fromRotY %s"%(fromRot,fromRotY)
	if fromGender == 'Female': # rotate male pegs
		fromRotY = (fromRotY+180)%360
	fromVector = rotateY([0,0,-1],fromRotY)
	
	toGender = 'Female' if "female" in toPeg else 'Male'
	toLoc = mc.xform(toPeg,q=1,translation=1,ws=1)
	toRot = mc.xform(toPeg,q=1,rotation=1, ws=1)
	toRotY = toRot[1]
	#print toRotY
	if toGender == 'Female': # rotate male pegs
		toRotY = (toRotY+180)%360
	toVector = rotateY([0,0,-1],toRotY)
	#toSplineVector = rotateY([0,0,-1],toRotY+180)
	toSplineVector = rotateY([0,0,-1],toRotY)
	
	#print "fromPeg %s \n\tfromGender %s \n\tfromLoc %s \n\tfromRotY %s, \n\tfromVector %s"%(fromPeg,fromGender, fromLoc,fromRotY,fromVector)
	#print "toPeg %s \n\ttoGender %s \n\ttoLoc %s \n\ttoRotY %s, \n\ttoVector %s"%(toPeg,toGender, toLoc,toRotY,toVector)

	#1) duplicate the kludgeTrackBin
	#2) parent it under the track group
	#3) duplicate the new kludegTrack Src pieces as necessary (in case two of the same gender is needed)
	#4) move (in space) the new src pieces to the from and to locations
	#5) rotate (in space the new src pieces to the from and to rotations
	#6) build a spline with which to create the geometry
	#7) extrude the profile curve along that spline
	#8) combine & merge the new geometry with the src pieces
	#9) parent pegs under new geometry

	#10) build a spline with which to create the track anim curve  (0.625 above loc)
	#11) rename spline as needed
	#12) parent stuff
	#13) delete stuff as needed
	
	#1
	newKBin = mc.duplicate("|library|kludgeTrackBin",rr=1)[0]
	##print "newKBin %s"%newKBin
	mc.showHidden(newKBin)
	#2
	#mc.parent(newKBin, "|track")
	#newKBin = "track|"+newKBin
	##print "newKBin %s"%newKBin
	#3	
	newFromGender = "Male" if fromGender == "Female" else "Female"
	newToGender = "Male" if toGender == "Female" else "Female"
	#print "newFromGender %s, newToGender %s"%(newFromGender,newToGender)
	
	newFromSrcObj = findChildSubstring(newKBin,newFromGender)

	if newFromGender == newToGender:
		#print "DUPLICATING SRC OBJ"
		newToSrcObj = mc.duplicate(newFromSrcObj,rr=1)[0]
	else:
		newToSrcObj = findChildSubstring(newKBin,newToGender)
	##print "newFromSrcObj %s, newToSrcObj %s"%(newFromSrcObj,newToSrcObj)
	
	# Rename the pegs to reflect the direction
	newFromName = newFromGender.lower() + 'PegA0'
	newToName = newToGender.lower() + 'PegA1'
	#print "newFromName %s, newToName %s"%(newFromName, newToName)
	
	#newFromSrcObj = mc.rename(newFromSrcObj,newFromName)
	#newToSrcObj = mc.rename(newToSrcObj,newToName)
	
	
	
	newFromSrcPeg = mc.listRelatives(newFromSrcObj,c=1,f=1, type='transform')[0]
	newToSrcPeg = mc.listRelatives(newToSrcObj,c=1,f=1, type='transform')[0]
	
	newFromSrcPeg = mc.rename(newFromSrcPeg,newFromName)
	newToSrcPeg = mc.rename(newToSrcPeg,newToName)
	
	#print "newFromSrcObj %s, newToSrcObj %s"%(newFromSrcObj,newToSrcObj)
	#print "newFromSrcPeg %s, newToSrcPeg %s"%(newFromSrcPeg,newToSrcPeg)
	
	#4
	mc.move(fromLoc[0], fromLoc[1], fromLoc[2],newFromSrcObj,ws=1,a=1)
	mc.move(toLoc[0], toLoc[1], toLoc[2],newToSrcObj,ws=1,a=1)
	
	#5
	mc.rotate(0,fromRotY,0,newFromSrcObj,ws=1,a=1)
	mc.rotate(0,toRotY,0,newToSrcObj,ws=1,a=1)

	#6
	# scale -- distance between points.  Gives us an idea of how much space to use
	scale = sqrt((toLoc[0]-fromLoc[0])**2 + (toLoc[1]-fromLoc[1])**2 + (toLoc[2]-fromLoc[2])**2)
	splineScale = scale / 3.0 # amount to scale the smoothness at the spline's end
	#print "scale %f, spineScale %f"%(scale, splineScale)
	
	offsets = {'Male':2.0, 'Female':1.0} # amount the src geometry object has an offset from the peg point
	#print "offsets from %f, to %f"%(offsets[newFromGender], offsets[newToGender])
	# make a spline with 4 points: 
	# These are the core spline points, but I need to smooth the beginnings/ends out more
	#	Pt0 = fromLoc + offset*fromVector 
	#	Pt1 = Pt0 + splineScale*fromVector
	#	Pt2 = Pt3 + splineScale*toVector
	#	Pt3 = toLoc + offset*toVector
	ptF0 = addList(fromLoc,multList(offsets[newFromGender],fromVector))
	#ptF1 = addList(ptF0,multList(splineScale,fromVector))
	mRes = multList(offsets[newToGender],toSplineVector)
	#print "mRes %s"%mRes
	ptT0 = addList(toLoc,multList(offsets[newToGender],toSplineVector))
	#ptT1 = addList(ptT0,multList(splineScale,toSplineVector))
	#print ("ptF0 %s, ptT0 %s")%(ptF0, ptT0)
	
	
	# Reduce the spline scale by the offset amount
	fromSplineScale = splineScale-offsets[newFromGender]
	toSplineScale = splineScale-offsets[newToGender]
	
	#print "fromVector %s, toSplineVector %s"%(fromVector,toSplineVector)
	ptList = []
	numSmoothPoints = 2
	for i in range(numSmoothPoints+1):
		ptList.append(addList(ptF0,multList(i*fromSplineScale/numSmoothPoints,fromVector)))
	for i in range(numSmoothPoints,-1,-1):
		ptList.append(addList(ptT0,multList(i*toSplineScale/numSmoothPoints,toSplineVector)))
	#print "num pts in geomSpline %d"%len(ptList)
	geomSpline = mc.curve( p=ptList )
	#print "geomSpline %s"%geomSpline
	
	rebuildSteps = 20+int(scale)
	#rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 64 -d 3 -tol 0.01 "curve2";
	mc.rebuildCurve(geomSpline, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=rebuildSteps, d=3, tol=0.01)
	
	#7
	profile = newKBin + "|kludgeTrackProfile"
	mc.move(ptF0[0],ptF0[1],ptF0[2],profile)
	mc.rotate(0,fromRotY,0,profile,ws=1,a=1)
	#print "TODO - ROTATE THE EXTRUSION PROFILE TO MATCH NEW_FROM_PEG"
	#extrude -ch true -rn false -po 1 -et 2 -ucp 0 -fpt 0 -upn 1 -rotation 0 -scale 1 -rsp 1 "kludgeTrackBin1|kludgeTrackProfile" "curve1" ;
	
	#nurbsGeomList[0] : nurbsSurface
	#nurbsGeomList[1] : extrude node
	nurbsGeomList = mc.extrude(profile,geomSpline,ch=1,rn=False,po=0,et=2,ucp=0,fpt=0,upn=1,rotation=0,scale=1,rsp=1)
	#print "extruded %s"%nurbsGeomList

	# rotation check?
	# When changing altitudes, the extrusion twists on the curve axis
	# This can be mediated by using the .rotate attr on the extrude node
	# use the end-point verts to determine the rotate amount
	numProfilePoints=51
	"""
	scratch:
	
	find num CVs in the nurbs surface
	find bottom corner CVs
	find positions of those CVs in world space
	calculate the angle between them (in deg)
	set .rotation attr if needed
	
	
	numU = mc.getAttr("extrudedSurfaceShape1.spansU")
	numV = mc.getAttr("extrudedSurfaceShape1.spansV")

	v0 = "extrudedSurfaceShape1.cv[%d][%d]" % (49 , numV+2)
	#print v0
	v1 = "extrudedSurfaceShape1.cv[%d][%d]" % (42 , numV+2)
	#print v1

	mc.select(v0)
	mc.select(v1,add=1)
	"""
	numU = mc.getAttr("%s.spansU"%nurbsGeomList[0])
	numV = mc.getAttr("%s.spansV"%nurbsGeomList[0])

	#CVs 42 and 49 are the corners in the profile curve
	v0 = "%s.cv[%d][%d]" % (nurbsGeomList[0], 49 , numV+2)
	#print v0
	v1 = "%s.cv[%d][%d]" % (nurbsGeomList[0], 42 , numV+2)
	#print v1
	#mc.select(v0,v1)
	v0Loc = mc.xform(v0,q=1,translation=1,ws=1)
	v1Loc = mc.xform(v1,q=1,translation=1,ws=1)
	#tan(angle) = opposite/adjacent
	#arctan(opposite/adjacent) = angle
	altitude = v1Loc[1] - v0Loc[1]
	adjacent = sqrt((v1Loc[0]-v0Loc[0])**2+(v1Loc[2]-v0Loc[2])**2)
	rAngle = atan(altitude/adjacent) # in radians
	#print "angle(rads) %f"%(rAngle)
	angle = rAngle * 180 / 3.14159
	#print "angle(deg) %f"%(angle)
	mc.setAttr(nurbsGeomList[1]+'.rotation',angle)

	newExtrusionGeom = mc.nurbsToPoly(nurbsGeomList[0], mnd=1,ch=0,f=3, pt=0, pc=200, chr=0.1, ft=0.01, mel=0.001, d=0.1, ut=1, un=3, vt=1, vn=3, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)
	#print "converted %s"%newExtrusionGeom
	mc.polyNormal(newExtrusionGeom, normalMode=0, userNormalMode=0, ch=0)
	

	mc.delete(nurbsGeomList[0])
	
	#8
	#polyUnite -ch 1 -mergeUVSets 1 kludgeTrackBin1|kludgeTrackProfile kludgeTrackBin1|kludgeTrackFemaleEndSrc1 extrudedSurface1;
	unitedGeom = mc.polyUnite(newExtrusionGeom, newToSrcObj, newFromSrcObj, ch=0, mergeUVSets=1, n='kludgeTrack1')[0]
	mergedGeom = mc.polyMergeVertex(unitedGeom, d=0.01,am=1,ch=0)
	mc.polySetToFaceNormal(unitedGeom)
	mc.polySoftEdge(unitedGeom,ch=0,angle=30)
	
	mc.sets(unitedGeom,e=1,fe='kludgeTrackShader1SG')
	mc.editDisplayLayerMembers( 'trackLayer', unitedGeom)
#	-e -forceElement trackLibraryMainPathsColored_trackLibraryMainPathsColored_revStraightTracks1_blinn1SG2;

	#print "unitedGeom %s, mergedGeom %s"%(unitedGeom,mergedGeom)
	
	#9
	# if newFromGender == 'Male': # rotate male pegs
		# print "ROTATING THE FROM PEG"
	#fromRotY = (fromRotY+180)%360
	# if newToGender == 'Male': # rotate male pegs
		# print "ROTATING THE TO PEG"
	#toRotY = (toRotY+180)%360

	if newFromGender == 'Male': # rotate male pegs
		mc.rotate(0,180,0,newFromSrcPeg,r=1)
	if newToGender == 'Male': # rotate male pegs
		mc.rotate(0,180,0,newToSrcPeg,r=1)
	mc.parent(newFromSrcPeg,unitedGeom,a=1)
	mc.parent(newToSrcPeg,unitedGeom,a=1)
	
	#10
	# extend the geomSpline to build the actual spline the train runs on
	#curve -os -a -p -40.915873 0 -8.306437 curve2 ;

	mc.curve(geomSpline,a=1,os=1,p=toLoc)
	mc.reverseCurve(geomSpline,ch=0,rpo=1) # reverse to add another point
	mc.curve(geomSpline,a=1,os=1,p=fromLoc)
	mc.reverseCurve(geomSpline,ch=0,rpo=1) # reverse again to restore direction
	mc.rebuildCurve(geomSpline, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=rebuildSteps, d=3, tol=0.01)

	mc.move(0,0.625,0,geomSpline,r=1)
	mc.hide(geomSpline)
	mc.parent(geomSpline,unitedGeom)
	
	#11
	geomSpline = mc.rename(geomSpline, "pathCurveA")

	#12
	mc.parent(unitedGeom,"track")
	unitedGeom = "track|"+unitedGeom
	
	#13
	mc.delete(newKBin)
	pass


	
# IDEA - accept a spline, and build a piece around it (That's different enough to require a different proc)
# need - (calculate from curve)
#		End point genders(default to F->M, can override with args)
#		End Point locations (Easy enough)
#		End point directions (clamp to horizontal)
#			(how to handle curved (even vertically curved endpoints?)
#			(recommend that 2 units of the curve at each end stay horizontal)
#			(draw the end geom from the end point to the pointOnCurve at <offset> distance along the curve
#	
# TODO - rebuild passed-in curve to be 0-1 parameter	
def kludgeTrackFromSpline(spline, fromGender='Female',toGender='Male'):
	print "NOT FULLY IMPLEMENTED"

	#fromGender is the gender of the existing fromPeg, so the new fromPeg should be the opposite.
	#fromGender = 'Female' if "female" in fromPeg else 'Male'

	newFromGender = fromGender
	newToGender = toGender
	
	maxParam = mc.getAttr(spline+'.max')
	numSpans = mc.getAttr(spline+'.spans')
	print 'spline max param %s  spans %s'%(maxParam, numSpans)
	
	curveSize = mc.arclen(spline)
	

	
	
	# reparameterize the curve
	newSpline = mc.duplicate(spline)[0] # trainSpline
	newSpline = mc.rename(newSpline,'pathCurveA')
	newNumSpans = curveSize/2.0
	mc.rebuildCurve(newSpline, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=newNumSpans, d=3, tol=0.01)

	fromLoc = mc.pointOnCurve(newSpline,pr=0.0,p=1)
	toLoc = mc.pointOnCurve(newSpline,pr=1.0,p=1)
	print 'curve size %s, fromLoc %s, toLoc %s'%(curveSize,fromLoc,toLoc)
	
	offsets = {'Male':2.0, 'Female':1.0} # amount the src geometry object has an offset from the peg point
	
	fromOffsetParam = offsets[newFromGender]/float(curveSize)
	fromOffsetLoc = mc.pointOnCurve(newSpline, pr=fromOffsetParam, p=1)
	loc = mc.spaceLocator()
	mc.move(fromOffsetLoc[0],fromOffsetLoc[1],fromOffsetLoc[2],loc)
	
	
	toOffsetParam = 1-(offsets[newToGender]/float(curveSize))
	toOffsetLoc = mc.pointOnCurve(newSpline, pr=toOffsetParam, p=1)
	loc = mc.spaceLocator()
	mc.move(toOffsetLoc[0],toOffsetLoc[1],toOffsetLoc[2],loc)
	

	print "fromOffsetParam %s fromOffsetLoc %s"%(fromOffsetParam,fromOffsetLoc)
	detatchList = mc.detachCurve(newSpline, p=fromOffsetParam, ch=0,cos=1,rpo=0)
	detatchList2 = mc.detachCurve(detatchList[1], p=toOffsetParam, ch=0,cos=1,rpo=0)
	print detatchList
	print detatchList2
	
	geomSpline = mc.rebuildCurve(detatchList2[0], ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=newNumSpans, d=3, tol=0.01) # extrusionSpline
	geomSpline = mc.rename(geomSpline,'extrusionSpline1')
	print geomSpline
	mc.delete(detatchList)
	mc.delete(detatchList2[1])
	
	initVec = {'Male':[0,0,-1], 'Female':[0,0,-1]}
	
	fromVector = subtractList(fromOffsetLoc,fromLoc)
	NfromVector=normalize(fromVector)
	#fromRotation = mc.angleBetween(v1=initVec,v2=fromVector,er=1)
	#fromRotY = mc.angleBetween(v1=initVec,v2=fromVector,er=0)[3]
	fromRotY = -acos(dot(initVec[newFromGender],NfromVector)) * 180/3.14159
	# if abs(fromRotation[0]) > 100:
		# fromRotation[1] += 90
	
	toVector = subtractList(toOffsetLoc,toLoc)
	NtoVector = normalize(toVector)
	#toRotation = mc.angleBetween(v1=initVec,v2=toVector,er=1)
	#toRotY2 = mc.angleBetween(v1=initVec,v2=toVector,er=0)[3]
	toRotY = acos(dot(initVec[newToGender],NtoVector)) * 180/3.14159
	# if abs(toRotation[0]) > 100:
		# toRotation[1] += 90
	print "fromRotation %s, toRotation %s"%(fromRotY, toRotY)
	#print "fromRotation %s, toRotation %s"%(fromRotY2, toRotY2)
	
	#return
	
	#fromRot = mc.xform(fromPeg,q=1,rotation=1,ws=1)
	#fromRotY = fromRotation[1]
	#print "fromRot %s, fromRotY %s"%(fromRot,fromRotY)
	#if fromGender == 'Male': # rotate male pegs
	#	fromRotY = (fromRotY+180)%360
	
	#toGender = 'Female' if "female" in toPeg else 'Male'
	#toLoc = mc.xform(toPeg,q=1,translation=1,ws=1)
	#toRot = mc.xform(toPeg,q=1,rotation=1, ws=1)
	#toRotY = toRotation[1]
	#print toRotY
	#if toGender == 'Male': # rotate male pegs
	#	toRotY = (toRotY+180)%360
		
	# toVector = rotateY([0,0,-1],toRotY)
	# #toSplineVector = rotateY([0,0,-1],toRotY+180)
	# toSplineVector = rotateY([0,0,-1],toRotY)
	
	#print "fromPeg %s \n\tfromGender %s \n\tfromLoc %s \n\tfromRotY %s, \n\tfromVector %s"%(fromPeg,fromGender, fromLoc,fromRotY,fromVector)
	#print "toPeg %s \n\ttoGender %s \n\ttoLoc %s \n\ttoRotY %s, \n\ttoVector %s"%(toPeg,toGender, toLoc,toRotY,toVector)

	#1) duplicate the kludgeTrackBin
	#2) parent it under the track group
	#3) duplicate the new kludegTrack Src pieces as necessary (in case two of the same gender is needed)
	#4) move (in space) the new src pieces to the from and to locations
	#5) rotate (in space the new src pieces to the from and to rotations
	#6) build a spline with which to create the geometry
	#7) extrude the profile curve along that spline
	#8) combine & merge the new geometry with the src pieces
	#9) parent pegs under new geometry

	#10) build a spline with which to create the track anim curve  (0.625 above loc)
	#11) rename spline as needed
	#12) parent stuff
	#13) delete stuff as needed
	
	#1
	newKBin = mc.duplicate("|library|kludgeTrackBin",rr=1)[0]
	##print "newKBin %s"%newKBin
	mc.showHidden(newKBin)
	#2
	#mc.parent(newKBin, "|track")
	#newKBin = "track|"+newKBin
	##print "newKBin %s"%newKBin
	#3	
	#newFromGender = "Male" if fromGender == "Female" else "Female"
	#newToGender = "Male" if toGender == "Female" else "Female"
	#print "newFromGender %s, newToGender %s"%(newFromGender,newToGender)
	
	newFromSrcObj = findChildSubstring(newKBin,newFromGender)

	if newFromGender == newToGender:
		#print "DUPLICATING SRC OBJ"
		newToSrcObj = mc.duplicate(newFromSrcObj,rr=1)[0]
	else:
		newToSrcObj = findChildSubstring(newKBin,newToGender)
	##print "newFromSrcObj %s, newToSrcObj %s"%(newFromSrcObj,newToSrcObj)
	
	# Rename the pegs to reflect the direction
	newFromName = newFromGender.lower() + 'PegA0'
	newToName = newToGender.lower() + 'PegA1'
	#print "newFromName %s, newToName %s"%(newFromName, newToName)
	
	#newFromSrcObj = mc.rename(newFromSrcObj,newFromName)
	#newToSrcObj = mc.rename(newToSrcObj,newToName)
	
	
	
	newFromSrcPeg = mc.listRelatives(newFromSrcObj,c=1,f=1, type='transform')[0]
	newToSrcPeg = mc.listRelatives(newToSrcObj,c=1,f=1, type='transform')[0]
	
	newFromSrcPeg = mc.rename(newFromSrcPeg,newFromName)
	newToSrcPeg = mc.rename(newToSrcPeg,newToName)
	
	print "newFromSrcObj %s, newToSrcObj %s"%(newFromSrcObj,newToSrcObj)
	print "newFromSrcPeg %s, newToSrcPeg %s"%(newFromSrcPeg,newToSrcPeg)
	
	#4
	mc.move(fromLoc[0], fromLoc[1], fromLoc[2],newFromSrcObj,ws=1,a=1)
	mc.move(toLoc[0], toLoc[1], toLoc[2],newToSrcObj,ws=1,a=1)
	
	#5
	mc.rotate(0,fromRotY,0,newFromSrcObj,ws=1,a=1)
	mc.rotate(0,toRotY,0,newToSrcObj,ws=1,a=1)
#	return
	#6
	# scale -- distance between points.  Gives us an idea of how much space to use
	# scale = sqrt((toLoc[0]-fromLoc[0])**2 + (toLoc[1]-fromLoc[1])**2 + (toLoc[2]-fromLoc[2])**2)
	# splineScale = scale / 3.0 # amount to scale the smoothness at the spline's end
	# #print "scale %f, spineScale %f"%(scale, splineScale)
	
	# offsets = {'Male':2.0, 'Female':1.0} # amount the src geometry object has an offset from the peg point
	# #print "offsets from %f, to %f"%(offsets[newFromGender], offsets[newToGender])
	# # make a spline with 4 points: 
	# # These are the core spline points, but I need to smooth the beginnings/ends out more
	# #	Pt0 = fromLoc + offset*fromVector 
	# #	Pt1 = Pt0 + splineScale*fromVector
	# #	Pt2 = Pt3 + splineScale*toVector
	# #	Pt3 = toLoc + offset*toVector
	ptF0 = addList(fromLoc,multList(offsets[newFromGender],fromVector))
	# #ptF1 = addList(ptF0,multList(splineScale,fromVector))
	# mRes = multList(offsets[newToGender],toSplineVector)
	# #print "mRes %s"%mRes
	ptT0 = addList(toLoc,multList(offsets[newToGender],toVector))
	# #ptT1 = addList(ptT0,multList(splineScale,toSplineVector))
	# #print ("ptF0 %s, ptT0 %s")%(ptF0, ptT0)
	
	
	# # Reduce the spline scale by the offset amount
	# fromSplineScale = splineScale-offsets[newFromGender]
	# toSplineScale = splineScale-offsets[newToGender]
	
	# #print "fromVector %s, toSplineVector %s"%(fromVector,toSplineVector)
	# ptList = []
	# numSmoothPoints = 2
	# for i in range(numSmoothPoints+1):
		# ptList.append(addList(ptF0,multList(i*fromSplineScale/numSmoothPoints,fromVector)))
	# for i in range(numSmoothPoints,-1,-1):
		# ptList.append(addList(ptT0,multList(i*toSplineScale/numSmoothPoints,toSplineVector)))
	# #print "num pts in geomSpline %d"%len(ptList)
	# geomSpline = mc.curve( p=ptList )
	# #print "geomSpline %s"%geomSpline
	
	# rebuildSteps = 20+int(scale)
	# #rebuildCurve -ch 1 -rpo 1 -rt 0 -end 1 -kr 0 -kcp 0 -kep 1 -kt 0 -s 64 -d 3 -tol 0.01 "curve2";
	# mc.rebuildCurve(geomSpline, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=rebuildSteps, d=3, tol=0.01)
	
	#7
	profile = newKBin + "|kludgeTrackProfile"
	mc.move(ptF0[0],ptF0[1],ptF0[2],profile)
	mc.rotate(0,fromRotY,0,profile,ws=1,a=1)
	#print "TODO - ROTATE THE EXTRUSION PROFILE TO MATCH NEW_FROM_PEG"
	#extrude -ch true -rn false -po 1 -et 2 -ucp 0 -fpt 0 -upn 1 -rotation 0 -scale 1 -rsp 1 "kludgeTrackBin1|kludgeTrackProfile" "curve1" ;
	
	#nurbsGeomList[0] : nurbsSurface
	#nurbsGeomList[1] : extrude node
	nurbsGeomList = mc.extrude(profile,geomSpline,ch=1,rn=False,po=0,et=2,ucp=1,fpt=0,upn=0,rotation=0,scale=1,rsp=1)
	#print "extruded %s"%nurbsGeomList
	

	
	# rotation check?
	# When changing altitudes, the extrusion twists on the curve axis
	# This can be mediated by using the .rotate attr on the extrude node
	# use the end-point verts to determine the rotate amount
	numProfilePoints=51
	"""
	scratch:
	
	find num CVs in the nurbs surface
	find bottom corner CVs
	find positions of those CVs in world space
	calculate the angle between them (in deg)
	set .rotation attr if needed
	
	
	numU = mc.getAttr("extrudedSurfaceShape1.spansU")
	numV = mc.getAttr("extrudedSurfaceShape1.spansV")

	v0 = "extrudedSurfaceShape1.cv[%d][%d]" % (49 , numV+2)
	#print v0
	v1 = "extrudedSurfaceShape1.cv[%d][%d]" % (42 , numV+2)
	#print v1

	mc.select(v0)
	mc.select(v1,add=1)
	"""
	numU = mc.getAttr("%s.spansU"%nurbsGeomList[0])
	numV = mc.getAttr("%s.spansV"%nurbsGeomList[0])

	#CVs 42 and 49 are the corners in the profile curve
	v0 = "%s.cv[%d][%d]" % (nurbsGeomList[0], 49 , numV+2)
	#print v0
	v1 = "%s.cv[%d][%d]" % (nurbsGeomList[0], 42 , numV+2)
	#print v1
	#mc.select(v0,v1)
	v0Loc = mc.xform(v0,q=1,translation=1,ws=1)
	v1Loc = mc.xform(v1,q=1,translation=1,ws=1)
	#tan(angle) = opposite/adjacent
	#arctan(opposite/adjacent) = angle
	altitude = v1Loc[1] - v0Loc[1]
	adjacent = sqrt((v1Loc[0]-v0Loc[0])**2+(v1Loc[2]-v0Loc[2])**2)
	rAngle = atan(altitude/adjacent) # in radians
	#print "angle(rads) %f"%(rAngle)
	angle = rAngle * 180 / 3.14159
	if v1Loc[1] < v0Loc[1]:
		print "no invert rotation"
	else:
		angle*=-1
		print "invert rotation"
		
	print "angle(deg) %f"%(angle)
	mc.setAttr(nurbsGeomList[1]+'.rotation',angle)
	# return
	
	newExtrusionGeom = mc.nurbsToPoly(nurbsGeomList[0], mnd=1,ch=0,f=3, pt=0, pc=200, chr=0.1, ft=0.01, mel=0.001, d=0.1, ut=1, un=3, vt=1, vn=3, uch=0, ucr=0, cht=0.2, es=0, ntr=0, mrt=0, uss=1)
	#print "converted %s"%newExtrusionGeom
	mc.polyNormal(newExtrusionGeom, normalMode=0, userNormalMode=0, ch=0)
	

	mc.delete(nurbsGeomList[0])
	
	#8
	#polyUnite -ch 1 -mergeUVSets 1 kludgeTrackBin1|kludgeTrackProfile kludgeTrackBin1|kludgeTrackFemaleEndSrc1 extrudedSurface1;
	unitedGeom = mc.polyUnite(newExtrusionGeom, newToSrcObj, newFromSrcObj, ch=0, mergeUVSets=1, n='splineTrack1')[0]
	mergedGeom = mc.polyMergeVertex(unitedGeom, d=0.03,am=1,ch=0)
	mc.polySetToFaceNormal(unitedGeom)
	mc.polySoftEdge(unitedGeom,ch=0,angle=30)
	
	mc.sets(unitedGeom,e=1,fe='kludgeTrackShader1SG')
	mc.editDisplayLayerMembers( 'trackLayer', unitedGeom)
#	-e -forceElement trackLibraryMainPathsColored_trackLibraryMainPathsColored_revStraightTracks1_blinn1SG2;

	#print "unitedGeom %s, mergedGeom %s"%(unitedGeom,mergedGeom)
	
	#9
	if newFromGender == 'Male': # rotate male pegs
		mc.rotate(0,180,0,newFromSrcPeg,r=1)
	if newToGender == 'Male': # rotate male pegs
		mc.rotate(0,180,0,newToSrcPeg,r=1)	
	#mc.rotate(fromRotation[0],fromRotation[1],fromRotation[2],newFromSrcPeg)
	#mc.rotate(toRotation[0],toRotation[1],toRotation[2],newToSrcPeg)
	mc.parent(newFromSrcPeg,unitedGeom)
	mc.parent(newToSrcPeg,unitedGeom)
	
	#10
	# extend the geomSpline to build the actual spline the train runs on
	#curve -os -a -p -40.915873 0 -8.306437 curve2 ;

	# mc.curve(geomSpline,a=1,os=1,p=toLoc)
	# mc.reverseCurve(geomSpline,ch=0,rpo=1) # reverse to add another point
	# mc.curve(geomSpline,a=1,os=1,p=fromLoc)
	# mc.reverseCurve(geomSpline,ch=0,rpo=1) # reverse again to restore direction
	# mc.rebuildCurve(geomSpline, ch=0, rpo=1, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=newNumSpans, d=3, tol=0.01)

	mc.move(0,0.625,0,newSpline,r=1)
	mc.hide(newSpline)
	mc.parent(newSpline,unitedGeom)
	
	#11
	#geomSpline = mc.rename(geomSpline, "pathCurveA")

	#12
	if not mc.objExists('track'):
		mc.group(em=1,n='track')
	mc.parent(unitedGeom,"track")
	unitedGeom = "track|"+unitedGeom
	
	#13
	# mc.delete(newKBin)
	# mc.delete(geomSpline)
	mc.move(fromLoc[0],fromLoc[1],fromLoc[2],unitedGeom+'.scalePivot',unitedGeom+'.rotatePivot')

	pass

	
def addList(a,b):
	return map(operator.__add__,a,b)
def subtractList(a,b):
	return map(operator.__sub__,a,b)
def multList(scalar,list):
	return [i * scalar for i in list] 
def cross(v1,v2):
	i = (v1[1]*v2[2])-(v1[2]*v2[1])
	j = (v1[2]*v2[0])-(v1[0]*v2[2])
	k = (v1[0]*v2[1])-(v1[1]*v2[0])
	return [i,j,k]
def dot(a,b):
  return reduce( operator.add, map( operator.mul, a, b))
def normalize(a):
	mag = sqrt(dot(a,a))
	return multList(1/float(mag),a)
  
def rotateY(a,amt):
	#print "rotateY amt %d (%s)"%(amt,str(a))
	if amt==0:
		return a
	amt = (amt%360)/180.0*3.14159
	xAmt = (sin(amt))*a[2] + (cos(amt))*a[0]
	zAmt = -1*(sin(amt))*a[0] + (cos(amt))*a[2]	
	#ret =(int(xAmt),int(a[1]),int(zAmt))
	ret =((xAmt),(a[1]),(zAmt))
	#print "rotatY xAmt %3.2f, zAmt %3.2f (%s)"%(xAmt,zAmt,str(ret))
	return ret

	
#placeAxle(axle,trackPiece,axleDistance)
	
# 	mc.setAttr(train+"|frontAxle.currTrackParamVal",1.0)
# 	mc.setAttr(train+"|frontAxle.currTrack",trackPiece,type="string")
# 	
# 	mc.setAttr(train+"|rearAxle.currTrack",trackPiece,type="string")
# 	dff = mc.getAttr(train+"|rearAxle.distFromFront")
# 	rearParam = 1.0-(dff / mc.arclen(trackPiece+"|pathCurve1"))
# 	mc.setAttr(train+"|rearAxle.currTrackParamVal",rearParam)


# def placeAxle(axle, trackPiece, distanceFromZero):
# 	#reverse = False
# 	#if distanceFromZero < 0:
# 	#	reverse = True
# 	#	distanceFromZero *= -1
# 	
# 	currTrackPiece = trackPiece
# 	trackPieceLength = 0.0
# 	while True:
# 		trackPieceLength = mc.arclen(currTrackPiece+"|pathCurve1")
# 		if distanceFromZero > trackPieceLength:
# 			#move to next track piece
# 			distanceFromZero -= trackPieceLength
# 			currTrackPiece = mc.getAttr(currTrackPiece+"|curvePath.nextTrack")
# 			if not currTrackPiece:
# 				break
# 		elif -distanceFromZero > trackPieceLength:
# 			distanceFromZero += trackPieceLength
# 
# 			else:	
# 				currTrackPiece = mc.getAttr(currTrackPiece+"|curvePath.prevTrack")
# 				if not currTrackPiece:
# 					break
# 			print axle + " next track Piece"
# 		else:
# 			break
# 			
# 	# the current track piece should be this axle's final position
# 	if not reverse:
# 		trackPieceParam = distanceFromZero / trackPieceLength
# 	else:
# 	 	trackPieceParam = 1- (distanceFromZero / trackPieceLength)
# 	
# 	print "setting " + axle + " to param: " + str(trackPieceParam)
# 	mc.setAttr(axle+".currTrack",currTrackPiece,type="string")
# 	mc.setAttr(axle+".currTrackParamVal",trackPieceParam)


#track.checkTrackLibrary() #checks to ensure that all of the pieces exist in the scene
#attachTrack("longStraightTrackPiece3","medStraightTrackPiece2")

#track.addTrack("mediumCurveLeft")
#track.addTrackToSelected("mediumCurveLeft")
#track.addTrackToSelected("mediumCurveRight")




# max = 10.0
# for x in xrange(0.0,max+1):
# 	pVal = x / max
# 	print pVal
# 	curvePos = mc.pointOnCurve("curve1", pr=pVal, p=1)
# 	mc.move(curvePos[0], curvePos[1], curvePos[2], "pCube1")



