# -*- coding: utf-8 -*-
import PyMGB
import simplejson as json
from handleImage import handleImage
from AbtTouch import CTouchScreen
import time
import PyInputKeyboard
import os
from logger import MyLog
import xlwt

#############################
class TAFramework():
#############################

    '''
    For report
    '''
    
    
    def __init__(self, inputCasesPath):
        
        self.InCasePath = inputCasesPath
        self.initReport()
        self.initTools()
    
    ###########################
    def initReport(self):
    ###########################

        self.passFlag = 1
        self.row = 0
        col = 0
        self.msg = ""
        
        self.workbook = xlwt.Workbook(encoding="utf-8")
        self.report = self.workbook.add_sheet("report")
   
        self.report.write_merge(0,0,0,2,"Navigation test report")
        self.row  = self.row + 1
        
        self.report.write(self.row, 0, "Case Name")
        self.report.write(self.row, 1, "Status")
        self.report.write(self.row, 2, "Message")
        
        self.row = self.row + 1

        
    #initTools MGB
    ########################
    def initTools(self):
    ########################
        self.MGB = PyMGB.PyMGB(isVirtual=False)
        self.MGB.startGrabbing()
        
        #Touch screen Initialization
        self.touch = CTouchScreen()
	if self.touch.initParams(26839, 1, self.touch.CANCaseXL, self.touch.DISPLAY_TOP):
            MyLog.info("TouchScreen is OK")
            print "touchScreen is OK"
        else:
            MyLog.error("TouchScreen failed")
            print "touchScreen failed"
        
        self.runCases()


    #Read Json file and run cases
    ####################################
    def runCases(self):
    ####################################
        #print self.InCasePath
        with open(self.InCasePath) as dataFile:
            self.recogCharacter = json.load(dataFile)

        #Check what the case is, destination input or
        #Route calculation
        try:
            if  self.recogCharacter["DestinationInput"]:
                MyLog.debug("Now run Destination input case")
                self.runInputDestination()
        except Exception as e:
            MyLog.debug(e.message + " No Destination")
            print e.message + " No Destination"

        try:
            if self.recogCharacter["RouteCalculation"]:
                MyLog.debug("Now run route calculation case")
                self.runRouteCalculation()
        except Exception as e:
            MyLog.debug(e.message + " No RouteCalculation")
            print e.message + "No RouteCalculation"


    #Destination input
    ###################################
    def runInputDestination(self):
    ###################################
        print self.recogCharacter["DestinationInput"]
        
        if self.recogCharacter["DestinationInput"]["NormalInput"]:
            
            for case in self.recogCharacter["DestinationInput"]["NormalInput"]:
                try:
                    #switch input method 
                    if self.recogCharacter["DestinationInput"]["NormalInput"][case]["Input method"] == "Free research":
                        MyLog.debug("Now run " + case + ":" +\
                                    self.recogCharacter["DestinationInput"]["NormalInput"][case]["Name"])
                        self.report.write(self.row, 0, self.recogCharacter["DestinationInput"]["NormalInput"][case]["Name"])
                        self.freeSearch(self.recogCharacter["DestinationInput"]["NormalInput"][case]["Input content"])

                        if self.passFlag == 1:
                            self.report.write(self.row, 1, "Passed")
                        else:
                            self.report.write(self.row, 1, "Failed")
                            self.report.write(self.row, 2, self.msg)

                        self.row = self.row + 1
                        self.msg = ""
                        self.passFlag = 1
                        
                    '''
                    ####################################################################################
                    If you have to use favorite or other ways to input destination, please add code here
                    ####################################################################################
                    '''
                except Exception as e:
                    MyLog.error(e.message + " recogCharacters failed")
                    self.msg = e.message + " recogCharacters failed"
                    self.report.write(self.row, 1, "Failed")
                    self.report.write(self.row, 2, self.msg)
                    self.msg = ""
                    self.passFlag = 1
                    print e.message + " recogCharacters failed"
                    
        print "Destination not NULL"

    #Route Calculation
    ##################################
    def runRouteCalculation(self):
    ##################################
        
        def checkParkPop():
            popString = "驻车信息"
            for i in range(5):
                self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviParkingInformation.xml", popString.decode("utf-8"))
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
            time.sleep(10)


        if self.recogCharacter["RouteCalculation"]:
            for case in self.recogCharacter["RouteCalculation"]:
                MyLog.debug("Now run RouteCalculation case")
                print self.report
                self.report(self.row, 0, self.recogCharacter["RouteCalculation"][case]["Name"])
                
                self.routeCalPrecondition()                
                
                if not self.recogCharacter["RouteCalculation"][case]["Map"]:

                    MyLog.debug("Now run " + case + ":" +\
                                self.recogCharacter["RouteCalculation"][case]["Name"])
                    
                    coords = self.recogCharacter["RouteCalculation"][case]["Coords"]
                    
                    #Set POI
                    setPOI(coords[0], coords[1])
                    #Check parking
                    if not checkParkPop() :#timeout.
                        self.passFlag = 0
                        self.mag = "Time out, Test Failed"
                        MyLog.error("Time out, Test Failed")
                        self.report(self.row, 1, "Failed")
                        self.report(self.row, 2, msg)
                        self.passFlag = 1
                        self.msg = ""
                        self.row = self.row + 1
                        print "Time out, Test Failed!"
                        
                    else:
                        
                        self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviRouteCalculationIconCheck.xml", None)
                        likelihood = self.handleImage.recognizeImage(r"D:\Temp\TA\MGB\RecogImage\Flag.png")


                        if likelihood > 0.60:
                            MyLog.debug("Get the flag Passed, and then check route information")
                            print "Get the flag Passed, and then check route information"
                            
                            #After find the route flag then you should check the route info flag and get route mile info
                            #Then check the route info flag first
                            self.grabAndHandleImage(r"D:\Temp\TA\Mask\RouteFlagInformation.xml", None)                            
                            likelihood = self.handleImage.recognizeImage(r"D:\Temp\TA\MGB\RecogImage\RouteCalFlag.PNG", None)
                            if likelihood > 0.75:
                                MyLog.debug("Get the route info flag")
                                self.msg = msg + "Get the route info flag"
                                print "Get the route info flag"
                            else:
                                self.msg = self.msg + " Get the route info failed"
                                self.passFlag = 0
                                MyLog.error("Get the route info failed")
                                print "Get the route info failed"

                            #Get the route mile info
                            self.grabAndHandleImage(r"D:\Temp\TA\Mask\RouteMilInformation.xml", None)
                            result, disL, flag, rect, countNum = self.handleImage.recognizeCharacters_AIn()
                            
                            print "#########################################"
                            print result
                            for i in range(countNum):
                                try:
                                    print result[i]
                                except Exception as e:
                                    self.msg = self.msg + "Return result is wrong " + e.message
                                    self.passFlag = 0
                                    MyLog.error("Return result is wrong " + e.message)
                                    print "return result is wrong " + e.message
                            
                            if self.passFlag == 0:
                                self.report(self.row, 1, "Failed")
                                self.report(self.row, 2, self.msg)
                                self.passFlag = 1
                                self.msg = ""
                                self.row = self.row + 1
                            else:
                                self.report(self.row, 1, "Passed")
                                self.report(self.row, 2, self.msg)
                                self.row = self.row + 1
                                self.msg = ""
                                
                                
                            self.touch.touchScreen(440, 135, 500, 1, 1)
                            time.sleep(3)
                            
                        else:
                            MyLog.error("Failed, couldn't find the flag")
                            print "Failed, couldn't find the flag"
                            self.msg = self.msg + "Failed, couldn't find the flag"
                            self.report(self.row, 1, "Failed")
                            self.report(self.row, 2, self.msg)
                            self.row  = self.row + 1
                            self.msg = ""
                            self.passFlag = 1
                            self.touch.touchScreen(440, 135, 500, 1, 1)
                            time.sleep(3)
                            

                elif self.recogCharacter["RouteCalculation"][case]["Map"].get("drag"):

                    MyLog.debug("Now run " + case + ":" +\
                                self.recogCharacter["RouteCalculation"][case]["Name"])
                    coordsDrag = self.recogCharacter["RouteCalculation"][case]["Map"]["drag"]
                    self.touch.dragCoords(coordsDrag[0], coordsDrag[1], coordsDrag[2], coordsDrag[3])

                    coords = self.recogCharacter["RouteCalculation"][case]["Coords"]
                    
                    #Set POI 
                    setPOI(coords[0], coords[1])
                    #Check parking
                    if not checkParkPop():
                        self.msg = self.msg + "Time out, Test Failed"
                        self.passFlag = 0
                        self.report(self.row, 1, "Failed")
                        self.report(self.row, 2, msg)
                        self.passFlag = 1
                        self.row = self.row + 1
                        self.msg = ""
                        print "Time out, Test Failed"

                    else:
                        #Need to drag the screen         
                        self.touch.dragCoords(coordsDrag[0], coordsDrag[1], coordsDrag[2], coordsDrag[3])

                        time.sleep(3)
                        self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviRouteCalculationIconCheck.xml", None)
                        likelihood = self.handleImage.recognizeImage(r"D:\Temp\TA\MGB\RecogImage\Flag.png")

                        
                        if likelihood > 0.60:
                            MyLog.debug("Recognize image passed")
                            print "Passed"
                            self.touch.touchScreen(200, 650, 500, 1, 1)#Touch navi deviation
                            time.sleep(3)
                            
                            #After find the route flag then you should check the route info flag and get route mile info
                            #Check the route info flag first
                            self.grabAndHandleImage(r"D:\Temp\TA\Mask\RouteFlagInformation.xml", None)                            
                            likelihood = self.handleImage.recognizeImage(r"D:\Temp\TA\MGB\RecogImage\RouteCalFlag.PNG", None)
                            if likelihood > 0.75:
                                self.msg = self.msg + "Get the route info flag"
                                MyLog.debug("Get the route info flag")
                                print "Get the route info flag"
                            else:
                                self.msg = self.msg + "Get the route info failed"
                                self.passFlag = 0
                                MyLog.error("Get the route info failed")
                                print "Get the route info failed"

                            #Get the route mile info
                            self.grabAndHandleImage(r"D:\Temp\TA\Mask\RouteMilInformation.xml", None)
                            result, disL, flag, rect, countNum = self.handleImage.recognizeCharacters_AIn()
                            
                            print "#########################################"
                            print result
                            for i in range(countNum):
                                try:
                                    print result[i]
                                except Exception as e:
                                    self.passFlag = 0
                                    self.msg = self.msg + "return result is wrong " + e.message
                                    MyLog.error("return result is wrong " + e.message)
                                    print "return result is wrong " + e.message

                                    
                            if self.passFlag == 0:
                                self.report(self.row, 1, "Failed")
                                self.report(self.row, 2, self.msg)
                                self.passFlag = 1
                                self.msg = ""
                                self.row = self.row + 1
                            else:
                                self.report(self.row, 1, "Passed")
                                self.report(self.row, 2, self.msg)
                                self.row = self.row + 1
                                self.msg = ""
                            
                            self.touch.touchScreen(440, 135, 500, 1, 1)#Touch calc navi route calculation
                            time.sleep(3)
                            
                        else:
                            self.msg = self.msg + "Failed, couldn't find the flag"
                            self.passFlag = 0
                            MyLog.error("Failed, couldn't find the flag")
                            print "Failed, couldn't find the flag"
                            self.report(self.row, 1, "Failed")
                            self.report(self.row, 2, self.msg)
                            self.passFlag = 1
                            self.msg = ""
                            self.row = self.row + 1
                            self.touch.touchScreen(200, 650, 500, 1, 1)#Touch navi deviation
                            time.sleep(3)
                            self.touch.touchScreen(440, 135, 500, 1, 1)#Touch cancel navi route calculation
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
            MyLog.debug("Now it's in the navi screen")
            print "It's in navi screen"
        else:
            self.touch.touchScreen(68, 619, 500, 1, 1)
            time.sleep(1)

        #Then we check if we are in search screen
        a = "搜索"
        MyLog.debug("Now check the '搜索' mask")
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\FreeSearch.xml", a.decode('utf-8'))
        chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
        
        print disL
        
        if disL < 0.87:
            self.touch.touchScreen(68, 619, 500, 1, 1)#Touch Navi Menu
            time.sleep(3)
            self.touch.touchScreen(1468, 140, 500, 1, 1)#Touch Navi Setting Button
            time.sleep(3)
        else:
            self.touch.touchScreen(1468, 140, 500, 1, 1)#Touch Navi Setting Button
            time.sleep(3)
            
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\RouteInformation.xml", None)
        likelihood = self.handleImage.recognizeColor([25,55], [25,55], [25,55])

        if likelihood == 1:
            self.touch.touchScreen(265, 155, 500, 1, 1)#Back up
            time.sleep(1)
        else:
            print "open setting"
            self.touch.touchScreen(1468, 140, 500, 1, 1)#Touch Navi Setting Button
            time.sleep(1)
            self.touch.touchScreen(1055, 530, 500, 1, 1)# Open the navi Setting
            time.sleep(1)
            self.touch.touchScreen(265, 155, 500, 1, 1)#Back up
            time.sleep(1)
            
                
            

    #Before destination input, you have to do the precondition
    #################################
    def desInPrecondition(self, coordX, coordY):
    #################################
        
        #Grab image to check what screen is
        #At first check if it is in navi    
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\NaviCheck.xml", None)
        colorResult = self.handleImage.recognizeColor([65,75], [55,65], [15,30])
        
        if colorResult == 1:
            MyLog.debug("It's in navi screen")
            print "It's in navi screen"
        else:
            self.touch.touchScreen(68, 619, 500, 1, 1)
            time.sleep(1)

        #Then we check if we are in search screen
        a = "搜索"
        MyLog.debug("Now check '搜索' mask")
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\FreeSearch.xml", a.decode('utf-8'))
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
            MyLog.info("Keyinput initialization success")
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
                        self.msg = "Failed!!! characters not found"
                        self.passFlag = 0
                        MyLog.error("Failed!!! characters not found")
                        print "failed!!! characters not founded"
                        break
                    
                if detailCheckFlag != 0:
                    time.sleep(3)
                    self.grabAndHandleImage(r"D:\Temp\TA\Mask\CharactersInputCheck.xml", inputContent[0])
                    chResult, disL, flag, rect = self.handleImage.recognizeCharacters()

                    if disL > 0.9:
                        self.checkDestination(inputContent[0])
                    else:
                        self.msg = "Failed!!! characters not found"
                        self.passFlag = 0
                        MyLog.error("Failed!!! characters not found")
                        print "failed!!! characters not founded"
            else:
                self.checkDestination(inputContent[0])
                
            time.sleep(2)
            #self.inputC.deleteEntry()
        else:
            self.inputC.enterString(inputContent[0], 200, 2, 0)
            #time.sleep(5)
            #Touch OK button to input string
            self.inputC.touchCoords(1180, 580, 200, 2, 0)
            time.sleep(3)

            self.grabAndHandleImage(r"D:\Temp\TA\Mask\CharactersInputCheck.xml", inputContent[0])
            chResult, disL, flag, rect = self.handleImage.recognizeCharacters()
            
            if disL > 0.9:
                self.checkDestination(inputContent[0])
            else:
                self.msg = "Failed!!! characters not found"
                self.passFlag = 0
                MyLog.error("Failed!!! characters not found")
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
                MyLog.debug("Please wait!!! Wait for information")
                print "Please wait"

                #Grab imge and imgeprocessing
                self.grabAndHandleImage(r"D:\Temp\TA\Mask\WaitDestinationCheck.xml", inputContent)
                time.sleep(4)

            else:
                waitDoneFlag = 1
                break
            
        if waitDoneFlag == 1:
            
            recFlag = self.loopCheckDes(620, 680, 620, 320, 20, inputContent)
            if recFlag == 0:
                self.inputC.deleteEntry()
                return recFlag

        else:
            self.passFlag = 0
            self.msg = "Failed!!! Timeout"
            MyLog.error("Failed!!! Timeout")
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
            #One by one check
            #Grab imge and imgeprocessing
            oneCharacter = inputContent[0].encode("utf-8")
            
            try:
                print oneCharacter
            except Exception as e:
                MyLog.error(e.message + " Can't print characters")
                print e.message + " Can't print characters"
                
            if oneCharacter.isalpha():
                #Touch OK button in the bottom screen.
                #a-z or A-Z only need to check if input is right after touch OK button
                MyLog.debug("Now input English characters")
                print "Now input English characters"
                self.inputC.touchCoords(1180, 580, 200, 2, 0)
                return 1

                
            elif oneCharacter.isdigit():

                #0-9 only need to check if input is right
                MyLog.debug("Now input numbers")
                print "Now input numbers"
                return 1

            else:
                #chinese characters you have to check carefully. Loopcheck if necessary
                
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

    ##########################################
    def loopCheckDes(self, csX,  csY , ceX, ceY, offset, inputContent):
    ##########################################
        '''
        When loopCheckDes is used csX,csY,ceX,ceY is equvilent to abt drag parameters
        The offset para is to recorrect the drag action. It is different with loopCheck
        You don't have to decide the number of loop
        '''

        MyLog.debug("Now in loopCheckDestinatons")
        print "Now we are in loopCheckDes"
        
        self.grabAndHandleImage(r"D:\Temp\TA\Mask\DestinationCheck.xml", inputContent)
        chResult, disL, flag, rect, countNum = self.handleImage.recognizeCharacters_RC()

        firstLine = chResult[0]
        print chResult[0]
        checkFlag = 1
        
        if countNum < 3:
            MyLog.error("Something wrong happens, please check Image " + str(self.MGB.ImgFN))
            print "Something wrong happens, please check Image " + self.MGB.ImgFN
            checkFlag = 0

        while(1):
            self.touch.dragCoords(csX,csY,ceX,ceY)
	    #time.sleep(1)
	    self.touch.dragCoords(csX,csY,ceX,abs(csY - offset))
            time.sleep(1)
            
	    self.grabAndHandleImage(r"D:\Temp\TA\Mask\DestinationCheck.xml", inputContent)
            chResult, disL, flag, rect, countNum = self.handleImage.recognizeCharacters_RC()

            if chResult[0] == firstLine:
                break
            else:
                firstLine = chResult[0]

            if countNum < 3:
                #########################################################################
                #Here we should now in this cluster MIB2+ the destination always shows 3 result
                #So we can code like this
                #If not we should change our logic
                #########################################################################
                print "Something wrong happens, please check Image " + self.MGB.ImgFN
                checkFlag = 0
                
        return checkFlag


    def deinit(self):
        '''
        self.inputC.deinitParams()
        '''
        self.MGB.stopGrabbing()
        self.workbook.save(r"D:\Temp\TA\report\report.xls")
        

    
if __name__ == "__main__":
    inputCasesPath = r"D:\Temp\TA\MGB\Config\InputCases.json"
    TAF = TAFramework(inputCasesPath)
    TAF.deinit()

    
