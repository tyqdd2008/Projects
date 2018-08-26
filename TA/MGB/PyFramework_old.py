import PyMGB
import simplejson as json
from handleImage import handleImage
from AbtTouch import CTouchScreen
import time
import PyInputKeyboard
import os

#############################
class TAFramework():
#############################
    def __init__(self, inputCasesPath):
        self.InCasePath = inputCasesPath
        self.initTools()


    #initTools MGB
    ########################
    def initTools(self):
    ########################
        self.MGB = PyMGB.PyMGB(isVirtual=False)
        
        #Touch screen Initialization
        self.touch = CTouchScreen()
	if self.touch.initParams(26839, 1, self.touch.CANCaseXL, self.touch.DISPLAY_TOP):
            print "touchScreen is OK"
        else:
            print "touchScreen failed"
        
        self.runCases()


    #Read Json file and run cases
    ####################################
    def runCases(self):
    ####################################
        print "a"
        print self.InCasePath
        with open(self.InCasePath) as dataFile:
            self.recogCharacter = json.load(dataFile)

        #Check what the case is, destination input or
        #Route calculation
        if  self.recogCharacter["DestinationInput"]:
            self.runInputDestination()
        else :
            self.runRouteCalculation()


    #Destination input
    ###################################
    def runInputDestination(self):
    ###################################
        print self.recogCharacter["DestinationInput"]
        
        if self.recogCharacter["DestinationInput"]["NormalInput"]:
            
            for case in self.recogCharacter["DestinationInput"]["NormalInput"]:
                
                #switch input method 
                if self.recogCharacter["DestinationInput"]["NormalInput"][case]["Input method"] == "Free research":
                    self.freeSearch(self.recogCharacter["DestinationInput"]["NormalInput"][case]["Input content"])

                #time.sleep(10)
                print "###################################"
                print case

                    
        print "Destination not NULL"

    #Route Calculation
    ##################################
    def runRouteCalculation(self):
    ##################################
        print "Route not NULL"


    #####################################
    def grabImage(self):
    #####################################
        self.MGB.startGrabbing()
        self.MGB.saveCurrentFrame()
        self.MGB.stopGrabbing()
        return self.MGB.ImgFN
    
    #Before destination input, you have to do the precondition
    #################################
    def desInPrecondition(self):
    #################################
        #Grab image to check what screen is
        #At first check if it is in navi
        self.MGB.startGrabbing()
        self.MGB.saveCurrentFrame()
        self.MGB.stopGrabbing()
        imagePath = self.MGB.ImgFN
        #imagePath =  self.grabImage()
        maskPath = r"D:\Temp\TA\Mask\NaviCheck.xml"
        recogPath = r"D:\Temp\TA\MGB\RecogImage\recogImage1.png"
        print imagePath
        
        self.handleImage = handleImage(imagePath,maskPath,recogPath,None)
        self.handleImage.greyROI()
        colorResult = self.handleImage.recognizeColor([65,75], [55,65], [15,30])
        
        if colorResult == 1:
            print "It's in navi screen"
        else:
            self.touch.touchScreen(68, 619, 500, 1, 1)

        #Then we check if we are in search screen
        #imagePath =  self.grabImage()
        self.MGB.startGrabbing()
        self.MGB.saveCurrentFrame()
        self.MGB.stopGrabbing()
        imagePath = self.MGB.ImgFN
        maskPath = r"D:\Temp\TA\Mask\FreeSearch.xml"
        recogPath = r"D:\Temp\TA\MGB\RecogImage\recogImage1.png"
        print imagePath
        self.handleImage = handleImage(imagePath,maskPath,recogPath,"Search")
        self.handleImage.greyROI()

        print "##############################"
        print "os.path.realpath(__file__)=%s" % os.path.realpath(__file__)
        
        chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
        print disL
        if disL > 0.9:
            self.touch.touchScreen(380, 140, 500, 1, 1)
        else:
            self.touch.touchScreen(68, 619, 500, 1, 1)
            time.sleep(3)
            self.touch.touchScreen(380, 140, 500, 1, 1)
            
        
    #free search method
    ##################################
    def freeSearch(self, inputContent):
    ##################################
        self.desInPrecondition()

        #Input characters Initialization
        self.inputC = PyInputKeyboard.CKeyboard()
        
        if self.inputC.initParams(26839, 1, self.inputC.CANCaseXL, 1):
            print "Keyinput initializition success"
            self.inputC.readKeyboardLayout()
            
        print "##############################"
        print "os.path.realpath(__file__)=%s" % os.path.realpath(__file__)
        
        if len(inputContent) > 1:
            self.inputC.enterString(inputContent[1], 200, 2, 0)
            #time.sleep(5)
            #self.checkCharacters(inputContent)
            time.sleep(2)
            #self.inputC.deleteEntry()
        else:
            self.inputC.enterString(inputContent[0], 200, 2, 0)
            #time.sleep(5)
            #self.checkCharacters(inputContent)
            time.sleep(2)
            #self.inputC.deleteEntry()

        self.inputC.deinitParams()

    #################################
    def checkCharacters(self, inputContent):
    #################################
        if len(inputContent) > 1:
            #imagePath = self.grabImage()
            self.MGB.startGrabbing()
            self.MGB.saveCurrentFrame()
            self.MGB.stopGrabbing()
            imagePath = self.MGB.ImgFN
            maskPath = r"D:\Temp\TA\Mask\CharactersCheck.xml"
            recogPath = r"D:\Temp\TA\MGB\RecogImage\recogImage1.png"
            
            self.handleImage = handleImage(imagePath,maskPath,recogPath,inputContent[0])
            self.handleImage.greyROI()

            print "##############################"
            print "os.path.realpath(__file__)=%s" % os.path.realpath(__file__)
                     
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            if disL > 0.9:
                print rect
            
        else:
            #imagePath = self.grabImage()
            self.MGB.startGrabbing()
            self.MGB.saveCurrentFrame()
            self.MGB.stopGrabbing()
            imagePath = self.MGB.ImgFN
            maskPath = r"D:\Temp\TA\Mask\CharactersCheck.xml"
            recogPath = r"D:\Temp\TA\MGB\RecogImage\recogImage1.png"
            
            self.handleImage = handleImage(imagePath,maskPath,recogPath,inputContent[0])
            self.handleImage.greyROI()

            print "##############################"
            print "os.path.realpath(__file__)=%s" % os.path.realpath(__file__)
                     
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            if disL > 0.9:
                print rect



        
    def deinit(self):
        '''
        self.inputC.deinitParams()
        '''
        

    
if __name__ == "__main__":
    inputCasesPath = r"D:\Temp\TA\MGB\Config\InputCases.json"
    TAF = TAFramework(inputCasesPath)
    '''
    TAF.MGB.startGrabbing()
    TAF.MGB.saveCurrentFrame()
    TAF.MGB.stopGrabbing()
    '''
    
