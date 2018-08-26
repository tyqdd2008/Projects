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
        self.MGB.startGrabbing()
        
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
        try:
            if  self.recogCharacter["DestinationInput"]:
                self.runInputDestination()
        except Exception as e:
            print e.message + "No Destination"

        try:
            if self.recogCharacter["RouteCalculation"]:
                self.runRouteCalculation()
        except Exception as e:
            print e.message + "No RouteCalculation"


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
                    
                '''
                ####################################################################################
                If you have to use favorite or other ways to input destination, please add code here
                ####################################################################################
                '''
                    
        print "Destination not NULL"

    #Route Calculation
    ##################################
    def runRouteCalculation(self):
    ##################################
        
        def checkParkPop():
            for i in range(5):
                self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviParkingInformation.xml", "Parking")
                chResult, disL, flag, rect = self.handleImage.recognizeCharacters()

                if disL > 0.9:
                    time.sleep(5)
                else:
                    return 1
            return 0

        def setPOI(coordX, coordY):
            self.touch.touchScreen(coordX, coordY, 500, 1, 1)
            time.sleep(3)
            self.touch.touchScreen(260, 145, 500, 1, 1)
            time.sleep(3)


        if self.recogCharacter["RouteCalculation"]:
            for case in self.recogCharacter["RouteCalculation"]:
                
                self.routeCalPrecondition()
                
                if not self.recogCharacter["RouteCalculation"][case]["Map"]:
                    
                    coords = self.recogCharacter["RouteCalculation"][case]["Coords"]
                    
                    #Set POI
                    setPOI(coords[0], coords[1])
                    #Check parking
                    if not checkParkPop() :#timeout.
                        print "Time out, Test Failed!"
                        
                    else:
                        
                        self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviRouteCalculationIconCheck.xml", None)
                        likelihood = self.handleImage.recognizeImage(r"D:\Temp\TA\MGB\RecogImage\Flag.png")

                        if likelihood > 0.75:
                            print "Passed"
                            self.touch.touchScreen(440, 135, 500, 1, 1)
                            time.sleep(3)
                            
                        else:
                            print "Failed, couldn't find the flag"
                            self.touch.touchScreen(440, 135, 500, 1, 1)
                            time.sleep(3)


                elif self.recogCharacter["RouteCalculation"][case]["Map"].get("drag"):
                    
                    print "Not in"
                    coordsDrag = self.recogCharacter["RouteCalculation"][case]["Map"]["drag"]
                    self.touch.dragCoords(coordsDrag[0], coordsDrag[1], coordsDrag[2], coordsDrag[3])

                    coords = self.recogCharacter["RouteCalculation"][case]["Coords"]
                    
                    #Set POI 
                    setPOI(coords[0], coords[1])
                    #Check parking
                    if not checkParkPop():
                        print "Time out, Test Failed"

                    else:
                        #Need to drag the screen         
                        self.touch.dragCoords(coordsDrag[0], coordsDrag[1], coordsDrag[2], coordsDrag[3])

                        time.sleep(3)
                        self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviRouteCalculationIconCheck.xml", None)
                        likelihood = self.handleImage.recognizeImage(r"D:\Temp\TA\MGB\RecogImage\Flag.png")

                        
                        if likelihood > 0.75:
                            print "Passed"
                            self.touch.touchScreen(200, 650, 500, 1, 1)
                            time.sleep(3)
                            self.touch.touchScreen(440, 135, 500, 1, 1)
                            time.sleep(3)
                            
                        else:
                            print "Failed, couldn't find the flag"
                            self.touch.touchScreen(200, 650, 500, 1, 1)
                            time.sleep(3)
                            self.touch.touchScreen(440, 135, 500, 1, 1)
                            time.sleep(3)
                        
        
        print "Route not NULL"
        

    #Before route calculation, you have to do the precondition
    #################################
    def routeCalPrecondition(self):
    #################################
        
        #Grab image to check what screen is
        #At first check if it is in navi    
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviCheck.xml", None)
        colorResult = self.handleImage.recognizeColor([65,75], [55,65], [15,30])
        
        if colorResult == 1:
            print "It's in navi screen"
        else:
            self.touch.touchScreen(68, 619, 500, 1, 1)

        #Then we check if we are in search screen        
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\FreeSearch.xml", "Search")
        chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
        
        print disL
        
        if disL < 0.87:
            self.touch.touchScreen(68, 619, 500, 1, 1)
            time.sleep(3)
        else:
            time.sleep(3)
            

    #Before destination input, you have to do the precondition
    #################################
    def desInPrecondition(self, coordX, coordY):
    #################################
        
        #Grab image to check what screen is
        #At first check if it is in navi    
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviCheck.xml", None)
        colorResult = self.handleImage.recognizeColor([65,75], [55,65], [15,30])
        
        if colorResult == 1:
            print "It's in navi screen"
        else:
            self.touch.touchScreen(68, 619, 500, 1, 1)

        #Then we check if we are in search screen        
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\FreeSearch.xml", "Search")
        chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
        
        print disL
        
        if disL > 0.87:
            self.touch.touchScreen(coordX, coordY, 500, 1, 1)
        else:
            self.touch.touchScreen(68, 619, 500, 1, 1)
            time.sleep(3)
            self.touch.touchScreen(coordX, coordY, 500, 1, 1)
            
        
    #free search method
    ##################################
    def freeSearch(self, inputContent):
    ##################################
        self.desInPrecondition(380, 140)

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
            checkFlag = self.checkCharacters(inputContent)
            
            if checkFlag == 0:
                #Then you input characters one by one
                for i in range(len(inputContent[0])):
                    self.inputC.enterString(inputContent[2][i], 200, 2, 0)
                    #print inputContent[0][i]
                    detailCheckFlag = self.checkCharacters([inputContent[0][i]])
                    if detailCheckFlag == 0:
                        print "failed!!! characters not founded"
                        break
                    
                if detailCheckFlag != 0:
                    self.checkDestination(inputContent[0])
            else:
                self.checkDestination(inputContent[0])
                
            time.sleep(2)
            #self.inputC.deleteEntry()
        else:
            self.inputC.enterString(inputContent[0], 200, 2, 0)
            #time.sleep(5)
            self.inputC.touchCoords(1180, 580, 200, 2, 0)
            time.sleep(3)

            self.grabAndHandleImage(r"D:\Temp\TA\Mask\CharactersInputCheck.xml", inputContent[0])
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            
            if disL > 0.9:
                self.checkDestination(inputContent[0])
            else:
                print "Failed!!! characters not founded"
            #self.inputC.deleteEntry()

        self.inputC.deinitParams()

            
    ###############################
    def checkDestination(self, inputContent):
    ###############################
        #Grab imge and imgeprocessing
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\WaitDestinationCheck.xml", inputContent)
        
        for i in range(25):
            waitDoneFlag = 0
            colorResult = self.handleImage.recognizeColor([20,35], [20,35], [20,30])
            if colorResult == 1:
                print "Please wait"

                #Grab imge and imgeprocessing
                self.grabAndHandleImage(r"D:\Temp\TA\Mask\WaitDestinationCheck.xml", inputContent)
                time.sleep(4)

            else:
                waitDoneFlag = 1
                break
            
        if waitDoneFlag == 1:
            
            self.grabAndHandleImage(r"D:\Temp\TA\Mask\DestinationCheck.xml", inputContent)
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            
            if disL > 0.87:
                print "Test passed"
                
            else:
                recFlag = self.loopCheck(600, 600, 600, 400, 3, inputContent)
                if recFlag == 0:
                    self.inputC.deleteEntry()
                    return recFlag

        else:
            print "Failed!!! Timeout"
        
    #################################
    def checkCharacters(self, inputContent):
    #################################
        if len(inputContent) > 1:
            
            self.grabAndHandleImage(r"D:\Temp\TA\Mask\CharactersCheck.xml", inputContent[0])            
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            
            if disL > 0.87:
                print rect.left, rect.top, rect.right, rect.bottom
                self.touch.touchScreen(self.handleImage.mask[0] + rect.left + (rect.right-rect.left)/2,\
                                       self.handleImage.mask[1] + rect.top + (rect.bottom - rect.top)/2,\
                                       500, 1, 1)
                return 1
            
            else:
                recFlag = self.loopCheck(1070, 250, 300, 240, 3, inputContent[0])
                if recFlag == 0:
                    self.inputC.deleteEntry()
                    return recFlag

        else:
            #Grab imge and imgeprocessing
            self.grabAndHandleImage(r"D:\Temp\TA\Mask\CharactersCheck.xml", inputContent[0])                     
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            
            if disL > 0.87:
                print rect.left, rect.top, rect.right, rect.bottom
                self.touch.touchScreen(self.handleImage.mask[0] + rect.left + (rect.right-rect.left)/2,\
                                       self.handleImage.mask[1] + rect.top + (rect.bottom - rect.top)/2,\
                                       500, 1, 1)
                return 1
            
            else:
                recFlag = self.loopCheck(1070, 250, 300, 240, 3, inputContent[0])
                if recFlag == 0:
                    self.inputC.deleteEntry()
                    return recFlag

    ##############################
    def grabAndHandleImage(self, maskPath, inputContent):
    ##############################
        self.MGB.saveCurrentFrame()
        imagePath = self.MGB.ImgFN
        
        recogPath = r"D:\Temp\TA\MGB\RecogImage\recogImage1.png"
        
        self.handleImage = handleImage(imagePath,maskPath,recogPath,inputContent)
        self.handleImage.greyROI()
        
    
    ##########################################
    def loopCheck(self, csX,  csY , ceX, ceY, num, inputContent):
    ##########################################
        '''When loopCheck is used, it is considered that
           the handleImage recognize characters is called once
           So there is no need to call it again. self.handleImage
           is useful
           the drag coord is needed and the count numbers for looping
           is also needed
        '''
        recFlag = 0
        for i in range(num):
            self.touch.dragCoords(csX,  csY , ceX, ceY, inputContent)

            #Grab imge and imgeprocessing
            self.grabAndHandleImage(r"D:\Temp\TA\Mask\CharactersCheck.xml", inputContent)
            
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            if disL > 0.87:
                print rect.left, rect.top, rect.right, rect.bottom
                self.touch.touchScreen(self.handleImage.mask[0] + rect.left + (rect.right-rect.left)/2,\
                                       self.handleImage.mask[1] + rect.top + (rect.bottom - rect.top)/2,\
                                       500, 1, 1)
                recFlag = 1
                return recFlag
        return recFlag
        
 
    def deinit(self):
        '''
        self.inputC.deinitParams()
        '''
        self.MGB.stopGrabbing()
        

    
if __name__ == "__main__":
    inputCasesPath = r"D:\Temp\TA\MGB\Config\InputCases.json"
    TAF = TAFramework(inputCasesPath)
    TAF.deinit()

    
