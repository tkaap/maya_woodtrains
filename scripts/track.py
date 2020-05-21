import maya.cmds as mc
import maya.mel as mm
from math import sqrt, sin, cos, atan,acos
from random import randint, choice
import operator
import string
import time
import ast
import re
from copy import deepcopy
import pprint
import os

"""

To launch the tool using the UI:
import woodTrainsControlPanel2 as wc
reload(wc)
wc.main()



TROUBLESHOOTING:
Playback works best in DG Evaluation mode.
The playback works best when Maya isn't looping to play the same frames.  It's best to set the animation range to around 10,000 frames, so that Maya doesn't loop.

NOTES:
Notes about Trains:
You can replace the geometry on the trains, and even build new trains.  Make sure to calculate/input the new distance-from-front for each axle of the train.  The script just moves each "axle" locator, it doesn't care what else you do to make the train pretty(aim/point constraints, etc)

Notes about Track Pieces:
The letter in the curve's name are important -- it associates that curve with the pegs at the end
The letters in the pegLocator names specify which other pegs connect to this peg using that letter's curve
The number at the end of the pegLocator name specifies if that peg is at the low(0) parametric end of the 
curve or the high(1) end of the curve

The .switch attr on the signpost drives the .switch attr on the peg.

For the "carpet" tracks, you can extend/edit the curve however you want.  Just rebuild it to be a uniform parametric increase from 0-1, and the train will run normally over it.

Expression that drives the trains:
trainMoverExp
python("import track; track.moveAllTrainsForward()");

NEEDS:
Method to export a built track for use in another scene.  A way to clean out all of the trains out of a scene.  If this is extended to contain a train-builder, a similar way to extract the trains will be needed.


IDEA: Store a database (dict) in the library node that holds where each train (or even axle) should be reset to at some initial frame.  This can store axle name, pathcurve name, and parametric value.  This should also store the train's switchData dict, if any, so that the state of the train on track is exactly 
repeatable.  Something like the repr method for python objects
DONE

IDEA: button on UI to cycle a signPost's value.
Select the peg that the switch is connected to (use buttons), then
Button to cycle the signPost's switch value
DONE


IDEA - TODO - Create a groundPlane around the 2-D bounding box of the track
    Complicated ground planes could incorporate negative space items
    

BUG - When the train speed is high enough, trains can get skip entirely across the smallest pieces and get confused about where to go next (crossTrackCrazy).  This might require having switch tracks on at least one side the short track to cause the failure.  The trains will reverse unexpectedly, or even break apart.   Make sure that trains know how to multi-step across short tracks in a single simulation step.

IDEA: Be able to force a switch to always go one direction (DONE, can key the post).  Be able to disable one option from a triple-switch. (e.g. disable the middle option).

IDEA: When pressing the playback button, set evaluation to be DG mode. DONE

IDEA: Add Button to Setup Utilities to set the playback range to be some huge number (10,000 frames)   
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
,"bridgeSupportSimple":"library|bridgeSupportSimple1"
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
,"maleCarpet":"library|maleCarpetTrack1"
,"femaleCarpet":"library|femaleCarpetTrack1"
,"TJunction":"library|longTJunctionTrack1"
,"magicTrack":"library|magicTrack"
#,"magicTrack":"library|kludgeTrack"
}



# import woodTrainsControlPanel
# reload(woodTrainsControlPanel)

def reverseTrain(trainGroup=None):
    if not trainGroup:
        selection = mc.ls(sl=1,type='transform')
        print selection
        if len(selection) < 0:
            trainGroup = "allTrainsGroup|classicFreightTrainGroup"
        else:
            trainGroup = selection[0]
            
    mc.setAttr(trainGroup+".speed",-1*mc.getAttr(trainGroup+".speed"))

# def controlPanel():
    # reload(woodTrainsControlPanel)
    # woodTrainsControlPanel.createControlPanel()

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
    print "setTrainSpeed %f"%speed
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
#    body
#        leftHand
#        rightHand
#        leftLeg
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

# like findChild, but doesn't require the substring be a prefix
# returns the first child found
def findChildSubstring(target, substring):
    targetChildren = mc.listRelatives(target,c=True, fullPath=True)
    for child in targetChildren:
        if substring in child:
            return child
    return None

def findDescendantSubstring(target, substring):
    targetChildren = mc.listRelatives(target,ad=True, fullPath=True)
    for child in targetChildren:
        if substring in child:
            return child
    return None

    
# Assumes that all transform children of the train transform are axles
# except for the final transform.  This is assumed to be geometry
#
def findAxles(train):
    children=mc.listRelatives(train,c=1,fullPath=True)
    if not children:
        return
    return children[:-1]
        
        

# returns all children of target that contain searchStr
#("body","left")
#    body
#        leftHand
#        rightHand
#        leftLeg
#
# returns ['leftHand','leftLeg']
#
def findChildren(target,searchStr, fullPath=True):
    targetChildren = mc.listRelatives(target,c=True, fullPath=True)
    if not targetChildren:
        return None
    #plen = len(childPrefix)
    ret = []
    for child in targetChildren:
        #print child
        childToken = child.split('|')[-1]
        #print childToken
        if childToken.find(searchStr) > -1:
            if fullPath:
                ret.append(child)
            else:
                ret.append(childToken)
    if len(ret) == 0:
        return None
    return ret

# Returns true is this is a reverse track.  That is, if the 'A' pegs are the same gender
#
# 
# 
def isReverseTrack(trackName):
    #print "isReverseTrack %s"%trackName
    
    aPegs = findChildren(trackName, "PegA")
    if not aPegs:
        return False
    if len(aPegs) != 2:
        return False
    if ("female" in aPegs[0]) and ("female" in aPegs[1]):
        return True
    if ("male" in aPegs[0]) and ("    male" in aPegs[1]):
        return True
    return False


# findPegA0
#
# Returns the full path of the A0 Peg of a track
#
# These pegs can have multiple letters, so this returns
# the peg that contains 'A' and 0
#
matchPegA0 = re.compile('.*Peg[B-Z]*A[B-Z]*0')
def findPegA0(track):
    children = mc.listRelatives(track,c=1,f=1)
    if not children:
        return None
    for child in children:
        matches = matchPegA0.match(child)
        if matches:
            return child
    return None
    
matchPegA1 = re.compile('.*Peg[B-Z]*A[B-Z]*1')    
def findPegA1(track):
    children = mc.listRelatives(track,c=1,f=1)
    if not children:
        return None
    for child in children:
        matches = matchPegA1.match(child)
        if matches:
            return child
    return None

def pegIsMale(peg):
    return False if 'female' in peg else True
def pegNumber(peg):
    return peg[-1]
    
def findMalePegA(track):
    #print 'findMalePegA %s' % track
    children = mc.listRelatives(track,c=1,f=1)
    onePeg = None
    for child in children:
        if '|malePeg' in child:
            if 'A' in child:
                if '0' in child: # mechanism to prefer returning the 0 peg before the 1 peg
                    return child
                else:
                    onePeg = child
    return onePeg
        
def findFemalePegA(track):
    #print 'findFemalePegA %s' % track
    children = mc.listRelatives(track,c=1,f=1)
    for child in children:
        if '|femalePeg' in child:
            if 'A' in child:
                if '0' in child: # mechanism to prefer returning the 0 peg before the 1 peg
                    return child
                else:
                    onePeg = child                
    return None


    
# classify which kind of object is selected
# "Peg" or other
#
# other means this is a piece of track.
#     Add new pieces to the 'A' peg outputs of the track 
#     in the direction of current track layout (zeroToOneDirection == True is the default)
#   - If zeroToOneDirection is true, attach to the A1 peg
#   - otherwise attach to the A0 Peg
#    Attach to the complimentary peg of the new track if possible 
#     - otherwise attach to the other track if possible (then toggle the zeroToOneDirection) 
#    - otherwise fail (place new track piece at origin?)
#
# "Peg" in the name means that this is a specific output peg of a
# track piece, and that the layout should continue from this 
# peg. (possibly inverting the layout of the track to line up), 
# (switching the 'zeroToOneDirection' flag on the 'library' transform)
#
# TODO - search/track the connection direction based on the A0 and A1 pegs, not on the shape's name
# (This gets broken when using the carpet, stopper, and cross tracks)
#
# Args:
#     baseObj - the object that is not moved during the attachment step
#     newObj - the object that is moved.
#
# Note:
#     zeroToOneDirection refers to the orientation of the track as we lay it out.  If the track is being 
# laid down in the direction from its 0 peg to its 1 peg, then we are in the zeroToOneDirection
#
def attachTrack(baseObj=None, newObj=None):
    #print 'attach track'
    if (baseObj==None) and (newObj==None):
        selection = mc.ls(sl=1)
        if len(selection) < 2:
            print "You must select or pass in two objects"
            return
        baseObj = selection[0]
        newObj = selection[1]
    
    # Find the information about the base object
    baseObjName = baseObj.split('|')[-1] 

    baseObjIsPeg = 'Peg' in baseObj.split('|')[-1] 
    baseObjPeg = None # the active Peg for the base object
    baseObjPegIsMale = None
    baseObjPegIsZero = None
    overrideZeroToOneDirection = False
    if baseObjIsPeg:
        #print "baseObj is a peg %s" % baseObj
        baseObjPeg = baseObj
        # zeroToOneDirection determined by this peg
        overrideZeroToOneDirection = True
    else:
        #print 'baseObjIs NOT peg, find active peg'
        # Find the active peg in the base object
        basePegs = findChildSubstring(baseObj, 'Peg')
        zeroToOneDirection = mc.getAttr("library.zeroToOneDirection")
        if zeroToOneDirection:
            baseObjPeg = findPegA1(baseObj)
        else:
            baseObjPeg = findPegA0(baseObj)
        
    baseObjPegIsMale = pegIsMale(baseObjPeg)
    baseObjPegIsZero = True if '0' == baseObjPeg[-1] else False
    if overrideZeroToOneDirection:
        zeroToOneDirection = not baseObjPegIsZero
        
    #print "baseObj %s %s %s %s" % (baseObj, baseObjPeg.split('|')[-1], "Male" if baseObjPegIsMale else "Female", "0" if baseObjPegIsZero else "1")
    
    # now find the same information for the newObj
    newObjName = newObj.split('|')[-1]

    newObjIsPeg = 'Peg' in newObj.split('|')[-1] 
    newObjPeg = None # the active Peg for the new object
    newObjPegIsMale = None
    if newObjIsPeg:
        #print "newObj is a peg %s" % newObj
        newObjPeg = newObj
        #set newObj to its track
        newObj = mc.listRelatives(newObjPeg,p=1)[0]
    else:
        #print 'newObjIs NOT peg, try to find a compatible peg'
        # Find the active peg in the new object (to compliment the one we've found)        
        if baseObjPegIsMale:
            newObjPeg = findFemalePegA(newObj)
        else:
            newObjPeg = findMalePegA(newObj)
    
    if not newObjPeg:
        print "Couldn't find a compatible peg"
        mc.move(0,0,0,newObj,ws=1)
        return 
        
    newObjPegIsMale = pegIsMale(newObjPeg)
    newObjPegIsZero = True if '0' == newObjPeg[-1] else False
    #print " newObj %s %s %s %s" % (newObj, newObjPeg.split('|')[-1], "Male" if newObjPegIsMale else "Female", "0" if newObjPegIsZero else "1")
    
    if baseObjPegIsMale == newObjPegIsMale:
        print "attachTrack - Both pegs are the same gender, can't attach, exiting"
        return
        
    # If needed, swap the zeroToOneDirection
    # 
    if mc.getAttr("library.zeroToOneDirection") != newObjPegIsZero:
        print "Changing zeroToOneDirection! to %s"%(newObjPegIsZero)
        mc.setAttr("library.zeroToOneDirection", newObjPegIsZero)

    # if zeroToOneDirection != newObjPegIsZero:
        # print "need to switch zeroToOneDirection"
        # if mc.getAttr("library.zeroToOneDirection") != newObjPegIsZero:
            # print "Changing zeroToOneDirection! to %s"%(newObjPegIsZero)
            # mc.setAttr("library.zeroToOneDirection", newObjPegIsZero)
        # else:
            # print "library's value already matches, don't bother"            
    # else:
        # print "don't need to switch zeroToOneDirection: current:%s, newObjPegIsZero:%s"%(zeroToOneDirection,newObjPegIsZero)
        # print "library:%s, newObjPegIsZero:%s"%(mc.getAttr("library.zeroToOneDirection"),newObjPegIsZero)
    
    # Now the pegs are determined, find their locations and offsets
    # The A0 Peg is always at the object origin
    # If we're using a 1 peg from the newObj, find it's offset and rotation
    #
    # move and counterRotate the newObj track
    #

    #NOTE - fails attaching a medRightCurve to a medCurveRightSwitch2 track on peg B0
    
    # Rotate first, then move using the peg's offset to the local object
    baseObjPegRot = mc.xform(baseObjPeg, query=True, rotation=True, ws=True)
    newObjPegRot = mc.xform(newObjPeg, query=True, rotation=True, os=True)
    newObjRot = mc.xform(newObj, query=True, rotation=True, ws=True)
    newObjNewRot = subtractList(baseObjPegRot,newObjPegRot)
    
    mc.rotate(newObjNewRot[0], newObjNewRot[1], newObjNewRot[2], newObj,ws=1)
    
    baseObjPegPos = mc.xform(baseObjPeg, query=True, translation=True, ws=True)
    
    newObjPegPos = mc.xform(newObjPeg, query=True, translation=True, ws=True)
    newObjPos = mc.xform(newObj, query=True, translation=True, ws=True)
    newObjNewPos = subtractList(baseObjPegPos,subtractList(newObjPegPos,newObjPos))
    
    #newObjPegLocalPos = mc.xform(newObjPeg, query=True, translation=True, os=True)
    #newObjNewPos2 = subtractList(baseObjPegPos,newObjPegLocalPos)
    
    #print "%s: Pos %s, Rot %s"%(baseObjPeg, baseObjPegPos, baseObjPegRot[1])
    #print "%s: Pos %s, Rot %s"%(newObjPeg, newObjPegPos, newObjPegRot[1])
    mc.move(newObjNewPos[0],newObjNewPos[1],newObjNewPos[2],newObj,ws=1)
    return
    
        
def alignTrackPegs(staticPeg, movingPeg):
    #print "alignTrackPegs"             
    # both passed-in objects are pegs, (not the automatic usage)
    # so ignore their gender, and align the peg locators
    #
    #print "two Pegs"
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
        trackLibraryFile = "woodTrainTrackLibrary.ma"
        try:
            mc.file(trackLibraryFile,i=1)
        except RuntimeError:
            libraryFileLocation = os.environ['WOODTRAINS_LIBRARY_LOCATION']
            if os.altsep == None:
                sep = os.sep
            else:
                sep = os.altsep        
            trackLibraryPath = libraryFileLocation + sep + trackLibraryFile
            mc.file(trackLibraryPath,i=1)
    newObj = mc.duplicate(trackLibrary[key], un=1)[0]
    return newObj
        
def addTrackToSelected(key):
    sel = mc.ls(sl=1)
    #print sel
    if len(sel) < 1:
        newTrack = makeNewTrack(key)
        mc.move(0,0,0,newTrack)
    else:
        # pass the selected object on to '/'
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
    if not mc.objExists("track"):
        mc.group(em=1,n="track")
    mc.showHidden(newTrack)        
    mc.parent(newTrack,"track")
    mc.select(newTrack,r=1)    

def importTrainLibrary():
    if not mc.objExists("trainsLibrary"):
        # import train library scene file
        trainLibraryFile = "woodTrainTrainLibrary.ma"
        try:
            mc.file(trainLibraryFile,i=1)
        except RuntimeError:
            libraryFileLocation = os.environ['WOODTRAINS_LIBRARY_LOCATION']
            if os.altsep == None:
                sep = os.sep
            else:
                sep = os.altsep        
            trainLibraryPath = libraryFileLocation + sep + trainLibraryFile
            mc.file( trainLibraryPath, i=1, type="mayaAscii", mergeNamespacesOnClash=False, rpr="woodTrainTrainLibrary" , options="v=0", pr=1)
    
def addTrain(trainName=None):
    """
    Create a new duplicate of the train named <trainName> (or <trainName>Group)
    import the train library scene file if necessary
        Creates the animation expression, if necesssary
    """
    if not trainName:
        trainName = 'classicFreightTrain'
    
    importTrainLibrary()
    #if not mc.objExists("trainsLibrary"):
    #    # import train library scene file
    #    mc.file( "scenes/woodTrainTrainLibrary.ma", i=1, type="mayaAscii", mergeNamespacesOnClash=False, rpr="woodTrainTrainLibrary" , options="v=0", pr=1)
    

    if mc.objExists("|trainsLibrary|%s"%trainName):
        dupName = "|trainsLibrary|%s"%trainName
    elif mc.objExists("|trainsLibrary|%sGroup"%trainName):
        dupName = "|trainsLibrary|%sGroup"%trainName
    else:
        print "%s not found"%trainName
        return

    newTrain = mc.duplicate(dupName, rr=1,un=1)[0]
    
    # rename on-board cameraShapes to unique node names
    # This is a temporary need for a tool that errors with non-unique cameras
    print "newTrain name is %s"%newTrain
        
    #engineerCameraShape
    #tankerCamera1Shape
    #trainCameraShape
    #newTrain: "classicFreightTrainGroup1"
    
    camShapeNameHash = ''.join([choice(string.ascii_letters) for i in range(4)])

    cameraShapePaths = [
        '|trainGeom|engineJoint|engineCar|engineerCamera|engineerCameraShape',
        '|trainGeom|tankerJoint|tankerCar|tankerCamera1|tankerCamera1Shape',
        '|trainGeom|engineJoint|engineCar|trainCamera|trainCameraShape',
    ]
    cameraNames = [
        'engineerCamera_',
        'tankerCamera1_',
        'trainCamera_',
    ]
    for path,shape in zip(cameraShapePaths,cameraNames):
        mc.rename(newTrain+path, shape+camShapeNameHash+"_Shape")

    
    
    mc.parent(newTrain,"allTrainsGroup")
    mc.setAttr(newTrain+".speed",1)
    spd = mc.getAttr(newTrain+".speed")
    #print "addTrain %s, setting speed, %d" %(newTrain,spd)

    if not mc.objExists("allTrainsGroup"):
        mc.group(em=1,n="allTrainsGroup")
    createAnimExpression()
    
    #newTrain = makeNewTrain(trainName)
    return newTrain
    
def createAnimExpression():
    """
    # Creates the train movement expression

    trainMoverExp
    #python("import track; track.moveTrainForward(\"allTrainsGroup\")");
    python("import track; track.moveTrainForward()");
    """
    if not mc.objExists('trainMoverExp'):
        mc.expression( s='python(\"import track; track.moveAllTrainsForward()\");', n='trainMoverExp', o='allTrainsGroup' )
        
    pass
    
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

# Rather than selecting mismatched pegs, create an annotation node for them
# Also, matched pegs should be checked for existing annotation node children, which
#     should be deleted
def analyzeTrack3(qDummy="", trackGroup="track"):
    #print("num args = %d"%(len(args)))
    initialSelection = mc.ls(sl=1)
    foundCt = 0
    print("using trackGroup: %s"%trackGroup)
    objs = mc.listRelatives(trackGroup, ad=1,f=1,type="transform")
    malePegList = []
    femalePegList = []
    #unmatchedList = []
    for obj in objs:  
        #tmp = obj.find("Peg")
        if obj.find("Peg") >= 0 and obj.find("Track") >= 0:
            if 'annotation' in obj:
                #annotation, do nothing
                continue
            elif obj.find("female") >= 0:
                femalePegList.append(obj)
                unAnnotatePeg(obj) # remove all existing annotations from female pegs
            else:
                malePegList.append(obj)
    print "Analyzing " + str(len(malePegList)) + " male pegs, and " + str(len(femalePegList)) + " female pegs."
    
    # start with all female pegs listed as unmatched, remove them from this 
    # list as they are matched
    unmatchedList = deepcopy(femalePegList)
    
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
                unAnnotatePeg(mPeg)
                if fPeg in unmatchedList:
                    unmatchedList.remove(fPeg)
                # Removing this break statement lets multiple pegs match to this peg.
                # While it would be more efficent to break here, the carpet tracks only work
                # with these multiple matches
                #break 
                    
        if not found:
            print "didn't find match for " + mPeg
            # start with no male pegs listed as unmatched, add them to the unmatched
            # list now if they have failed to find a match
            unmatchedList.append(mPeg)
            
    print "Found " + str(foundCt) + " matching pairs" 
    
    # add annotations to all pegs that are unmatched
    if len(unmatchedList) > 0:
        for peg in unmatchedList:
            if 'female' in peg:
                annotatePeg(peg,halfHeight=1)
            else:
                annotatePeg(peg)
    if initialSelection:
        mc.select(initialSelection,r=1)
    else:
        mc.select(cl=1)

def unAnnotatePeg(peg):
    # check for annotation nodes
    # delete any you find
    annotations = mc.listRelatives(peg, type='annotationShape', ad=1, f=1)
    if annotations:
        for annotation in annotations:
            parent = mc.listRelatives(annotation,p=1,f=1)
            mc.delete(parent)
        
def annotatePeg(peg,halfHeight=False):
    pegPos = mc.xform(peg,ws=1,translation=1,query=1)
    pegNames = peg.split('|')
    pegShortName = pegNames[-1]
    
    annotations = mc.listRelatives(peg, type='annotationShape', ad=1, f=1)
    if annotations:
        #Do not add an additional annotation if one already exists
        print "peg %s aleady has an annotation, skipping"%peg
        return
    
    mc.select(peg)
    if halfHeight:
        annotationShape = mc.annotate( peg, tx=pegNames[-2]+'|'+pegNames[-1] + " unmatched", p=(pegPos[0],pegPos[1]+5,pegPos[2]))
    else:
        annotationShape = mc.annotate( peg, tx=pegNames[-2]+'|'+pegNames[-1] + " unmatched", p=(pegPos[0],pegPos[1]+10,pegPos[2]))
        
    aTransform = mc.listRelatives(annotationShape, p=1)
    #print "parent = %s"%aTransform
    aTransform = mc.rename(aTransform,pegShortName+"_annotation")
    #print "parent = %s"%aTransform
    mc.parent(aTransform,peg)
    
    #annotationShape = mc.createNode('annotationShape',parent=aTransform)
    #mc.setAttr(annotationShape+'.text',"aasdasd",type="string")
    pass
    
# a train object should hold the name of its current track,
#        and its position along that track (range of 0-1)
#   and its current speed
#
#        per-train attributes:            
#            currTrack - string name of track object
#            speed - positive float value of cm/frame of travelling speed
#            frontAxle - a string naming the first axle in the train
#
#        per-axle attributes
#            currTrackParamVal - float [0-1] of progress along current track curve path
#
#
# a track object should be the parent of its pathCurve (one for each exit...),
#        and know its own length.  For each exit/pathCurve, it should know
#        what track object is "next"...
#
#        per-pathCurve attributes
#            trackDistance - float value in cm of the length of this path
#            nextTrack - string name of the track object connecting to the end
#                        of this path. (blank for none -- stops train) 
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

def toggleTrackSetupDirection():
    #newVal = not mc.getAttr("library.femaleToMaleDirection")
    newVal = not mc.getAttr("library.zeroToOneDirection")
    #mc.setAttr("library.femaleToMaleDirection",newVal)
    mc.setAttr("library.zeroToOneDirection",newVal)
    return newVal

# IDEA - a method to cycle through all of the pegs of a track piece
#
# If no track is passed, use the first selection
# If a track is selected or passed, call selectActivePeg to select the active peg
# If a peg is selected, change the selection to be the next peg in DAG order beneath its parent track piece
#
def selectPegCycle(trackPiece=None):
    print 'cycle peg'
    if trackPiece:
        mc.select(trackPiece,r=1)
        selectActivePeg()

    sel = mc.ls(sl=1)        
    if "Track" in sel[0]:
        selectActivePeg()
        
    if "Peg" in sel[0]:
        parent = mc.listRelatives(sel[0],parent=1,f=1)
        pegs = findChildren(parent,"Peg", fullPath=True)
        numPegs = len(pegs)
        currPeg = sel[0].split('|')[-1]
        index = 0
        found = False
        while index < numPegs:
            if '|'+currPeg in pegs[index]:
                found = True
                break
            index+=1
        if not found:
            return
            
        nextIndex = (index+1)%len(pegs)
        mc.select(pegs[nextIndex],r=1)
    return
    
# Selects the peg on the A track that is in the current layout direction
#
def selectActivePeg():
    #print 'select active peg'
    #1) look for selection
    #    (if it's a peg, do nothing)
    #2) If it's a track piece, grab the A peg in the current direction
    sel = mc.ls(sl=1)
    if not sel:
        return
    if 'Peg' in sel[0]:
        # This is a peg, return
        #print 'peg selected, returning'
        return
    
    aPegs = findChildren(sel[0],"PegA")
    if not aPegs:
        if 'Track' in sel[0]:
            parent = mc.listRelatives(sel[0],p=1)[0]
            aPegs = findChildren(parent,"PegA")
        else:
            print "Select active peg didn't find any pegs in %s" % sel[0]
            return
    
    #if not mc.getAttr("library.femaleToMaleDirection"):
    if not mc.getAttr("library.zeroToOneDirection"):
        # select Female Peg
        for peg in aPegs:
            if "female" in peg:
                mc.select(peg,r=1)
                return
    else:
        # select Male Peg
        for peg in aPegs:
            if not "female" in peg:
                mc.select(peg,r=1)
                return
        pass
    
    mc.select(aPegs[0],r=1)
    #print 'reached end, returning'
        
# for moving down, set dir=-1
def movePieceVertically(dir=1):
    amount = 6.1*dir
    mc.move(0,amount,0,r=1)

def rebuildCarpetCurve(curve=None):
    if not curve:
        selection = mc.ls(sl=1)
        if len(selection) > 0:
            curve = selection[0]
        else:
            return
    #mc.rebuildCurve(curve, ch=0, rp0=1,rt=4,end=1,kr=0,kcp=0,kep=1,kt=0,s=4,d=3,tol=0.01)
    newCurve = mc.rebuildCurve(curve, ch=0, rpo=1,rt=4,end=1,kr=0,kcp=0,kep=1,kt=0,s=4,d=3,tol=0.01)
    mc.select(newCurve)
        
# change the .switch value on the signPost to the next valid 
# value.
# The signPost can be specified either by selection of the post or peg, or by passing the
# peg name
def cycleSignPostValue(qDummy=None, peg=None):
    currentPeg = None
    currentSignPost = None
    if peg == None:
        # check selection
        sel = mc.ls(sl=1)
        if len(sel) < 1:
            return
        selObj = sel[0]
        selObjName = selObj.split('|')[-1]
        if 'Peg' in selObjName:
            currentPeg = selObj
        elif 'signPost' in selObjName:
            currentSignPost = selObj
        elif 'Track' in selObjName:
            # try to find a signPost in a track
            track = selObj
            currentSignPost = findChild(track,'signPost')
        elif 'post' in selObjName or 'arrowPlastic' in selObjName:
            # try to find a signPost if one of its sub-objects is selected
            parent = mc.listRelatives(selObj,p=1,f=1)[0]
            if 'signPost' in parent:
                currentSignPost = parent

    #print "cycleSignPostValue using %s and %s"%(currentPeg,currentSignPost)
                
    if not currentPeg and not currentSignPost:
        print "cycleSignPostValue couldn't determine a signPost, skipping"
        return
        
    if not currentPeg:
        # use currentSignPost to determine a Peg
        currentPeg = mc.listConnections(currentSignPost+'.switch', type='transform')[0]
        pass
    if not currentSignPost:
        # use currentPeg to determing a signPost
        otherPegTags = currentPeg[currentPeg.find("Peg")+3:-1]
        numTags = len(otherPegTags)
        if numTags > 1:
            currentSignPost = mc.listConnections(currentPeg+'.switch', type='transform')[0]
        else:
            print "currentPeg %s doesn't have a switch" % currentPeg
            return
        pass
    mc.select(currentSignPost)    
    
    otherPegTags = currentPeg[currentPeg.find("Peg")+3:-1]
    numTags = len(otherPegTags)
    switch = mc.getAttr(currentPeg+".switch")
    newSwitchVal = (switch + 1) % numTags    
    mc.setAttr(currentSignPost+'.switch',newSwitchVal)
        
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
def moveAllTrainsForward():
    #if trainName == "allTrainsGroup":
    #print "calling all trains"
    # this is the group holding all trains, recurse on all children
    trains = mc.listRelatives('allTrainsGroup', c=1,f=1)
    if trains:
        #frameStart = time.clock()
        for train in trains:
            moveTrainForward(train)
        #elapsed = time.clock() - frameStart
        #print "frame moveTrainForward time: %5.5f,  %5.5f/train\n\n"%(elapsed,elapsed/len(trains))
    return
    
def moveTrainForward(trainName, tempSpeed=None):
    # tempSpeed should override the train's speed

    #print "moving train " + trainName

    #else:
    #    print "only seeing one train " + trainName
        
    # just insist on the axles being in rough order under the parent.
    # minmally, the front axle should be first, and the back axle should
    # be last.
    
    #findAxleStart = time.clock()
    axleList = findAxles(trainName)
    #findAxleElapsed = time.clock()-findAxleStart
    #print "findAxle Time %6.6fs"%findAxleElapsed
    
    if tempSpeed != None:
        trainSpeed = tempSpeed
    else:
        trainSpeed = mc.getAttr(trainName+".speed")
        if trainSpeed == 0:
            return
        if trainSpeed < 0:
            axleList.reverse()
            
    mc.setAttr(axleList[0]+".isLastAxle",0)
    mc.setAttr(axleList[0]+".isFirstAxle",1)
    mc.setAttr(axleList[-1]+".isLastAxle",1)
    mc.setAttr(axleList[-1]+".isFirstAxle",0)
    #print axleList    
    
    numAxles = len(axleList)
    #print "numAxles: %d"%numAxles
    #totalTime = 0
    #trainSpeed = mc.getAttr(trainName + ".speed")
    for axle in axleList:
        #startTime = time.clock()
        result = moveAxleForward2(trainName, axle, trainSpeed)
        #elapsed = (time.clock()-startTime)
        #print "axleTime: %5.5fs"%elapsed
        #totalTime += elapsed
        
        # if the first can cannot complete its forward movement, it 
        # doesn't move, reverses the speed, and returns None.  
        # Skip calculating the other cars for this frame.
        #
        if None == result:
            #print "reversing train!"
            mc.setAttr(trainName+".speed",-1*mc.getAttr(trainName+".speed"))
            break
    #print "totalTrainAxleTime %5.5f - %5.5f/axle"%(totalTime, totalTime / numAxles)


# retrieves the string attr data on the train transform, 
# converts it to a dict and returns it
#
def getSwitchData(trainName):
    dataStr = mc.getAttr(trainName+'.switchData')
    if dataStr and not (dataStr == ''):
        #print "getSwitchData - making dict from string: %s"%dataStr
        switchData = ast.literal_eval(dataStr)
        return switchData
    return {}

# sets the switch data dict as a string on the train transform
def setSwitchData(trainName, switchDataDict):
    mc.setAttr(trainName+'.switchData',str(switchDataDict), type="string")
    
# find current track, trainSpeed, axleDirection along the track
# move the axle the appropriate distance along the appropriate track
# if there is not enough track left, move the axle to the next track,
#   and update the track direction attributes
#
# Return values:
#     None - movement was obsctructed, reverse this axle (and therefore this train)
#    1 - movement was completed, do nothing else (this includes when a train is not connected to any track)
#
def moveAxleForward2(trainName, axleName, trainSpeed):
    #print "moving %s forward by %f"%(axleName, trainSpeed)
    
    #trainSpeed = mc.getAttr(trainName + ".speed")
    currAxleDirection = mc.getAttr(axleName+".facingZeroToOneDir")
    #print currAxleDirection
    #currTrack = mc.getAttr(axleName+".currTrack")
    #print currTrack
    currParamVal = mc.getAttr(axleName+".currTrackParamVal")
    #print currParamVal
    currPathCurve = mc.getAttr(axleName+".currTrackCurve")
    #print currPathCurve
    if currPathCurve == None:
        # Train is not connected to any track, stop processing it.
        return 1
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


#    switchDataStr = mc.getAttr(trainName+'.switchData')
    #print "train %s switchData %s"%(trainName, switchDataStr)
    #switchData = switchDataStr
    

    
    followedSwitch = False
    newPathCurve = None
    thisEnd = None
    remainingDistance = 0
    switchAxleDirection = False
    
    if newDistanceFromZeroOnThisTrack > currTrackDistance:
    
        # move to next track beyond the 1 peg for this pathCurve
        #print "1 " + currPathCurve
        switchData = getSwitchData(trainName)    
        cachedLetter = switchData[currPathCurve] if currPathCurve in switchData else None
        result = getNextPathCurve(currPathCurve, '1', letter=cachedLetter, cycle=True,axle=axleName)
        if result:
            [otherPeg, newPathCurve, followedSwitch] = result
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
        switchData = getSwitchData(trainName)    
        cachedLetter = switchData[currPathCurve] if currPathCurve in switchData else None
        result = getNextPathCurve(currPathCurve, '0', letter=cachedLetter, cycle=True, axle=axleName)
        if result:
            [otherPeg, newPathCurve, followedSwitch] = result
            if otherPeg[-1] == '0':
                switchAxleDirection = True
                #print "switching " + axleName + "'s facing direction"
                mc.setAttr(axleName+".facingZeroToOneDir",not mc.getAttr(axleName+".facingZeroToOneDir"))
        else:
            return None
        thisEnd = otherPeg[-1]
        remainingDistance = -newDistanceFromZeroOnThisTrack
    
    if followedSwitch:
        #print "moveAxleForward - gotNewParamCurve %s" % newPathCurve
        #switchData = getSwitchData(trainName)
        if not (currPathCurve in switchData):
            newPathLetter = newPathCurve[-1]
            switchData[currPathCurve] = newPathLetter

        # After the last axle makes its switch decision, remove
        # the entry from this train's switch data
        if mc.getAttr(axleName+".isLastAxle"):
            #print "removing entry for %s"%currPathCurve
            del switchData[currPathCurve]
            
        #print switchData
        setSwitchData(trainName, switchData)
        
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
    if newParamVal < 0 or newParamVal > 1:
        return None
    
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
    followedSwitch = False
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
        #print "No matching peg found -- reverse!"
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
            followedSwitch = True
            #print "following choice %s"%wantTag
        if letter:
            wantTag = letter
        
        #if mc.getAttr(axle+".isLastAxle"):
        #if mc.getAttr(axle+".distFromFront") == 0:
        if mc.getAttr(axle+".isFirstAxle"):
            # Choose the next switch setting randomly
            if random: #and mc.getAttr(axle+".isLastAxle"):
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
                        

            # Choose the next switch setting cyclicly
            if cycle: #and mc.getAttr(axle+".isLastAxle"):
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
            
            # Remove this path from this train's switchData dict
            
            

    #print "wantTag: " + wantTag
    for obj in siblingCurves:
        splitName = obj.split('|')[-1]
        wantLoc = splitName[9:].find(wantTag)
        #print "checking " + splitName + " wantLoc: " + str(wantLoc)
        
        if splitName.find("pathCurve") >= 0 and splitName[9:].find(wantTag) >= 0:
            #print "started with " + pathCurve +", returning new curve:" + obj
            #print "getNextPath returning followedSwitch %s"%("True" if followedSwitch else "False")
            return [otherPeg, obj, followedSwitch]
    print "ERROR - didn't find the right next pathCurve!"
    return None
    
# #track.resetTrain("trainGroup","longStraightTrackPiece3")
# #track.resetTrain("trainGroup")
# NOTE: resetting trains across switch tracks can be unpredictable, so it unadviseable.
#
# Modes:
#     Find track piece by selection or name passed in
#     If trackPiece is not passed in or selected, use the first track piece in the track list
#
#    Find train by selection or name passed in
#    If the train is not passed-in or selected, reset all trains
#
# IDEA - provide option to stagger the reset, so trains can be aligned back to front
# or reset one train a given space behind another trains
#
def resetTrain(forward = 1, train="", trackPiece="", speed=1.0):
    if(train == "") and (trackPiece == ""):
        # use selection (user should select train, then track)
        #print "Select trainGroup (top level), then track piece" 
        sel = mc.ls(sl=1)
        if len(sel) == 1:
            if 'track' in mc.listRelatives(sel[0], p=1):
                trackPiece = sel[0]
            else:
                train = sel[0]
        elif len(sel) == 2:
            train = sel[0]
            trackPiece = sel[1]
        else:
            print "Select trainGroup (top level), then track piece"
            return

    # If train wasn't passed or selected, reset all trains
    if not train:
        if mc.objExists("allTrainsGroup"):
            #mc.select("allTrainsGroup|*",r=1)
            trains = mc.listRelatives("allTrainsGroup",c=1)
            #train = mc.ls(sl=1,type="transform")[-1]
            for train in trains:
                #mc.select(train,r=1)
                #mc.select(trackPiece,add=1)
                resetTrain(forward=1,train=train,trackPiece=trackPiece)

    if trackPiece == "":
        sel = mc.ls(sl=1)
        if len(sel) == 1:
            if 'track' in mc.listRelatives(sel[0], p=1):
                trackPiece = sel[0]
        
        if not trackPiece:        
            # if trackPiece is not determined, choose the first one that isn't a switch.
            if mc.objExists("track"):
                tracks = mc.listRelatives("track")
                for track in tracks:
                    if "Switch" in track:
                        continue
                    else:
                        trackPiece = track
                        break
    
    if not train or not trackPiece:
        #This shouldn't happen, but still...
        print "resetTrain can't determine what you intend..."
        return
    
    #print "resetTrain train: %s to track %s"%(train,trackPiece)
    
    # distFromFront will be positive
    defaultSpeed = speed #1.0
    mc.setAttr(train+".speed",defaultSpeed)    
    #axles = findChildren(train, "Axle")
    axles = findAxles(train)
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
        #    moveTrainForward(train)
        #    distTraveled += defaultSpeed
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

    # bump the train forward one more movement to finish resetting the final car
    moveTrainForward(train)    
    mc.setAttr(train+".speed", defaultSpeed)

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
                
            
def isWoodShaded(track):
    #print "isWoodShaded %s"% track

    if mc.nodeType(track) == 'transform':
        plugs = mc.listRelatives(track, c=1,type='mesh')
        if plugs:
            shape = plugs[0]
    else:
        shape = track
        
    connections = mc.listConnections(shape, d=1, p=1)
    if connections:
        for c in connections:
            if 'dagSetMembers' in c:
                setName = c.split('.')[0]
                plugs = mc.listConnections(setName+'.surfaceShader',d=1,p=1)
                if plugs:
                    shaderPlug = plugs[0]
                    shader = shaderPlug.split('.')[0]
                    plugs = mc.listConnections(shader+'.color',d=1,p=1)
                    if plugs:
                        texturePlug = plugs[0]
                        texture = texturePlug.split('.')[0]
                        if mc.nodeType(texture) == 'wood':
                            return True    
    else:
        print "not changing to wood shader %s"%shape
    return False
    
def switchTracksToWoodShader(qDummy="", inTrackGroup="track"):
    selection = mc.ls(sl=1) # store current selection
    switchTracksToShader(trackGroup=inTrackGroup, shader='woodShader2')
    if selection:
        # restore saved selection
        mc.select(selection,r=1)
    else:
        mc.select(cl=1)

def switchTracksToShader(qDummy="", trackGroup="track", shader=None):
    #print "switchTracksToWoodShader("+trackGroup+")"
    #print "not fully implemented"
    # 1) grab all mesh objects in group 'trackGroup' named "Track"
    # and not labeled "Plastic"
    objs = mc.listRelatives(trackGroup, c=1, f=1, ad=1)
    tracks = []
    for obj in objs:
        #print obj
        if mc.nodeType(obj) == 'mesh':
            if obj.find('Track') >= 0:
                if not obj.find('Plastic') >= 0:
                    # check if object is already attached to a wood shader
                    if shader == 'woodShader2' and not isWoodShaded(obj):
                        tracks.append(obj)
    #print tracks
    #woodShadingGroup
    for track in tracks:
        #mc.set(track, set=woodshadingGroup, add=1)
        #print "add " + track + " to woodShader ShadingGroup (blinn3SG?)"
        #blinn3SG, for the current track scene
        
        # 2) TODO - create a new woodShader for each object, and randomize
        # the 3dTexturePlacement object's position and orientation for
        # each piece.    
        newWoodTex = mc.shadingNode('wood',asTexture=1)
        newPlace3dTex = mc.shadingNode('place3dTexture',asUtility=1)
        mc.setAttr(newPlace3dTex+'.rotate',randint(0,180),randint(0,180),randint(0,180))
        mc.setAttr(newPlace3dTex+'.scale',5,5,5)
        mc.setAttr(newPlace3dTex+'.visibility',0)
        mc.setAttr(newWoodTex+'.veinColor',0.316,0.158,0.198)
        mc.setAttr(newWoodTex+'.age',0)
        mc.connectAttr(newPlace3dTex+'.wim[0]',newWoodTex+'.pm')
        newLambert = mc.shadingNode('lambert',asShader=1)# lambert;
        #// Result: lambert4 // 
        newShadingGroup = mc.sets (renderable=1, noSurfaceShader=1, empty=1, name='trackWoodMaterialSG1')
        #// Result: lambert4SG // 
        mc.connectAttr (newLambert+'.outColor', newShadingGroup+'.surfaceShader', f=1)
        mc.connectAttr (newWoodTex+'.outColor', newLambert+'.color', f=1)
        trackParent = mc.listRelatives(track,p=1,f=1)
        if len(trackParent):
            trackParent = trackParent[0]
        mc.parent(newPlace3dTex,trackParent)
        
        #3)  add object to shadingGroup set
        mc.sets(track,fe=newShadingGroup)
        
        
# the MagicTrack is a flexible custom track piece that will fit into any remaining gap in
# the track layout.
# This lets you specify any two pegs, and a track piece will be generated
# along a spline between the two pegs
"""
fromPeg = selection[0]
toPeg = selection[1]
track.buildMagicTrack()
"""
def buildMagicTrack(fromPeg=None,toPeg=None):
    if fromPeg == None and toPeg == None:
        selection = mc.ls(sl=1,type='transform')
        if len(selection) < 2:
            raise RuntimeError, "Select at least two pegs between which to create a magic track"
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

    #1) duplicate the magicTrackBin
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
    newKBin = mc.duplicate("|library|magicTrackBin",rr=1)[0]
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
    #    Pt0 = fromLoc + offset*fromVector 
    #    Pt1 = Pt0 + splineScale*fromVector
    #    Pt2 = Pt3 + splineScale*toVector
    #    Pt3 = toLoc + offset*toVector
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
    profile = newKBin + "|magicTrackProfile"
    mc.move(ptF0[0],ptF0[1],ptF0[2],profile)
    mc.rotate(0,fromRotY,0,profile,ws=1,a=1)
    #print "TODO - ROTATE THE EXTRUSION PROFILE TO MATCH NEW_FROM_PEG"
    #extrude -ch true -rn false -po 1 -et 2 -ucp 0 -fpt 0 -upn 1 -rotation 0 -scale 1 -rsp 1 "magicTrackBin1|magicTrackProfile" "curve1" ;
    
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
    #polyUnite -ch 1 -mergeUVSets 1 magicTrackBin1|magicTrackProfile magicTrackBin1|magicTrackFemaleEndSrc1 extrudedSurface1;
    unitedGeom = mc.polyUnite(newExtrusionGeom, newToSrcObj, newFromSrcObj, ch=0, mergeUVSets=1, n='magicTrack1')[0]
    mergedGeom = mc.polyMergeVertex(unitedGeom, d=0.01,am=1,ch=0)
    mc.polySetToFaceNormal(unitedGeom)
    mc.polySoftEdge(unitedGeom,ch=0,angle=30)
    
    mc.sets(unitedGeom,e=1,fe='magicTrackShader1SG')
    mc.editDisplayLayerMembers( 'trackLayer', unitedGeom)
#    -e -forceElement trackLibraryMainPathsColored_trackLibraryMainPathsColored_revStraightTracks1_blinn1SG2;

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
    #pass
    return unitedGeom


def findTrainCamera(train, camera):
    #print "engineerCamera train:%s camera:%s"%(train, camera)
    camera = findDescendantSubstring(train, camera)
    return camera
    
# IDEA - commands to switch the camera to the train's on-board cameras
#     
def switchCameras(cameraName):
    focusPanel = mc.getPanel( withFocus=1)
    panelType = mc.getPanel(typeOf=focusPanel)
    if panelType != 'modelPanel':
        # grab the Persp View panel instead
        focusPanel = mc.getPanel( withLabel='Persp View')
    
    if cameraName and mc.objExists(cameraName):
        mc.modelPanel(focusPanel, e=1,camera=cameraName)
    else:
        mc.modelPanel(focusPanel, e=1,camera='persp')

    

# IDEA - accept a spline, and build a piece around it (That's different enough to require a different proc)
# need - (calculate from curve)
#        End point genders(default to F->M, can override with args)
#        End Point locations (Easy enough)
#        End point directions (clamp to horizontal)
#            (how to handle curved (even vertically curved endpoints?)
#            (recommend that 2 units of the curve at each end stay horizontal)
#            (draw the end geom from the end point to the pointOnCurve at <offset> distance along the curve
#    
# TODO - rebuild passed-in curve to be 0-1 parameter    
def magicTrackFromSpline(spline, fromGender='Female',toGender='Male'):
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
    #    fromRotY = (fromRotY+180)%360
    
    #toGender = 'Female' if "female" in toPeg else 'Male'
    #toLoc = mc.xform(toPeg,q=1,translation=1,ws=1)
    #toRot = mc.xform(toPeg,q=1,rotation=1, ws=1)
    #toRotY = toRotation[1]
    #print toRotY
    #if toGender == 'Male': # rotate male pegs
    #    toRotY = (toRotY+180)%360
        
    # toVector = rotateY([0,0,-1],toRotY)
    # #toSplineVector = rotateY([0,0,-1],toRotY+180)
    # toSplineVector = rotateY([0,0,-1],toRotY)
    
    #print "fromPeg %s \n\tfromGender %s \n\tfromLoc %s \n\tfromRotY %s, \n\tfromVector %s"%(fromPeg,fromGender, fromLoc,fromRotY,fromVector)
    #print "toPeg %s \n\ttoGender %s \n\ttoLoc %s \n\ttoRotY %s, \n\ttoVector %s"%(toPeg,toGender, toLoc,toRotY,toVector)

    #1) duplicate the magicTrackBin
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
    newKBin = mc.duplicate("|library|magicTrackBin",rr=1)[0]
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
#    return
    #6
    # scale -- distance between points.  Gives us an idea of how much space to use
    # scale = sqrt((toLoc[0]-fromLoc[0])**2 + (toLoc[1]-fromLoc[1])**2 + (toLoc[2]-fromLoc[2])**2)
    # splineScale = scale / 3.0 # amount to scale the smoothness at the spline's end
    # #print "scale %f, spineScale %f"%(scale, splineScale)
    
    # offsets = {'Male':2.0, 'Female':1.0} # amount the src geometry object has an offset from the peg point
    # #print "offsets from %f, to %f"%(offsets[newFromGender], offsets[newToGender])
    # # make a spline with 4 points: 
    # # These are the core spline points, but I need to smooth the beginnings/ends out more
    # #    Pt0 = fromLoc + offset*fromVector 
    # #    Pt1 = Pt0 + splineScale*fromVector
    # #    Pt2 = Pt3 + splineScale*toVector
    # #    Pt3 = toLoc + offset*toVector
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
    profile = newKBin + "|magicTrackProfile"
    mc.move(ptF0[0],ptF0[1],ptF0[2],profile)
    mc.rotate(0,fromRotY,0,profile,ws=1,a=1)
    #print "TODO - ROTATE THE EXTRUSION PROFILE TO MATCH NEW_FROM_PEG"
    #extrude -ch true -rn false -po 1 -et 2 -ucp 0 -fpt 0 -upn 1 -rotation 0 -scale 1 -rsp 1 "magicTrackBin1|magicTrackProfile" "curve1" ;
    
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
    #polyUnite -ch 1 -mergeUVSets 1 magicTrackBin1|magicTrackProfile magicTrackBin1|magicTrackFemaleEndSrc1 extrudedSurface1;
    unitedGeom = mc.polyUnite(newExtrusionGeom, newToSrcObj, newFromSrcObj, ch=0, mergeUVSets=1, n='splineTrack1')[0]
    mergedGeom = mc.polyMergeVertex(unitedGeom, d=0.03,am=1,ch=0)
    mc.polySetToFaceNormal(unitedGeom)
    mc.polySoftEdge(unitedGeom,ch=0,angle=30)
    
    mc.sets(unitedGeom,e=1,fe='magicTrackShader1SG')
    mc.editDisplayLayerMembers( 'trackLayer', unitedGeom)
#    -e -forceElement trackLibraryMainPathsColored_trackLibraryMainPathsColored_revStraightTracks1_blinn1SG2;

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


# selects all intermediate objects in the scene
def selectIntermediateObjects():
    allObjs = mc.ls('*')
    iObjs = []
    for obj in allObjs:
        #print obj
        if mc.attributeQuery("intermediateObject", node=obj,exists=1):
            if mc.getAttr(obj+".intermediateObject"):
                iObjs.append(obj)
    mc.select(iObjs,r=1)
    return iObjs

    
# creates a python dict of the track locations in a scene (for easy export/transfer/repr)
def recordTracks():
    dataDict = {}
    tracks = mc.listRelatives('track',c=1)
    for track in tracks:
        #print track
        pos = mc.xform(track, query=True, translation=True, ws=True)        
        rot = mc.xform(track, query=True, rotation=True, ws=True)
        type = findTrackTypeKey(track)
        
        if type == None:
            print "%s has no type"%track
        # store the signPost values
        elif 'Switch' in type or 'Junction' in type:
            signPosts = findChildren(track,'signPost', fullPath=True)
            signPostValues = [mc.getAttr(sign+'.switch') for sign in signPosts]
            dataDict[track] = {'pos':pos,'rot':rot, 'type':type, 'signPostValues':signPostValues}
        
        # for kludge/magic tracks, store the names of the 'other' pegs, 
        # which were used to create them in the first place
        elif type == 'magicTrack':
            pegs = findChildren(track, 'Peg', fullPath=True)
            peg0OtherPeg = mc.getAttr(pegs[0]+".otherPeg")
            peg1OtherPeg = mc.getAttr(pegs[1]+".otherPeg")
            track = track.replace('kludge','magic')
            dataDict[track] = {'pos':pos,'rot':rot, 'type':type, 'peg0OtherPeg':peg0OtherPeg, 'peg1OtherPeg':peg1OtherPeg}
        else:
            dataDict[track] = {'pos':pos,'rot':rot, 'type':type}
    return dataDict

def findTrackTypeKey(trackName):
    
    searchName = "|"+trackName.rstrip('0123456789')
    #print 'searching for %s'%searchName
    for key, value in trackLibrary.iteritems():
        #print value
        if searchName in value:
            return key
    return None
    
def recreateTracks(trackDict):
    importTrainLibrary()
    magicTracks = {} # create these last
    for track,info in trackDict.iteritems():
        #print track
        #print info
        type = info['type']
        if not type:
            continue
        # store the magic tracks for processing last
        if 'magic' in type:
            #print "peg0OtherPeg %s  peg1OtherPeg %s"%(info['peg0OtherPeg'], info['peg1OtherPeg'])
            magicTracks[track] = info
            continue
            
        newTrack = addTrack(type)
        newTrack = mc.rename(newTrack,track)
        pos = info['pos']
        rot = info['rot']
        mc.move(pos[0],pos[1],pos[2],newTrack)
        mc.rotate(rot[0],rot[1],rot[2],newTrack)
        if 'Switch' in type or 'Junction' in type:
            #print "restoring switch values"
            #restore the signPostValues
            signPostValues = info['signPostValues']
            signPosts = findChildren(track,'signPost', fullPath=True)
            for sign, value in zip(signPosts, signPostValues):
                #print "sign %s, value %d"%(sign,value)
                mc.setAttr(sign+'.switch',value)

    # process the magic tracks -- use the names of the 'other' pegs to
    # recreate the magic tracks
    for magicTrack, info in magicTracks.iteritems():
        mc.select(info['peg0OtherPeg'], info['peg1OtherPeg'] ,r=1)
        track = buildMagicTrack(fromPeg=info['peg0OtherPeg'],toPeg=info['peg1OtherPeg'])
        mc.rename(track,magicTrack)
        
    pass

    
# Stores the state of all of the trains to the allTrainsGroup node
# For use in restoring the trains to the same state
#
# Store a dict of information to a string attr on the allTrainsGroup node
#     axle current curve
#     axle current param curve
#     train speed
#     current train switchData structure
#
def saveTrainState():
    #1) get list of trains
    #2) get info from each train
    #3) store dict of info to the allTrainsGroup
    
    if not mc.objExists('allTrainsGroup'):
        return
    
    trainState = {}
    trains = mc.listRelatives('allTrainsGroup',c=1,type='transform')
    print trains
    
    for train in trains:
        trainState[train] = getTrainInfo(train)
    
    if not mc.attributeQuery('trainState', node='allTrainsGroup', exists=1):
        mc.addAttr("|allTrainsGroup", ln='trainState', dt="string")
        mc.setAttr("|allTrainsGroup.trainState",e=1,keyable=True)
    mc.setAttr("|allTrainsGroup.trainState", str(trainState), type="string")
    print("Saved train state to attr on allTrainsGroup")
    #pprint.pprint(trainState)
    pass
    
def getTrainInfo(train):
    trainInfo = {}    
    print "gather state of %s" % train
    axles = mc.listRelatives(train, c=1, type='transform',f=1)
    print "axles %s"%axles
    for axle in axles:
        if not 'Axle' in axle:
            continue
        axleInfo = getAxleInfo(axle)
        trainInfo[axle] = axleInfo
    trainSpeed = mc.getAttr(train+'.speed')
    trainSwitchData = mc.getAttr(train+'.switchData')
    trainInfo['speed'] = trainSpeed
    trainInfo['switchData'] = trainSwitchData
    return trainInfo
    
def getAxleInfo(axle):
    currTrackParamVal = mc.getAttr(axle+'.currTrackParamVal')
    facingZeroToOneDir = mc.getAttr(axle+'.facingZeroToOneDir')
    isFirstAxle = mc.getAttr(axle+'.isFirstAxle')
    isLastAxle = mc.getAttr(axle+'.isLastAxle')
    currTrackCurve = mc.getAttr(axle+'.currTrackCurve')
    info = {
        'currTrackParamVal':currTrackParamVal,
        'facingZeroToOneDir':facingZeroToOneDir,
        'isFirstAxle':isFirstAxle,
        'isLastAxle':isLastAxle,
        'currTrackCurve':currTrackCurve,
    }
    return info
    
# restores trains to the saved train state
def restoreTrainState():
    #1) get list of trains
    #2) get info from each train
    #3) store dict of info to the allTrainsGroup
    
    print("Restoring train state from attr on allTrainsGroup")
    
    if not mc.objExists('allTrainsGroup'):
        print("\tNo trains are loaded.")
        return

    if not mc.attributeQuery('trainState', node='allTrainsGroup', exists=1):
        print("\tTrain state not found")
        return

    trainStateStr = mc.getAttr('allTrainsGroup.trainState')
    trainState = ast.literal_eval(trainStateStr)
    trains = mc.listRelatives('allTrainsGroup',c=1,type='transform')
    for train in trains:
        if train in trainState.keys():    
            trainInfo = trainState[train]
            setTrainInfo(train, trainInfo)
        moveTrainForward(train, tempSpeed=0)
    
def setTrainInfo(train, info):
    axles = mc.listRelatives(train, c=1, type='transform',f=1)
    for axle in axles:
        if not 'Axle' in axle:
            continue
        axleInfo = info[axle]
        setAxleInfo(axle, axleInfo)
    mc.setAttr(train+'.speed', info['speed'])
    if info['switchData']:
        mc.setAttr(train+'.switchData', info['switchData'], type="string")
    
def setAxleInfo(axle, info):
    mc.setAttr(axle+'.currTrackParamVal', info["currTrackParamVal"])
    mc.setAttr(axle+'.facingZeroToOneDir', info["facingZeroToOneDir"])
    mc.setAttr(axle+'.isFirstAxle', info["isFirstAxle"])
    mc.setAttr(axle+'.isLastAxle', info["isLastAxle"])
    mc.setAttr(axle+'.currTrackCurve', info["currTrackCurve"], type="string")
    
    
    
