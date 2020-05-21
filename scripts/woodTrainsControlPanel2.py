from maya.app.general import mayaMixin
import os
import sys
from PySide2 import QtGui, QtWidgets
import maya.cmds as mc
import logging
import track

reload(track)
# mc.file(f=1,new=1)
# mc.polySphere()

"""
Installation instructions are inside track.py

#EXAMPLE
import woodTrainsControlPanel2 as wc
reload(wc)
wc.main()
"""

#wtcw = None

def main():
#    app = QtWidgets.QApplication(sys.argv)
    #ex = Example() 
    
    # a single train control
    #sb = Sandbox("classicFreightTrainGroup1") 
    
    wtcw = WoodenTrainControlWindow() 
    #    wtcw.deleteTrainController(1)
#    sys.exit(app.exec_())


#iconPath = os.getenv("MAYA_APP_DIR") + "/tkTestIcons/"
#print iconPath
#testicon = iconPath + "testIcon100.png"
#print testicon
class IconPushButton(QtWidgets.QPushButton):
    labeltext = 'Button'
    blindData = None
    
    iconimage=None
    align='center'
    labelbackgroundcolor='#00000077'
    
    def makeNewPixmap(self, labeltext=None, iconimage=None, align=None, labelbackgroundcolor=None):
        
        if not labeltext:
            labeltext=self.labeltext
        else:
            self.labeltext=labeltext
            
        if not iconimage:
            iconimage=self.iconimage
        else:
            self.iconimage=iconimage
        
        if not align:
            align=self.align
        else:
            self.align=align
            
        if not labelbackgroundcolor:
            labelbackgroundcolor = self.labelbackgroundcolor
        else:
            self.labelbackgroundcolor=labelbackgroundcolor
            
        #pixmap = toolCatalog.createShelfButtonPixmap( {'labeltext':labeltext, 'iconimage':iconimage, 'labeltextalignh':align, 'labelbackgroundcolor':labelbackgroundcolor} )
        
        # correct: - use catalog code:
        # pixmap = catalog.createShelfButtonPixmap( {'labeltext':labeltext, 'iconimage':iconimage, 'labeltextalignh':align, 'labelbackgroundcolor':labelbackgroundcolor} )
        
        # Extracted icon search logic:
        pixmap = QtGui.QPixmap()
        if os.path.isfile(self.iconimage):
            pixmap = QtGui.QPixmap(self.iconimage)
        else:
            # Do some searching for the icon file:
            filename = self.iconimage
            searchpaths = os.environ.get('XBMLANGPATH','').split(os.pathsep)
            for p in searchpaths:
                p = p.replace('%B','')  # Remove the trailing %B found in Linux paths
                fullpath = os.path.join(p, filename)
                if os.path.isfile(fullpath):
                    pixmap = QtGui.QPixmap(fullpath)
                    break
        
        icon = QtGui.QIcon(pixmap)
        iconSize = mayaMixin.QSize(pixmap.width(), pixmap.height())
        self.setIconSize(iconSize)
        self.setIcon(icon)    
        return pixmap
        
    def __init__(self, labeltext='',iconimage='', align='center', labelbackgroundcolor='#00000077', trackPiece=None, bumpDir=None, handled=False):
        super(IconPushButton,self).__init__()
        self.labeltext = labeltext
        
        # NOTE: adds a dependency on the toolCatalog
        pixmap = self.makeNewPixmap(labeltext=labeltext, iconimage=iconimage, align=align, labelbackgroundcolor=labelbackgroundcolor)
    
        #self.setMinimumWidth(40)
        #self.setMinimumHeight(40)
        #self.setMaximumWidth(64)
        #self.setMaximumHeight(64)
        self.setMaximumWidth(50)
        self.setMaximumHeight(50)
        self.setContentsMargins(0,0,0,0)
        
        # make a connection
        if handled:
            return

        if not trackPiece == None:
            #print "connect to addTrackPieceToSelected %s"%trackPiece
            self.blindData = trackPiece
            self.clicked.connect(self.handleAddTrackClick)
            pass
        elif not bumpDir == None:
            if 'down' in bumpDir.lower():
                self.clicked.connect(track.bumpDown)
            elif 'up' in bumpDir.lower():
                self.clicked.connect(track.bumpUp)
            elif 'left' in bumpDir.lower():
                self.clicked.connect(track.bumpLeft)
            elif 'right' in bumpDir.lower():
                self.clicked.connect(track.bumpRight)
            elif 'counterclock' in bumpDir.lower():
                self.clicked.connect(track.bumpCounterClockwise)
            elif 'clock' in bumpDir.lower():
                self.clicked.connect(track.bumpClockwise)
        else:
            print "No connection for button %s" % labeltext
            
        pass
        
    def handleAddTrackClick(self):
        sender = self.sender()
        #print "inside handleAddTrackClick %s"%sender.blindData
        trackPiece = self.sender().blindData
        track.addTrackToSelected(trackPiece)
        pass
            
        #self.clicked.connect(self.clickHandler)
    
    #def clickHandler(self):
    #    print "IconPushButton clicked - labeltext:%s"%self.labeltext
        
class ButtonHBox(QtWidgets.QHBoxLayout):
    def __init__(self):
        super(ButtonHBox,self).__init__()
        self.setSpacing(1)
        
# TODO - Rename trains (dialog?  renames the train node and UI label
#
# TODO - add other tabs and global controls
#    - global control - train speed multiplier - speed/slow all trains together
#    - should reset a train be local or global?
#
class WoodenTrainControlWindow(mayaMixin.MayaQWidgetDockableMixin, QtWidgets.QTabWidget):
    controllerLayout=None
    playButton = None
    #directionToggleButton = None
    toggleDirectionButton = None
    
    def __init__(self, trainName=None):
        super(WoodenTrainControlWindow, self).__init__()
        width=325
        #height=830
        height = 400
        self.setDockableParameters(dockable=True, floating=True, area="top", width=width, height=height)
        self.setWindowTitle("Wooden Trains Control")
        
        self.trainName = trainName
        self.initUI(width=width, height=height)

        
    def initUI(self, width=300, height=200):
        tab = self
        tab.setMinimumHeight(height)
        tab.setMinimumWidth(width)
        
        trackSetupPage = self.createTrackSetupPage()
        #trainSetupPage = self.createTrainSetupPage()
        scrollArea = self.createTrainControlPage()
        #testPage = self.createTestPage()
            
        tab.addTab(trackSetupPage, "Track Setup")
        #tab.addTab(trainSetupPage, "Train Setup")
        tab.addTab(scrollArea, "Train Control")
        #tab.addTab(testPage, "Test Page")
        tab.show()
    
        
    def createTrainSetupPage(self):
        trainSetupPage = QtWidgets.QWidget() #Train Setup
        trainSetupGrid = QtWidgets.QGridLayout()
        trainSetupVBox = QtWidgets.QVBoxLayout()
        trainSetupPage.setLayout(trainSetupVBox)
        return trainSetupPage
                
    def createTrainControlPage(self):
        pageContainer = QtWidgets.QWidget() #page2
        #pageContainer.setWidgetResizable(True)
        pageLayout = QtWidgets.QVBoxLayout(pageContainer)
        self.controllerLayout = pageLayout
        
        #Create the play/stop control buttons outside the VBox scroll list
        playTrainButton = IconPushButton(labeltext='play', iconimage='trackRender1.47.png', handled=True)
        playTrainButton.clicked.connect(self.playButtonHandler)
        playTrainButton.setCheckable(1)
        self.playButton = playTrainButton
        
        addTrainButton = IconPushButton(labeltext='train', iconimage='trackRender1.46.png', handled=True)
        addTrainButton.clicked.connect(self.trainClickedHandler)

        resetTrainButton = IconPushButton(labeltext='reset', iconimage='trackRender1.49.png', handled=True)
        resetTrainButton.clicked.connect(track.resetTrain)

        refreshTrainListButton = IconPushButton(labeltext='refresh', iconimage='uiRefresh48.png', handled=True)
        refreshTrainListButton.clicked.connect(self.loadTrainControllers)

        saveTrainStateButton = IconPushButton(labeltext='save', iconimage='saveTrainState.png', handled=True)
        saveTrainStateButton.clicked.connect(track.saveTrainState)

        restoreTrainStateButton = IconPushButton(labeltext='restore', iconimage='restoreTrainState.png', handled=True)
        restoreTrainStateButton.clicked.connect(track.restoreTrainState)
        
        #clearTrainListButton = IconPushButton(labeltext='clear', iconimage='trackRender1.49.png', handled=True)
        #clearTrainListButton.clicked.connect(self.clearTrainControllers)

        
        Line1HBox = ButtonHBox()
        Line1HBox.addWidget(playTrainButton)
        Line1HBox.addWidget(addTrainButton)
        Line1HBox.addWidget(resetTrainButton)
        Line1HBox.addWidget(refreshTrainListButton)
        Line1HBox.addWidget(saveTrainStateButton)
        Line1HBox.addWidget(restoreTrainStateButton)
        #Line1HBox.addWidget(clearTrainListButton)
        Line1HBox.addStretch()
        pageLayout.addLayout(Line1HBox)
        
        
        # Create the scroll list of train controls
        scrollArea = QtWidgets.QScrollArea() 
        scrollArea.setWidgetResizable(True)
        
        pageLayout.addWidget(scrollArea)
        
        scrollContainer = QtWidgets.QWidget()
        scrollArea.setWidget(scrollContainer)
        scrollLayout = QtWidgets.QVBoxLayout(scrollContainer)
        self.controllerLayout = scrollLayout
        scrollLayout.addStretch()

        self.loadTrainControllers()
        
        #return scrollArea
        return pageContainer

    def loadTrainControllers(self):    
        self.clearTrainControllers()
        if mc.objExists("allTrainsGroup"):
            trains = mc.listRelatives('allTrainsGroup', c=1)
            if trains:
                for train in trains:
                    self.addTrainController(train)
        
    def clearTrainControllers(self):
        numWidgets = self.controllerLayout.count()
        
        # close existing train contoller layouts
        for i in range(numWidgets-1):
            w = self.controllerLayout.itemAt(i).widget()
            if w:
                w.close()
        
        # Remove existing train controllers        
        for i in range(numWidgets-1):
            toTrash = self.controllerLayout.takeAt(0)
            self.controllerLayout.removeItem(toTrash)
        
    
    def createTrackSetupPage(self):
        scrollArea = QtWidgets.QScrollArea() #page2
        scrollArea.setWidgetResizable(True)
        
        trackSetupPage = QtWidgets.QWidget() #Track Setup
        #scrollContainer = QtWidgets.QWidget()
        scrollArea.setWidget(trackSetupPage)
    
        trackSetupVBox = QtWidgets.QVBoxLayout()
        trackSetupPage.setLayout(trackSetupVBox)

        # group = QtWidgets.QGroupBox()
        # trackSetupVBox.addWidget(group)
        
        # trackSetupGrid = QtWidgets.QGridLayout()
        # group.setLayout(trackSetupGrid)
        
        #Curve Tracks
        miniLeftButton = IconPushButton(labeltext='minL', iconimage='trackRender1.17.png', trackPiece='shortCurveLeft')
        miniRightButton = IconPushButton(labeltext='minR', iconimage='trackRender1.16.png', trackPiece='shortCurveRight')
        leftButton = IconPushButton(labeltext='left', iconimage='trackRender1.15.png', trackPiece='mediumCurveLeft')
        rightButton = IconPushButton(labeltext='right', iconimage='trackRender1.14.png', trackPiece='mediumCurveRight')
        
        #Straight Tracks
        miniStraightButton = IconPushButton(labeltext='Mini', iconimage='trackRender1.21.png', trackPiece='miniStraight')
        shortStraightButton = IconPushButton(labeltext='Short', iconimage='trackRender1.20.png', trackPiece='shortStraight')
        mediumStraightButton = IconPushButton(labeltext='Med', iconimage='trackRender1.19.png', trackPiece='mediumStraight')
        longStraightButton = IconPushButton(labeltext='Long', iconimage='trackRender1.18.png', trackPiece='longStraight')
        
        #Switch Tracks
        rightSwitch1Button = IconPushButton(labeltext='rtSwch', iconimage='trackRender1.23.png', trackPiece='mediumCurveRightSwitch')
        leftSwitch1Button = IconPushButton(labeltext='lfSwch', iconimage='trackRender1.24.png', trackPiece='mediumCurveLeftSwitch')
        rightSwitch2Button = IconPushButton(labeltext='rtSw2', iconimage='trackRender1.26.png', trackPiece='mediumCurveRightSwitch2')
        leftSwitch2Button = IconPushButton(labeltext='lfSw2', iconimage='trackRender1.25.png', trackPiece='mediumCurveLeftSwitch2')
        curveSwitchButton = IconPushButton(labeltext='crvSw', iconimage='trackRender1.27.png', trackPiece='mediumCurveSwitch')
        tJunctionButton = IconPushButton(labeltext='tJunc', iconimage='trackRender1.35.png', trackPiece='TJunction')
        
        #Bridge Tracks
        upTrackButton = IconPushButton(labeltext='up', iconimage='trackRender1.09.png', trackPiece='longAscendingStraight')
        downTrackButton = IconPushButton(labeltext='down', iconimage='trackRender1.10.png', trackPiece='longDescendingStraight')
        supportTrackButton = IconPushButton(labeltext='support', iconimage='trackRender1.11.png', trackPiece='bridgeSupport1')
        thinSupportButton = IconPushButton(labeltext='thin', iconimage='trackRender1.13.png', trackPiece='bridgeSupportThinStacking')
        trackSupportButton = IconPushButton(labeltext='track', iconimage='trackRender1.12.png', trackPiece='bridgeSupportStacking')
        
        #Reversing Tracks
        miniMaleReverseButton = IconPushButton(labeltext='Mini', iconimage='trackRender1.05.png', trackPiece='miniReverseMaleStraight')
        shortMaleReverseButton = IconPushButton(labeltext='Short', iconimage='trackRender1.06.png', trackPiece='shortReverseMaleStraight')
        mediumMaleReverseButton = IconPushButton(labeltext='Med', iconimage='trackRender1.07.png', trackPiece='medReverseMaleStraight')
        longMaleReverseButton = IconPushButton(labeltext='Long', iconimage='trackRender1.08.png', trackPiece='longReverseMaleStraight')
        
        miniFemaleReverseButton = IconPushButton(labeltext='Mini', iconimage='trackRender1.01.png', trackPiece='miniReverseFemaleStraight')
        shortFemaleReverseButton = IconPushButton(labeltext='Short', iconimage='trackRender1.02.png', trackPiece='shortReverseFemaleStraight')
        mediumFemaleReverseButton = IconPushButton(labeltext='Med', iconimage='trackRender1.03.png', trackPiece='medReverseFemaleStraight')
        longFemaleReverseButton = IconPushButton(labeltext='Long', iconimage='trackRender1.04.png', trackPiece='longReverseFemaleStraight')
        
        # Special Tracks
        crossTrackButton = IconPushButton(labeltext='Cross', iconimage='trackRender1.31.png', trackPiece='crossTrack')
        threeJunctionButton = IconPushButton(labeltext='3Junc', iconimage='trackRender1.30.png', trackPiece='curveThreeSwitch')
        
        maleStopButton = IconPushButton(labeltext='mRev', iconimage='trackRender1.29.png', trackPiece='maleStopper')
        femaleStopButton = IconPushButton(labeltext='fRev', iconimage='trackRender1.28.png', trackPiece='femaleStopper')
        
        femaleCarpetButton = IconPushButton(labeltext='fCarp', iconimage='trackRender1.33.png', trackPiece='femaleCarpet')
        maleCarpetButton = IconPushButton(labeltext='mCarp', iconimage='trackRender1.32.png', trackPiece='maleCarpet')
        magicTrackButton = IconPushButton(labeltext='Magic', iconimage='trackRender1.34.png', handled=True) 
        magicTrackButton.clicked.connect(track.buildMagicTrack)
    

        #Track Control Buttons

            #link the track pieces
        linkButton = IconPushButton(labeltext='Link', iconimage='iconLinkTrack.png', handled=True) 
        linkButton.clicked.connect(track.analyzeTrack3)
        
        directionToggleButton = IconPushButton(labeltext='dirTgl', iconimage='trackRender1.50.png', handled=True)
        directionToggleButton.clicked.connect(self.toggleTrackSetupDirection)
        self.toggleDirectionButton = directionToggleButton
        
        selectPegButton = IconPushButton(labeltext='selPeg', iconimage='trackRender1.43.png', handled=True)
        selectPegButton.clicked.connect(track.selectActivePeg)

        cyclePegButton = IconPushButton(labeltext='cyclePeg', iconimage='trackRender1.52.png', handled=True)
        cyclePegButton.clicked.connect(track.selectPegCycle)

        woodTextureButton = IconPushButton(labeltext='woodTex', iconimage='trackRender1.53.png', handled=True)
        woodTextureButton.clicked.connect(track.switchTracksToWoodShader)

        rebuildTrackCurveButton = IconPushButton(labeltext='fixCurve', iconimage='trackRender1.54.png', handled=True)
        rebuildTrackCurveButton.clicked.connect(track.rebuildCarpetCurve)

        cycleSignPostValueButton = IconPushButton(labeltext='Switch', iconimage='trackRender1.55.png', handled=True)
        cycleSignPostValueButton.clicked.connect(track.cycleSignPostValue)
        

        
        # Pixel Track Budging
        BumpTrackUpButton = IconPushButton(labeltext='mvUp', iconimage='trackRender1.41.png', bumpDir="up")
        BumpTrackDownButton = IconPushButton(labeltext='mvDn', iconimage='trackRender1.40.png', bumpDir="down")
        BumpTrackLeftButton = IconPushButton(labeltext='mvLeft', iconimage='trackRender1.39.png', bumpDir="left")
        BumpTrackRightButton = IconPushButton(labeltext='mvRigt', iconimage='trackRender1.38.png', bumpDir="right")
        
        BumpTrackClockButton = IconPushButton(labeltext='rotClk', iconimage='trackRender1.44.png', bumpDir="clock")
        BumpTrackCounterClockButton = IconPushButton(labeltext='rotCClk', iconimage='trackRender1.45.png', bumpDir="counterclock")
        
        moveTrackUpButton = IconPushButton(labeltext='+Up', iconimage='trackRender1.37.png', handled=True)
        moveTrackUpButton.clicked.connect(moveTrackVertUp)
        
        moveTrackDownButton = IconPushButton(labeltext='-Down', iconimage='trackRender1.36.png', handled=True)
        moveTrackDownButton.clicked.connect(moveTrackVertDown)
        
         # align track pieces
        alignTrackButton = IconPushButton(labeltext='align', iconimage='iconAlignTrack.png', handled=True)
        alignTrackButton.clicked.connect(track.attachTrack)

        
        label = QtWidgets.QLabel("<FONT SIZE = 10><b>Track Pieces</b></font>")            
        trackSetupVBox.addWidget(label)
        
        Line1HBox = ButtonHBox()
        Line1HBox.setContentsMargins(0,0,0,0)
        Line1HBox.setSpacing(1)
        
        Line1HBox.addWidget(miniLeftButton)
        Line1HBox.addWidget(miniRightButton)
        Line1HBox.addWidget(leftButton)
        Line1HBox.addWidget(rightButton)
        Line1HBox.addStretch()
        trackSetupVBox.addLayout(Line1HBox)
        
        Line2HBox = ButtonHBox()
        Line2HBox.addWidget(miniStraightButton)
        Line2HBox.addWidget(shortStraightButton)
        Line2HBox.addWidget(mediumStraightButton)
        Line2HBox.addWidget(longStraightButton)
        Line2HBox.addStretch()
        trackSetupVBox.addLayout(Line2HBox)

        # trackSetupVBox.addWidget(miniStraightButton)
        # trackSetupVBox.addWidget(shortStraightButton)
        # trackSetupVBox.addWidget(mediumStraightButton)
        # trackSetupVBox.addWidget(longStraightButton)

        Line3HBox = ButtonHBox()
        Line3HBox.addWidget(rightSwitch1Button)
        Line3HBox.addWidget(leftSwitch1Button)
        Line3HBox.addWidget(curveSwitchButton)
        Line3HBox.addWidget(rightSwitch2Button)
        Line3HBox.addWidget(leftSwitch2Button)
        Line3HBox.addStretch()
        trackSetupVBox.addLayout(Line3HBox)

        Line4HBox = ButtonHBox()
        Line4HBox.addWidget(crossTrackButton)
        Line4HBox.addWidget(threeJunctionButton)
        Line4HBox.addWidget(tJunctionButton)
        Line4HBox.addWidget(maleStopButton)
        Line4HBox.addWidget(femaleStopButton)
        Line4HBox.addStretch()
        trackSetupVBox.addLayout(Line4HBox)

        Line5HBox = ButtonHBox()
        Line5HBox.addWidget(femaleCarpetButton)
        Line5HBox.addWidget(maleCarpetButton)
        Line5HBox.addWidget(magicTrackButton)
        Line5HBox.addStretch()
        trackSetupVBox.addLayout(Line5HBox)

        label = QtWidgets.QLabel("<FONT SIZE = 5><b>Bridge Tracks</b></font>")            
        trackSetupVBox.addWidget(label)
        
        Line6HBox = ButtonHBox()        
        Line6HBox.addWidget(upTrackButton)
        Line6HBox.addWidget(downTrackButton)
        Line6HBox.addWidget(supportTrackButton)
        Line6HBox.addWidget(thinSupportButton)
        Line6HBox.addWidget(trackSupportButton)
        Line6HBox.addStretch()
        trackSetupVBox.addLayout(Line6HBox)
        
        label = QtWidgets.QLabel("<FONT SIZE = 5><b>Reverse Tracks</b></font>")            
        trackSetupVBox.addWidget(label)
        
        Line7HBox = ButtonHBox()
        label = QtWidgets.QLabel("<FONT SIZE = 2><b>Male</b></font>")            
        label.setMinimumWidth(50)
        Line7HBox.addWidget(label)
        Line7HBox.addWidget(miniMaleReverseButton)
        Line7HBox.addWidget(shortMaleReverseButton)
        Line7HBox.addWidget(mediumMaleReverseButton)
        Line7HBox.addWidget(longMaleReverseButton)
        Line7HBox.addStretch()
        trackSetupVBox.addLayout(Line7HBox)
        
        Line8HBox = ButtonHBox()
        label = QtWidgets.QLabel("<FONT SIZE = 2><b>Female</b></font>")            
        label.setMinimumWidth(50)
        Line8HBox.addWidget(label)
        Line8HBox.addWidget(miniFemaleReverseButton)
        Line8HBox.addWidget(shortFemaleReverseButton)
        Line8HBox.addWidget(mediumFemaleReverseButton)
        Line8HBox.addWidget(longFemaleReverseButton)
        Line8HBox.addStretch()
        trackSetupVBox.addLayout(Line8HBox)

        label = QtWidgets.QLabel("<FONT SIZE = 10><b>Setup Utilities</b></font>")            
        trackSetupVBox.addWidget(label)
        
        Line9HBox = ButtonHBox()
        #Line9HBox.addWidget(initializeButton)    # not critical
        #Line9HBox.addWidget(testButton)            # not critical
        Line9HBox.addWidget(linkButton)
        Line9HBox.addWidget(alignTrackButton)
        Line9HBox.addWidget(directionToggleButton)
        Line9HBox.addWidget(selectPegButton)
        Line9HBox.addWidget(cyclePegButton)
        Line9HBox.addStretch()
        trackSetupVBox.addLayout(Line9HBox)

        Line9aHBox = ButtonHBox()
        Line9aHBox.addWidget(woodTextureButton)
        Line9aHBox.addWidget(rebuildTrackCurveButton)
        Line9aHBox.addWidget(cycleSignPostValueButton)
        Line9aHBox.addStretch()
        trackSetupVBox.addLayout(Line9aHBox)

        label = QtWidgets.QLabel("<FONT SIZE = 3><b>Pixel Bump Tracks</b></font>")            
        trackSetupVBox.addWidget(label)

        Line10HBox = ButtonHBox()            
        Line10HBox.addWidget(BumpTrackUpButton)
        Line10HBox.addWidget(BumpTrackDownButton)
        Line10HBox.addWidget(BumpTrackLeftButton)
        Line10HBox.addWidget(BumpTrackRightButton)
        
        Line10HBox.addStretch()
        trackSetupVBox.addLayout(Line10HBox)
        
        Line11HBox = ButtonHBox()        
        Line11HBox.addWidget(BumpTrackClockButton)
        Line11HBox.addWidget(BumpTrackCounterClockButton)
        Line11HBox.addWidget(moveTrackUpButton)
        Line11HBox.addWidget(moveTrackDownButton)
        Line11HBox.addStretch()
        trackSetupVBox.addLayout(Line11HBox)

        # label = QtWidgets.QLabel("Label")            
        # trackSetupVBox.addWidget(label)
        trackSetupVBox.addStretch()            
        #return trackSetupPage
        return scrollArea
        
    def createTestPage(self):
        testPage = QtWidgets.QWidget() #Track Setup
        testPageVBox = QtWidgets.QVBoxLayout()
        testPage.setLayout(testPageVBox)

        # import the track library file
        initializeButton = IconPushButton(labeltext='Init', iconimage='driveFast.png') 
            # create a test track
        testButton = IconPushButton(labeltext='TEST', iconimage='driveFast.png')
    
        Line1HBox = ButtonHBox()
        Line1HBox.addWidget(initializeButton)    # not critical
        Line1HBox.addWidget(testButton)            # not critical
        Line1HBox.addStretch()
        testPageVBox.addLayout(Line1HBox)
        return testPage
    
    #    Given a train name, find the index of the TrainController UI object
    #     (used for deletion)
    def findControllerIndex(self,trainName):
        for i in range(self.controllerLayout.count()):
            item = self.controllerLayout.itemAt(i)
            widget = item.widget()
            if hasattr(widget, 'trainName'):
                if trainName == widget.trainName:
                    return i
        return None

    # Deletes the train controller UI in the list of controllers
    #
    def deleteTrainController(self,index):
        toDelete = self.controllerLayout.takeAt(index)
        toDelete.widget().deleteLater()    

    def addTrainController(self,trainName):
        tc = TrainControllerH(self, trainName=trainName)
        numWidgets = self.controllerLayout.count()
        #self.controllerLayout.insertWidget(numWidgets-1,tc,0,1)
        self.controllerLayout.insertWidget(numWidgets-1,tc,0) # can add an Alignment
    
    def trainClickedHandler(self):
        #print "inside trainClickedHandler"
        newTrain = track.addTrain()
        #print newTrain
        self.addTrainController(newTrain)
    
    def playButtonHandler(self):
        # Handle the playback button
        #print "inside playButtonHandler"
        mc.evaluationManager(mode="off")
        state = mc.play(q=1,state=1)
        
        # Adjust the icon
        if not state:
            self.playButton.makeNewPixmap(labeltext="stop", iconimage='trackRender1.48.png')
        else:
            self.playButton.makeNewPixmap(labeltext="play", iconimage='trackRender1.47.png')
        
        mc.play(forward=1, state=not state)
        pass
        
    def toggleTrackSetupDirection(self):        
        # Change the track laying direction
        # change the icon/pixmap on the pushButton

        #,command="import maya.cmds as m\r\nnewVal = not m.getAttr(\"library.femaleToMaleDirection\")\rm.setAttr(\"library.femaleToMaleDirection\",newVal)\rif newVal:\r\tm.shelfButton(\""+dirTGL+"\", e=1,i=\"woodTrainsPegMale.xpm\")\relse:\r\tm.shelfButton(\""+dirTGL+"\", e=1,i=\"woodTrainsPegFemale.xpm\")"

        #print "Toggle Direction"
        # let the track library alter Maya
        newVal = track.toggleTrackSetupDirection()
        
        #newVal = mc.getAttr("library.femaleToMaleDirection")
        #newVal = mc.getAttr("library.zeroToOneDirection")
        if newVal:    
            self.toggleDirectionButton.makeNewPixmap(labeltext="dirTgl", iconimage='trackRender1.50.png')
            #m.shelfButton(\""+dirTGL+"\", e=1,i=\"woodTrainsPegMale.xpm\")
            pass
        else:
            self.toggleDirectionButton.makeNewPixmap(labeltext="dirTgl", iconimage='trackRender1.51.png')
            #m.shelfButton(\""+dirTGL+"\", e=1,i=\"woodTrainsPegFemale.xpm\")
            pass
        pass


def moveTrackVertDown():
    print "inside moveTrackVertDown"
    track.movePieceVertically(dir=-1)
def moveTrackVertUp():
    print "inside moveTrackVertUp"
    track.movePieceVertically(dir=1)
    
        
#
# Creates a dockable Maya window with a LCD readout and a slider
# Will control the speed of the default train when the slider is moved
#
# Make the trainName in a larger font
#
# The global UI will need a playback start/stop button
# And a train reset button
#    Perhaps add to the reset function an ability to reset to the 
#    first track piece (that isn't a switch)...
#
class TrainControllerH(QtWidgets.QGroupBox):
    trainName = None
    speedDial = None
    WoodenTrainControlWindow = None
 
    def __init__(self, wtcw, trainName=None):
        super(TrainControllerH, self).__init__()
        
        width=0#310
        height=0#130
        #self.setDockableParameters(dockable=True, floating=True, area="top", width=width, height=height)
        
        self.WoodenTrainControlWindow = wtcw
        self.trainName = trainName
        self.initUI(width=width, height=height)
        
    def initUI(self, width=0, height=0): # 300,150

        #hbox=QtWidgets.QHBoxLayout()
        #vLabelBox=QtWidgets.QVBoxLayout()
        #vButtonBox=QtWidgets.QVBoxLayout()
        
        self.setMinimumWidth(275)
        self.setMinimumHeight(105)
        
        label = QtWidgets.QLabel(self)
        label.move(90,5)
        
        dial = QtWidgets.QDial(self)
        #dial.move(-5,-10)
        dial.move(-5,4)
        
        lcd = QtWidgets.QLCDNumber(self)
        lcd.move(90,50)
        
        btnStop = QtWidgets.QPushButton(self)
        btnStop.move(90,25)
        btnSelect = QtWidgets.QPushButton(self)
        btnSelect.move(170,25)
        btnReset = QtWidgets.QPushButton(self)
        btnReset.move(170,50)
        btnResetRev = QtWidgets.QPushButton(self)
        btnResetRev.move(254,50)
        btnDelete = QtWidgets.QPushButton(self)
        btnDelete.move(170,75)
        
        #self.resize(300,130)
        #add buttons to vertical section
        # vButtonBox.addWidget(btnStop)
        # vButtonBox.addWidget(btnSelect)
        # vButtonBox.addWidget(btnDelete)
        
        #vLabelBox.addWidget(label)
        #vLabelBox.addWidget(lcd)
        
        #hbox = QtWidgets.QhboxLayout()
        #hbox.addWidget(dial)
        #hbox.addWidget(label)
        #hbox.addWidget(lcd)
        #vButtonBox.addWidget(btnStop)
        #vButtonBox.addWidget(btnSelect)
        #vButtonBox.addWidget(btnDelete)
        
        #self.show()
        
        
        # hbox.addLayout(vLabelBox) # add vertical layout
        # hbox.addLayout(vButtonBox) # add vertical layout
        
        
        trainCameraBtn = QtWidgets.QPushButton(self)
        trainCameraBtn.move(0,0)
        
        engineCameraBtn = QtWidgets.QPushButton(self)
        engineCameraBtn.move(20,0)
        
        tankerCameraBtn = QtWidgets.QPushButton(self)
        tankerCameraBtn.move(40,0)

        perspCameraBtn = QtWidgets.QPushButton(self)
        perspCameraBtn.move(60,0)

        trainCameraBtn.setMinimumWidth(20)
        trainCameraBtn.setText("C")
        trainCameraBtn.setStyleSheet("background-color: rgb(128,95,95); color:rgb(255,255,255)")
        
        engineCameraBtn.setMinimumWidth(20)
        engineCameraBtn.setText("E")
        engineCameraBtn.setStyleSheet("background-color: rgb(95,95,128); color:rgb(255,255,255)")
        
        tankerCameraBtn.setMinimumWidth(20)
        tankerCameraBtn.setText("T")
        tankerCameraBtn.setStyleSheet("background-color: rgb(95,128,95); color:rgb(255,255,255)")
        
        perspCameraBtn.setMinimumWidth(20)
        perspCameraBtn.setText("P")
        perspCameraBtn.setStyleSheet("background-color: rgb(128,128,128); color:rgb(255,255,255)")
        dial.valueChanged.connect(lcd.display)

        
        #label.setMinimumWidth(width-10)
        label.setMinimumHeight(16)
        #label.setAlignment(mayaMixin.Qt.AlignHCenter)
        if not self.trainName:
            label.setText("Train's Name Here")
        else:
            label.setText(self.trainName)
        dial.setMinimumHeight(120)
        dial.setMinimumWidth(100)
        dial.setWrapping(False)
        #dial.setMinimum(-20)
        #dial.setMaximum(20)
        dial.setMinimum(-50)
        dial.setMaximum(50)
    
        #self.adjustSize()
        
        self.speedDial = dial
        #lcd.setNumDigits(3)
        lcd.setDigitCount(3)
        lcd.setMinimumHeight(50)
        lcd.setMinimumWidth(75)
        
        btnStop.setText("Stop this train")
        btnStop.setStyleSheet("background-color: rgb(200,0,0); color:rgb(255,255,255)")
        btnSelect.setText("Select this train")
        btnSelect.setStyleSheet("background-color: rgb(200,200,0); color:rgb(0,0,0)")
        btnReset.setText("Reset this train")
        btnReset.setStyleSheet("background-color: rgb(100,0,100); color:rgb(255,255,255)")
        btnResetRev.setText("R")
        btnResetRev.setStyleSheet("background-color: rgb(100,0,100); color:rgb(255,255,255)")
        btnDelete.setText("Remove this train")
        btnDelete.setStyleSheet("background-color: rgb(0,0,0); color:rgb(255,255,255)")
            
        dial.valueChanged.connect(lcd.display)
        dial.valueChanged.connect(self.setTrainSpeed)
        btnStop.pressed.connect(self.stopThisTrain)
        btnSelect.pressed.connect(self.selectThisTrain)
        btnReset.pressed.connect(self.resetThisTrain)
        btnResetRev.pressed.connect(self.resetThisTrainReverse)
        btnDelete.pressed.connect(self.removeButtonHandler)

        trainCameraBtn.pressed.connect(self.switchToTrainCamera)
        engineCameraBtn.pressed.connect(self.switchToEngineCamera)
        tankerCameraBtn.pressed.connect(self.switchToTankerCamera)
        perspCameraBtn.pressed.connect(self.switchToPerspCamera)

        
        speed = mc.getAttr(self.trainName+".speed")
        #print "speed attrValue %d"%speed
        lcd.display(speed)
        dial.setValue(speed*10)
        
        
        #self.setGeometry(height, width, 250, 150)
        #self.setWindowTitle('Train Control')
        #self.show()
        #self.setLayout(hbox)
        #self.setFrameStyle(QFrame.Box | QFrame.Raised)
        
    def moveSphere(self):
        """
        Moves an example sphere by some value
        - This is to test value update from the UI during playback
        - Seems to work
        """
        sender = self.sender()
        #print "inside moveSphere %d"%sender.value()
        mc.move(0,sender.value(),0,'pSphere1')

    def setTrainSpeed(self):
        sender = self.sender()
        #print "contollerH setTRainSpeed %d"%sender.value()
        if mc.objExists(self.trainName):
            #print "trainController -- setting train speed %f"% (sender.value() / 10.0)
            mc.setAttr(self.trainName+'.speed',sender.value()/10.0)

    def selectThisTrain(self):
        if mc.objExists(self.trainName):
            mc.select(self.trainName,tgl=1)
    
    def resetThisTrain(self):
        speed = self.speedDial.value()
        track.resetTrain(train=self.trainName, speed=speed/10.0)
    def resetThisTrainReverse(self):
        speed = self.speedDial.value()
        track.resetTrain(forward=0,train=self.trainName, speed=speed/10.0)
        
    def stopThisTrain(self):
        if mc.objExists(self.trainName):
            mc.setAttr(self.trainName+'.speed',0)
        self.speedDial.setValue(0)
        
    def removeButtonHandler(self):
        reply = QtWidgets.QMessageBox.question(self, 'Message',
            "Are you sure to remove this train?", QtWidgets.QMessageBox.Yes | 
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.removeThisTrain()
        
    def removeThisTrain(self):
        #if mc.objExists(self.trainName):
        #    mc.setAttr(self.trainName + '.speed',0)
        #self.speedDial.setValue(0)
        
        # parent = self.parent()
        # while parent:
            # print parent
            # parent = self.parent()
        mc.delete('allTrainsGroup|'+self.trainName)
        #print "TrainControllerH removeThisTrain"
        
        #print self.WoodenTrainControlWindow
        index = self.WoodenTrainControlWindow.findControllerIndex(trainName=self.trainName)
        self.WoodenTrainControlWindow.deleteTrainController(index)
            
        pass

    def switchToTrainCamera(self):
        camera = track.findTrainCamera(self.trainName, 'trainCamera')
        track.switchCameras(camera)
        pass

    def switchToEngineCamera(self):
        camera = track.findTrainCamera(self.trainName, 'engineerCamera')
        track.switchCameras(camera)
        pass
    
    def switchToTankerCamera(self):
        camera = track.findTrainCamera(self.trainName, 'tankerCamera')
        track.switchCameras(camera)
        pass
    
    def switchToPerspCamera(self):
        #camera = track.findTrainCamera(self.trainName, None)
        track.switchCameras(None)
        pass
    
    
        
#iconPath = os.getenv("MAYA_APP_DIR") + "/tkTestIcons/"
#print iconPath
#testicon = iconPath + "testIcon100.png"
#print testicon

# Creates a dockable Maya window with a LCD readout and a slider
# Will control the speed of the default train when the slider is moved
# class Example(mayaMixin.MayaQWidgetDockableMixin, QtWidgets.QWidget):
 
    # def __init__(self):
        # super(Example, self).__init__()
        # self.setDockableParameters(dockable=True, floating=True, area="top", width=300, height=200)
        
        # self.initUI()
        
    # def initUI(self):
        # lcd = QtWidgets.QLCDNumber(self)
        # sld = QtWidgets.QSlider(mayaMixin.Qt.Horizontal, self)

        # vbox = QtWidgets.QVBoxLayout()
        # vbox.addWidget(lcd)
        # vbox.addWidget(sld)

        # self.setLayout(vbox)
        # sld.setMaximum(20)
        # sld.setMinimum(-10)        
        # sld.valueChanged.connect(lcd.display)
        # sld.valueChanged.connect(self.setTrainSpeed)
        
        # self.setGeometry(300, 300, 250, 150)
        # self.setWindowTitle('Signal & slot')
        # self.show()
        
        
    # def moveSphere(self):
        # """
        # Moves an example sphere by some value
        # - This is to test value update from the UI during playback
        # - Seems to work
        # """
        # sender = self.sender()
        # #print "inside moveSphere %d"%sender.value()
        # mc.move(0,sender.value(),0,'pSphere1')

    # def setTrainSpeed(self):
        # print "setTrainSpeed %d"%sender.value() / 10.0
        # sender = self.sender()
        # train = "classicFreightTrainGroup1"
        # if mc.objExists(train):
            # mc.setAttr(train+'.speed',sender.value()/10.0)


        
"""
#SAMPLE CODE FOR USING TABWIDGETS

    tab = QtWidgets.QTabWidget(self)
    
    page1 = QtWidgets.QWidget()
    
    p1v = QtWidgets.QVBoxLayout()
    page1.setLayout(p1v)
    
    for i in range(10):
        pL1=QtWidgets.QLabel()
        pL1.setText("Page%d"%i)
        pL1.setMinimumHeight(20)
        p1v.addWidget(pL1)
    
    parent = pL1.parent()
    i = 0
    while i < 10 and parent:
        print parent
        i += 1
        parent = parent.parent()
    
    print pL1.layout() # Label has no layout inside it
    print page1.layout() # Label has a parent (page1)
    print pL1.parent().layout() # page1 has a layout inside it (p1v)
    
    
    #page1.show()
    
    #p1v.addWidget(pl1)
    
#    page2 = QtWidgets.QWidget()
    
#        page3 = QtWidgets.QWidget()
    
    tab.addTab(page1, "page1")
#        tab.addTab(page2, "page2")
#        tab.addTab(page3, "page3")
    
    tab.show()
    return
"""