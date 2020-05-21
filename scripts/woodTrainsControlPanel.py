import maya.cmds as m
import maya.mel as mm

def sp():
	m.setParent('..')
	
def createControlPanel():
	window = m.window( title="Train Control Panel", iconName='trainsCP', widthHeight=(320,900))
	#window = m.window( title="Long Name", iconName='Short Name', widthHeight=(500, 550) )
	#m.columnLayout()
 	#initShelf = m.shelfLayout('Initialize', width=480)


#  	m.paneLayout(configuration="horizontal4")
#  	m.shelfLayout(width=400)
# 	sp()
#  	m.shelfLayout(width=400)
# #	m.setParent('..')
# 	sp()
#  	m.shelfLayout(width=400)
# 	sp()
#  	m.shelfLayout(width=400)
	m.scrollLayout()
	m.columnLayout()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Regular Pieces' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)

	#m.rowLayout(numberOfColumns=10)

	#global b1
	#b1 = 
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"shortCurveLeft\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="miniL"
	,image="woodTrainsleftCurve1.xpm"
	,image1="woodTrainsleftCurve1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"shortCurveLeft\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	#print b1
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"shortCurveRight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="miniR"
	,image="woodTrainsrightCurve1.xpm"
	,image1="woodTrainsrightCurve1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"shortCurveRight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveLeft\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="left"
	,image="woodTrainsleft1.xpm"
	,image1="woodTrainsleft1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumCurveLeft\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveRight\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="right"
	,image="woodTrainsright1.xpm"
	,image1="woodTrainsright1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumCurveRight\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton()
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"miniStraight\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="mini"
	,image="woodTrainsstraight1.xpm"
	,image1="woodTrainsstraight1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"miniStraight\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"shortStraight\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="short"
	,image="woodTrainsstraight1.xpm"
	,image1="woodTrainsstraight1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"shortStraight\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumStraight\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="med"
	,image="woodTrainsstraight1.xpm"
	,image1="woodTrainsstraight1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumStraight\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"longStraight\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="long"
	,image="woodTrainsstraight1.xpm"
	,image1="woodTrainsstraight1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"longStraight\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')

	sp()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Track Setup' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="import track\rreload(track)"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="init"
	,image="woodTrainsInit.xpm"
	,image1="woodTrainsInit.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nimport track\r\nreload(track)\r\nif not m.objExists(\"library\"):\r\n\tm.file(\"C:/myDocuments/maya/projects/woodTrains/scenes/woodTrainTrackLibrary.ma\",i=1)\r\n"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
		
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.analyzeTrack2()"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="link2"
	,image="woodTrainslinkTrack.xpm"
	,image1="woodTrainslinkTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.analyzeTrack2()"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	global dirTGL
	
	dirTGL = m.shelfButton()
	#print dirTGL
	m.shelfButton(dirTGL
	,e=1
	,enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track direction toggle"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="drTGL"
	,image="woodTrainsPegMale.xpm"
	,image1="woodTrainsPegMale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nnewVal = not m.getAttr(\"library.femaleToMaleDirection\")\rm.setAttr(\"library.femaleToMaleDirection\",newVal)\rif newVal:\r\tm.shelfButton(\""+dirTGL+"\", e=1,i=\"woodTrainsPegMale.xpm\")\relse:\r\tm.shelfButton(\""+dirTGL+"\", e=1,i=\"woodTrainsPegFemale.xpm\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.makeTestTrack()\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="TEST"
	,image="woodTrainscheckTest.xpm"
	,image1="woodTrainscheckTest.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.makeTestTrack()\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="m.move(0,6.1,0,r=1)\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="mvUP"
	,image="woodTrainsUpArrow.xpm"
	,image1="woodTrainsUpArrow.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="m.move(0,6.1,0,r=1)\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="m.move(0,-6.1,0,r=1)\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="mvDN"
	,image="woodTrainsDownArrow.xpm"
	,image1="woodTrainsDownArrow.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nm.move(0,-6.1,0,r=1)\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="import maya.cmds as m\r\nsel=m.ls(sl=1)\rtrack.attachTrack(sel[0],sel[1])"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="align"
	,image="woodTrains2pegAlign.xpm"
	,image1="woodTrains2pegAlign.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nsel=m.ls(sl=1)\rtrack.attachTrack(sel[0],sel[1])"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton()
	
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="import track\rreload(track)"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="camera"
	,image="woodTrainsrenderCamera.xpm"
	,image1="woodTrainsrenderCamera.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nimport track\r\nreload(track)\r\nif not m.objExists(\"renderCamera1\"):\r\n\tm.file(\"C:/myDocuments/maya/projects/woodTrains/scenes/renderCamera.ma\",i=1)\r\n"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
 	#m.setParent('..')
# 	m.setParent('..')

# 	m.shelfButton(
# 	enableCommandRepeat=1
# 	,enable=1
# 	,width=34
# 	,height=34
# 	,manage=1
# 	,visible=1
# 	,preventOverride=0
# 	,align="center"
# 	,label="Select Surface Toggle"
# 	,labelOffset=0
# 	,font="tinyBoldLabelFont"
# 	,imageOverlayLabel="mesh"
# 	,image="woodTrainspythonFamily.xpm"
# 	,image1="woodTrainspythonFamily.xpm"
# 	,style="iconOnly"
# 	,marginWidth=1
# 	,marginHeight=1
# 	,command="setObjectPickMask(\"Surface\" true;"
# 	,sourceType="mel"
# 	,actionIsSubstitute=0
# 	); 
# 
# 	m.shelfButton(
# 	enableCommandRepeat=1
# 	,enable=1
# 	,width=34
# 	,height=34
# 	,manage=1
# 	,visible=1
# 	,preventOverride=0
# 	,align="center"
# 	,label="Select Surface Toggle"
# 	,labelOffset=0
# 	,font="tinyBoldLabelFont"
# 	,imageOverlayLabel="pegs"
# 	,image="woodTrainsmelFamily.xpm"
# 	,image1="woodTrainsmelFamily.xpm"
# 	,style="iconOnly"
# 	,marginWidth=1
# 	,marginHeight=1
# 	,command="setObjectPickMask \"Other\" true;"
# 	,sourceType="mel"
# 	,actionIsSubstitute=0
# 	); 

	sp()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Train Setup' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="import maya.cmds as m\r\nif not m.objExists(\"trainGroup\"):\r\tm.file(\"C:/myDocuments/maya/p..."
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="train"
	,image="woodTrainsclassicFreightTrain.xpm"
	,image1="woodTrainsclassicFreightTrain.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nif not m.objExists(\"trainsGroup\"):\r\tm.file(\"C:/myDocuments/maya/projects/woodTrains/scenes/trainClassicFreight.ma\",i=1)"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	# Change this to bring trains in as a library, then copy-special "duplicate input graph" to activate them.
	
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.resetTrain()\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="reset"
	,image="woodTrainsresetTrainOnTrack.xpm"
	,image1="woodTrainsresetTrainOnTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.resetTrain()\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.resetTrain(forward=0)\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="teser"
	,image="woodTrainsresetTrainOnTrack.xpm"
	,image1="woodTrainsresetTrainOnTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.resetTrain(forward=0)\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
# 	m.shelfButton(
# 	enableCommandRepeat=1
# 	,enable=1
# 	,width=34
# 	,height=34
# 	,manage=1
# 	,visible=1
# 	,preventOverride=0
# 	,align="center"
# 	,label="track.moveTrainForward(\"trainGroup\")"
# 	,labelOffset=0
# 	,font="tinyBoldLabelFont"
# 	,imageOverlayLabel="drive"
# 	,image="woodTrainsdrive.xpm"
# 	,image1="woodTrainsdrive.xpm"
# 	,style="iconOnly"
# 	,marginWidth=1
# 	,marginHeight=1
# 	,command="track.moveTrainForward(\"trainGroup\")"
# 	,sourceType="python"
# 	,actionIsSubstitute=0
# 	); 
# 	#m.setParent('..')
# 	
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="reverse"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="reverse"
	,image="woodTrainstrainReverse.xpm"
	,image1="woodTrainstrainReverse.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.reverseTrain()"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.moveTrainForward(\"trainGroup\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="slow"
	,image="woodTrainsdriveSlow.xpm"
	,image1="woodTrainsdriveSlow.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nsel = m.ls(sl=1)\rif len(sel) > 0:\r\ttrack.setTrainSpeed(sel[0],speed=0.5,r=0)\relse:\r\ttrack.setTrainSpeed(speed=0.5,r=0)"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.moveTrainForward(\"trainGroup\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="med"
	,image="woodTrainsdriveMedium.xpm"
	,image1="woodTrainsdriveMedium.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nsel = m.ls(sl=1)\rif len(sel) > 0:\r\ttrack.setTrainSpeed(sel[0],speed=1.0,r=0)\relse:\r\ttrack.setTrainSpeed(speed=1.0,r=0)"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.moveTrainForward(\"trainGroup\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="fast"
	,image="woodTrainsdriveFast.xpm"
	,image1="woodTrainsdriveFast.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nsel = m.ls(sl=1)\rif len(sel) > 0:\r\ttrack.setTrainSpeed(sel[0],speed=2.0,r=0)\relse:\r\ttrack.setTrainSpeed(speed=2.0,r=0)"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.moveTrainForward(\"trainGroup\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="slower"
	,image="woodTrainsdriveSlower.xpm"
	,image1="woodTrainsdriveSlower.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nsel = m.ls(sl=1)\rif len(sel) > 0:\r\ttrack.setTrainSpeed(sel[0],speed=0.5,r=1)\relse:\r\ttrack.setTrainSpeed(speed=0.5,r=1)"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.moveTrainForward(\"trainGroup\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="faster"
	,image="woodTrainsdriveFaster.xpm"
	,image1="woodTrainsdriveFaster.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="import maya.cmds as m\r\nsel = m.ls(sl=1)\rif len(sel) > 0:\r\ttrack.setTrainSpeed(sel[0],speed=2.0,r=1)\relse:\r\ttrack.setTrainSpeed(speed=2.0,r=1)"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	sp()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Switch Tracks' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveRightSwitch\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="rSwch"
	,image="woodTrainsrightSwitch1.xpm"
	,image1="woodTrainsrightSwitch1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumCurveRightSwitch\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	);
	##m.setParent('..')	
 	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveLeftSwitch\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="lSwch"
	,image="woodTrainsleftSwitch1.xpm"
	,image1="woodTrainsleftSwitch1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumCurveLeftSwitch\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	);
	#m.setParent('..')
		
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveSwitch\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="crvSw"
	,image="woodTrainscurveSwitch1.xpm"
	,image1="woodTrainscurveSwitch1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumCurveSwitch\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveRightSwitch2\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="rSw2"
	,image="woodTrainsrightSwitch2.xpm"
	,image1="woodTrainsrightSwitch2.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumCurveRightSwitch2\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveLeftSwitch2\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="lSw2"
	,image="woodTrainsleftSwitch2.xpm"
	,image1="woodTrainsleftSwitch2.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"mediumCurveLeftSwitch2\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"mediumCurveLeftSwitch2\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="tJun"
	,image="woodTrainsleftSwitch2.xpm"
	,image1="woodTrainsleftSwitch2.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"TJunction\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	
	
	#m.setParent('..')

	sp()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Bridge Tracks' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"longAscendingStraight\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="up"
	,image="woodTrainsascendingTrack.xpm"
	,image1="woodTrainsascendingTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"longAscendingStraight\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"longDescendingStraight\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="down"
	,image="woodTrainsdescendingTrack.xpm"
	,image1="woodTrainsdescendingTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"longDescendingStraight\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"bridgeSupportSimple\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="suprt"
	,image="woodTrainsbridgeSupport1.xpm"
	,image1="woodTrainsbridgeSupport1.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"bridgeSupportSimple\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"bridgeSupportThinStacking\")\r"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="thin"
	,image="woodTrainsbridgeSupportThinStack.xpm"
	,image1="woodTrainsbridgeSupportThinStack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"bridgeSupportThinStacking\")\r"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"bridgeSupportStacking\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="track"
	,image="woodTrainsbridgeSupportStackTrackB.xpm"
	,image1="woodTrainsbridgeSupportStackTrackB.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"bridgeSupportStacking\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	sp()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Reversing Tracks' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"miniReverseFemaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="mini"
	,image="woodTrainsreverseFemale.xpm"
	,image1="woodTrainsreverseFemale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"miniReverseFemaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"shortReverseFemaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="short"
	,image="woodTrainsreverseFemale.xpm"
	,image1="woodTrainsreverseFemale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"shortReverseFemaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"medReverseFemaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="med"
	,image="woodTrainsreverseFemale.xpm"
	,image1="woodTrainsreverseFemale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"medReverseFemaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"longReverseFemaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="long"
	,image="woodTrainsreverseFemale.xpm"
	,image1="woodTrainsreverseFemale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"longReverseFemaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton()
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"miniReverseMaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="mini"
	,image="woodTrainsreverseMale.xpm"
	,image1="woodTrainsreverseMale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"miniReverseMaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"shortReverseMaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="short"
	,image="woodTrainsreverseMale.xpm"
	,image1="woodTrainsreverseMale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"shortReverseMaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"medReverseMaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="med"
	,image="woodTrainsreverseMale.xpm"
	,image1="woodTrainsreverseMale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"medReverseMaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="track.addTrackToSelected(\"longReverseMaleStraight\")"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="long"
	,image="woodTrainsreverseMale.xpm"
	,image1="woodTrainsreverseMale.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"longReverseMaleStraight\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	#m.setParent('..')
	
	sp()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Special Tracks' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="cross"
	,image="woodTrainscrossTrack.xpm"
	,image1="woodTrainscrossTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"crossTrack\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="three"
	,image="woodTrainssplitThree.xpm"
	,image1="woodTrainssplitThree.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"curveThreeSwitch\")"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton()

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="mStop"
	,image="woodTrainsmStop.xpm"
	,image1="woodTrainsmStop.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"maleStopper\")"
	,sourceType="python"
	,actionIsSubstitute=0
	);
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="fStop"
	,image="woodTrainsfStop.xpm"
	,image1="woodTrainsfStop.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"femaleStopper\")"
	,sourceType="python"
	,actionIsSubstitute=0
	);

	m.shelfButton()

	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="fCarp"
	,image="woodTrainsfemaleCarpetTrack.xpm"
	,image1="woodTrainsfemaleCarpetTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"femaleCarpet\")"
	,sourceType="python"
	,actionIsSubstitute=0
	);
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="mCarp"
	,image="woodTrainsmaleCarpetTrack.xpm"
	,image1="woodTrainsmaleCarpetTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.addTrackToSelected(\"maleCarpet\")"
	,sourceType="python"
	,actionIsSubstitute=0
	);
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="Kldg"
	,image="woodTrainsmaleCarpetTrack.xpm"
	,image1="woodTrainsmaleCarpetTrack.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.buildKludgeTrack()"
	,sourceType="python"
	,actionIsSubstitute=0
	);
	
	sp()
	m.iconTextStaticLabel( height=20, width=300, align="left", st='textOnly',l='Track Budging' )
	m.gridLayout(numberOfColumns=10, cellWidth=32, cellHeight=32)
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="up"
	,image="woodTrainsUpArrow.xpm"
	,image1="woodTrainsUpArrow.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.bumpUp()"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="down"
	,image="woodTrainsDownArrow.xpm"
	,image1="woodTrainsDownArrow.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.bumpDown()"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="left"
	,image="woodTrainsLeftArrow.xpm"
	,image1="woodTrainsLeftArrow.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.bumpLeft()"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	
	m.shelfButton(
	enableCommandRepeat=1
	,enable=1
	,width=34
	,height=34
	,manage=1
	,visible=1
	,preventOverride=0
	,align="center"
	,label="cross track"
	,labelOffset=0
	,font="tinyBoldLabelFont"
	,imageOverlayLabel="right"
	,image="woodTrainsRightArrow.xpm"
	,image1="woodTrainsRightArrow.xpm"
	,style="iconOnly"
	,marginWidth=1
	,marginHeight=1
	,command="track.bumpRight()"
	,sourceType="python"
	,actionIsSubstitute=0
	); 
	

	
	sp()
	m.showWindow( window )
