# -*- coding: utf-8 -*-
import cv2
import numpy as np
from ctypes import *
import json
#import simplejson

class AudiTest(Structure):
    _fields_ = [("texts",POINTER(c_wchar_p)),
                ("textCount", c_int)]

class RECT(Structure):
    _fields_ = [("left", c_long),
                ("top", c_long),
                ("right", c_long),
                ("bottom", c_long)]

class AudiBlock(Structure):
    _fields_ = [("rect", RECT),
                ("text", c_wchar_p),
                ("dist", POINTER(c_short)),
                ("charCount", c_int)]

class AudiResult(Structure):
    _fields_ = [("rect", RECT),
                ("result", c_char_p),
                ("disL", c_double),
                ("flag", c_bool)]

class AudiResult_RC(Structure):
    _fields_ = [("rect", RECT * 100),
                ("result", c_char_p * 100),
                ("disL", c_double * 100),
                ("flag", c_bool * 100),
                ("countNum", c_int)]

    

class handleImage(object):
    '''
    In this class, the job is to
    handle the image such as getting the
    ROI image, grey image and recognizing
    the characters
    '''
    def __init__(self, imagePath, maskPath, recogPath, recogConfig=None):
        #Read the image
        self.img = cv2.imread(imagePath)
        self.mask = self.getMask(maskPath)
        self.recogPath = recogPath
        self.recogConfig = recogConfig

    #Get the ROI and Grey image
    ##########################################
    def greyROI(self):
    ##########################################
        
        offX = self.mask[0]
        width = offX + self.mask[2]
        print offX, width

        offY = self.mask[1]
        height = self.mask[3] + offY
        print offY, height
        
        self.roi = self.img[offY : height, offX : width]

        #Save image for Hanvon recognition
        cv2.imwrite(self.recogPath, self.roi)  
        
    #In this function use HanvonOCR to recognize the Chinese characters
    ########################################
    def recognizeCharacters(self):
    ########################################
        
        #Initialize return result 
        self.recogDll = cdll.LoadLibrary(r'D:\Temp\TA\MGB\RecogImage.dll')
        self.recogDll.recogImage.restype = AudiResult

        path = c_char_p(self.recogPath)

        trasCharacter = self.recogConfig.encode('utf-8')
        #print s, len(s)
        result = c_char_p(trasCharacter)

        num = c_int(len(trasCharacter))

        returnResult = self.recogDll.recogImage(path, result, num)
        print returnResult.result, returnResult.disL, returnResult.flag
        return returnResult.result, returnResult.disL, returnResult.flag, returnResult.rect
        print "Left is ", returnResult.rect.left
        print "Top is ", returnResult.rect.top
        print "Right is ", returnResult.rect.right
        print "Bottom is ", returnResult.rect.bottom



    #In this function use HanvonOCR to recognize the Chinese characters
    ########################################
    def recognizeCharacters_RC(self):
    ########################################
        
        #Initialize return result 
        self.recogDll = cdll.LoadLibrary(r'D:\Temp\TA\MGB\RecogImage.dll')
        self.recogDll.recogImage_RC.restype = AudiResult_RC

        path = c_char_p(self.recogPath)
        trasCharacter = self.recogConfig.encode('utf-8')
        result = c_char_p(trasCharacter)
        num = c_int(len(trasCharacter))

        try:
            returnResult = self.recogDll.recogImage_RC(path, result, num)
        except Exception as e:
            print e.message + " Recognition failed"
        print "show me the result"
        print returnResult.result[0], returnResult.disL, returnResult.flag, returnResult.countNum
        return returnResult.result, returnResult.disL, returnResult.flag, returnResult.rect, returnResult.countNum
        print "Left is ", returnResult.rect.left
        print "Top is ", returnResult.rect.top
        print "Right is ", returnResult.rect.right
        print "Bottom is ", returnResult.rect.bottom


    #In this function use HanvonOCR to recognize the Chinese characters and get all information without checking
    ########################################
    def recognizeCharacters_AIn(self):
    ########################################
        
        #Initialize return result 
        self.recogDll = cdll.LoadLibrary(r'D:\Temp\TA\MGB\RecogImage.dll')
        self.recogDll.recogImage_AIn.restype = AudiResult_RC

        path = c_char_p(self.recogPath)

        try:
            returnResult = self.recogDll.recogImage_AIn(path)
        except Exception as e:
            print e.message + " Recognition failed"
        print "show me the result"
        print returnResult.result[0], returnResult.disL, returnResult.flag, returnResult.countNum
        return returnResult.result, returnResult.disL, returnResult.flag, returnResult.rect, returnResult.countNum

        
    ########################################
    def recognizeColor(self, blue, green , red):
    ########################################
        (B,G,R) = cv2.split(self.roi)
        print "###############################################"
        print np.mean(R), np.mean(G), np.mean(B)
        if np.mean(B) > blue[0] and np.mean(B) < blue[1] \
           and np.mean(G) > green[0] and np.mean(G) < green[1] \
           and np.mean(R) > red[0] and np.mean(R) < red[1]:
            return 1
        else:
            return 0

    #########################################
    def recognizeImage(self, iconName, minLikelihood=0.60):
    #########################################
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        imageGrey = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        iconGrey = cv2.imread(iconName, 0)
        
        print iconName
        
        method = cv2.TM_CCOEFF_NORMED
        h, w = iconGrey.shape[:2]
        res = cv2.matchTemplate(imageGrey, iconGrey, method)
        min_val, likelihood, min_loc, max_loc = cv2.minMaxLoc(res)
        #print "max_val:",max_val
        print likelihood, min_loc, max_loc
        

        if likelihood > minLikelihood:
            isFound = True
            print iconGrey[1], iconGrey[0]
            pos = max_loc[0], max_loc[1]
            center = pos[0] + w/2, pos[1] + h/2
        else:
            isFound = False
            Pos = None
            center = None
        print center
        return likelihood

        #imageColor = cv2.cvtColor(imageGrey, cv2.GRAY2RGB)
        cv2.circle(imageGrey, center, 20, (255, 0, 0), 2)
        cv2.imshow("imageGrey", imageGrey)
        #cv2.imshow("iconGrey", iconGrey)
        cv2.waitKey(0)
        
    #Get mask
    #########################################
    def getMask(self, maskPath):
    #########################################
        import xml.etree.ElementTree as ET

        #Parse the file and get the element you want
        tree = ET.parse(maskPath)
        root = tree.getroot()
        elements = root.find("ELEMENTS")
        element = elements.find("ELEMENT")

        offX = int(element.find("OffsetX").text)
        offY = int(element.find("OffsetY").text)

        width = int(element.find("SizeX").text)
        height = int(element.find("SizeY").text)

        mask = [offX, offY, width, height]

        return mask

if __name__ == "__main__":
    imagePath = r"D:\workspace\NavigationTA\SaveImage\GrabbedSingleFrame 2018_05_15__10_56_59_146000.png"
    maskPath = r"D:\workspace\NavigationTA\Config\Mask\FreeSearch.xml"
    recogPath = r"D:\workspace\NavigationTA\RecogImage\recogImage1.png"
    recogConfigPath = r"D:\Temp\TA\MGB\Config\RecogText.json"

    testImage = handleImage(imagePath, maskPath, recogPath, "ktv")
    testImage.greyROI()
    result, disL, flag, rect, countNum  = testImage.recognizeCharacters_RC()
    print "The result is###############################"
    print result
    
    for i in range(countNum):

        try:
            print result[i]
        except Exception as e:
            print "return result is wrong " + e.message
    
    result, disL, flag, rect, countNum  = testImage.recognizeCharacters_AIn()
    print "The result is###############################"
    print result
    
    
    for i in range(countNum):

        try:
            print result[i]
        except Exception as e:
            print "return result is wrong " + e.message
    
    
    #print testImage.mask

    '''
    testImage.greyROI()
    #testImage.recognizeCharacters()
    colorResult = testImage.recognizeColor()
    print colorResult

    testImage.recognizeImage(r"D:\Temp\TA\MGB\RecogImage\Flag.png")
    '''
                             
    

        
        
        
    
        
