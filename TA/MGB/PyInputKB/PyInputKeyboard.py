# -*- coding: utf-8 -*-
"""
Module for realizing keyboard touch events on displays (MIB2p)
"""
# coding: utf8
# © Audi, all rights reserved
import ctypes
import json
import os
import sys
import yaml
import time

#Path
EDAS_Dir = r"D:\Temp\TA\MGB"


#==========================================
def swipe_ToRightScreen(CubeInfo, KBD): #finger right to left
#==========================================

    """ SIMPLIFY MIND-TWISTING SWIPE GESTURE """

    #TBD: read screen dimensions from cube info
    #xS, xE  = 468, 1283 #left to right
    xS, xE  = 1283, 468 #right to left
    yS, yE  = 435, 440
    KBD.dragCoords(xS,  yS , xE,  yE)
    sleep(2) # until we have feedback loop
    
#==========================================
def swipe_ToLeftScreen(CubeInfo, KBD): #finger left to right
#==========================================

    """ SIMPLIFY MIND-TWISTING SWIPE GESTURE """

    #TBD: read screen dimensions from cube info
    xS, xE  = 468, 1283 #left to right
    #xS, xE  = 1283, 468 #right to left
    yS, yE  = 435, 440
    KBD.dragCoords(xS,  yS , xE,  yE)
    sleep(2) # until we have feedback loop

#=================
class CKeyboard():
#=================
    """
    Class CKeyboard to realize function like init, deinit, enterCharacter and enterString
    """
    #constants used for initializing CANCase
    CANCaseXL = 0
    CANCardXL = 1
    CANCardX = 2

    #constants used for display index
    DISPLAY_TOP = 1
    DISPLAY_BOT = 2

    #configuration
    config = {}
    instanceOfAbt = {}
    characterPosition = {}

    

    #==================
    def __init__(self, isVirtual=False):
    #==================
        """load AbtPlugin library and write library directory + keyboard layouts into
        environment variable"""

        self.isVirtual = isVirtual
        
        bSuccess = True
        libAbt = os.path.abspath(EDAS_Dir+ "/PyInputKB/Lib")
        self.libKeyboardPath = os.path.abspath(EDAS_Dir + "/PyInputKB/KeyboardLayout/")
        os.environ['PATH'] = os.path.normpath(libAbt) + ';' + os.environ['PATH']

        #read configuration file
        self.config = {}
        configPath =os.path.abspath(EDAS_Dir + "/PyInputKB")
        with open(configPath + '\\' + 'config.yaml') as fp:
            self.config.update(yaml.load(fp))
        

    #===================
    def initParams(self, serialNumber, channel, hardwareType, displayIndex):
    #===================
        """init AbtPlugin -> set following parameter:
        *serialNumber*: serial number of CAN Case (MIB-CAN), if set to
        0 the first serial will be used
        *channel*: channel number of MIB-CAN
        *hardwareType*: CAN-Case hardware Type (e.g. CANCaseXL or CANCardXL, see constants)
        *displayIndex*: index of display which should be used (e.g. TOP or BOT) """

        if self.isVirtual:
            print "Virtual Keyboard initialized"
            return

        # load AbtPlugin library
        OldDir = EDAS_Dir + "/PyInputKB/Lib/"
        try:
            print "PyInputKB: init with serial nr:", serialNumber
            self.libabt = ctypes.cdll.LoadLibrary(OldDir +'AbtPlugin.dll')
            self.instaceOfAbt = self.libabt.getInstanceOfAbtPlugin()
            ret = self.libabt.init(self.instaceOfAbt,
                                     serialNumber,
                                     channel,
                                     hardwareType,
                                     displayIndex,
                                     1,
                                     0)
            print "Retval of libabt.init()", ret
            assert ret != -1
        except:
            #printException()
            print "Error: Initialization of MIB-CAN with serial " + serialNumber + " was not successfull"
            raise
			
        #changeDir(OldDir)
        print "Initialization was successfull"
        return ret
        
    #===================
    def deinitParams(self):
    #===================
        """deinit AbtPlugin """

        if self.isVirtual:
            return True
    
        
        value = self.libabt.deinit(self.instaceOfAbt)
        if value:
            print "Deinit was successfull"
            bSuccess = True
        else:
            print "Error: Deinit was not successfull"
            bSuccess = False
        return bSuccess

    #===================
    @staticmethod
    def getHalf(value):
    #===================
        """calculate half of a value"""

        return value/2

    #===================
    def getNewXOffset(self, oldXOffset, keyWidthRatio):
    #===================
        """calculate the next x value pending on key width ratio defined in JSON file
		Return the next x value
		Attributes:
		    oldXOffset: previous x offset
            keyWidthRatio: keyWidthRatio read out of JSON file
        """

        xOffset = oldXOffset

        xOffset += self.getHalf(keyWidthRatio * self.config['keyWidth'])
        return xOffset

    #===================
    def loadBottomKeyboardRow(self, yOffsetToUpperRow):
    #===================
        """load JSON file defining bottom row of keyboard (fpbr_standard.json)
        calculate the icon position and save in dict"""
        # load JSON file
        bSuccess = True
        try:
            with open(self.libKeyboardPath + '/' + 'fpbr_standard.json') as data_file:
                data = json.load(data_file)
        except IOError:
            return False

        #initialize x and y offset values
        #(y offset should be the last y position of the last keyboard road)
        xOffset = self.config['keyXOffset']
        yOffset = yOffsetToUpperRow

        yOffset += self.getHalf(data['bottom_row']['height'])

        #go through rows and calculate icon position
        for rowIndex in range(len(data['buttons'])):
            try:
                keyWidthRatio = int(data['buttons'][rowIndex]['button']['widthRatio'])
            except KeyError:
                keyWidthRatio = 1

            xOffset = self.getNewXOffset(xOffset, keyWidthRatio)

            #save icons + position in dict
            self.characterPosition[data['buttons'][rowIndex]['button']['type']] = {"x": xOffset, "y": yOffset}

            xOffset = self.getNewXOffset(xOffset, keyWidthRatio)

        xOffset = self.config['keyXOffset']
        return bSuccess

    #===================
    def readKeyboardLayout(self, keyboardLayout=""):
    #===================
        """load JSON file defining keyboard layout (default layout will be defined in config.yaml)
        calculate the icon position and save in dict
        return true, if keyboard layout was found, otherwise false """
        self.characterPosition = {}
        bSuccess = True
        yOffset = self.config['keyYOffset']

        #if there is no keyboard layout defined use default one (config.yaml)
        if keyboardLayout == "":
            keyboardLayout = self.config['defaultKeyboardLayout']

        try:
            with open(self.libKeyboardPath + '/' + keyboardLayout) as data_file:
                data = json.load(data_file)

            xOffset = self.config['keyXOffset']
            yOffset = self.config['keyYOffset']

            for rowIndex in range(len(data['rows'])):
                yOffset += self.getHalf(self.config['keyHeight'])

                for keyIndex in range(len(data['rows'][rowIndex]['keys'])):
                    try:
                        keyWidthRatio = int(data['rows'][rowIndex]['keys'][keyIndex]['keyWidthRatio'])
                    except KeyError:
                        keyWidthRatio = 1

                    xOffset = self.getNewXOffset(xOffset, keyWidthRatio)

                    self.characterPosition[data['rows'][rowIndex]['keys'][keyIndex]['key']] = {"x": xOffset, "y": yOffset}

                    xOffset = self.getNewXOffset(xOffset, keyWidthRatio)

                xOffset = self.config['keyXOffset']
                yOffset += self.getHalf(self.config['keyHeight'])

        except IOError:
            print "ERROR: Could not open JSON file: " + keyboardLayout
            bSuccess = False

        if bSuccess:
            bSuccess = self.loadBottomKeyboardRow(yOffset)
        return bSuccess

    #===================
    def enterCharacter(self, character, duration=200, displayIndex=DISPLAY_BOT, forceUsage=1):
    #===================
        """enter character on keyboard, following params can be used:
        character: 	string containing single char, which should be used
        duration: 	duration [ms] how long this icon should be pressed
        displayIndex: index of display, which should be used
        forceUsage:	1 if Force should be used
        return False, if character is not available"""
        
        if self.isVirtual:
            return True
    
        
        bSuccess = True
        try:
            #if character is a space -> space should be used
            if character == " ":
                character = "SPACE"

            xValue = self.characterPosition[character.upper()]["x"]
            yValue = self.characterPosition[character.upper()]["y"]

            #get force value to use for touching
            forceValue = self.config['forceValue']
            if forceUsage == 0:
			    forceValue = -1
			
            self.libabt.pressCoord(self.instaceOfAbt, xValue, yValue, duration, displayIndex, forceValue)
        except KeyError:
            print "ERROR: character: " + character + " not available."
            bSuccess = False

        return bSuccess

    #===================
    def enterString(self, stringToWrite, duration=200, displayIndex=DISPLAY_BOT, forceUsage=1):
    #===================
        """enter string on keyboard, following parameter can be used:
        stringToWrite: string which should be written on bottom display
        duration: duration [ms] how long this icon should be pressed
        displayIndex: index of display, which should be used
        forceUsage:	1 if Force should be used"""
        time.sleep(self.config['waitBetweenChars'])
        for idx, characterIndex in enumerate(stringToWrite):
            self.enterCharacter(characterIndex, duration, displayIndex, forceUsage)
            #if idx < 1:
            #    time.sleep(5)
            
            time.sleep(self.config['waitBetweenChars'])

	#===================
    def deleteEntry(self):
    #===================
    
        if self.isVirtual:
            return
    
        """delete given text input"""
        time.sleep(self.config['waitBetweenChars'] * 2)

        #get force value to use for touching
        forceValue = self.config['forceValue']

        self.libabt.dragCoord(self.instaceOfAbt,
                              self.config['maxDisplayWidth'],
                              self.characterPosition['BACKSPACE']["y"],
                              self.config['keyXOffset'],
                              self.characterPosition['BACKSPACE']["y"],
                              500,
                              self.DISPLAY_BOT,
                              forceValue)
        time.sleep(self.config['waitBetweenChars'] * 2)

    #===================
    def touchCoords(self,xValue, yValue,duration=200, displayIndex=DISPLAY_TOP, forceUsage=1):
    #===================
        print "PyInputKB: Touching Coords:", xValue, yValue        

        if self.isVirtual:
            return

        
    
        forceValue = 99
        if forceUsage == 0:
            forceValue = -1
        self.libabt.pressCoord(self.instaceOfAbt, xValue, yValue, duration, displayIndex, forceValue)
    #===================
    def dragCoords(self,xValueS, yValueS,xValueE, yValueE,duration=200, displayIndex=DISPLAY_TOP, forceUsage=1):
    #===================
        if self.isVirtual:
            return
        print "PyInputKB: drag from: ", xValueS, yValueS, " to: ", xValueE, yValueE
        forceValue = 99
        if forceUsage == 0:
            forceValue = -1
        self.libabt.dragCoord(self.instaceOfAbt,
                              xValueS,
                              yValueS,
                              xValueE,
                              yValueE,
                              500,
                              displayIndex,
                              forceValue)
if __name__ == "__main__":
    #Example Usage of PyAbt
    kbd = CKeyboard()
    if kbd.initParams(26839, 1, kbd.CANCaseXL, 1):
        kbd.readKeyboardLayout()
        print kbd.characterPosition
        kbd.enterCharacter("a")
        time.sleep(1)
        #kbd.enterString('xyz', 200, 2, 0)
        
        kbd.enterString('odizhongguolou', 200, 2, 0)
        kbd.deleteEntry()
        kbd.deinitParams()
        
