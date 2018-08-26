import cv2
import numpy as np
from ctypes import *

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
    _fields_ = [("blocks", POINTER(AudiBlock)),
                ("blockCount", c_int)]

    

class handleImage(object):
    '''
    In this class, the job is to
    handle the image such as getting the
    ROI image, grey image and recognizing
    the characters
    '''
    def __init__(self, imagePath, maskPath, recogPath):
        #Read the image
        self.img = cv2.imread(imagePath)
        self.mask = self.getMask(maskPath)
        self.recogPath = recogPath

    ##########################################
    #Get the ROI and Grey image
    def greyROI(self):
        
        offX = self.mask[0]
        width = offX + self.mask[2]
        print offX, width

        offY = self.mask[1]
        height = self.mask[3] + offY
        print offY, height
        
        roi = self.img[offY : height, offX : width]

        self.img2Grey = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        print self.img2Grey
        print type(self.img2Grey)

        #Save image for Hanvon recognition
        cv2.imwrite(self.recogPath, self.img2Grey)  

        '''
        cv2.imshow("res", self.img2Grey)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        '''

        '''
        fi = open('result.txt', 'w+')
        fi.write(self.img2Grey)
        '''
        
        self.recognizeImage()
        
    ########################################
    #In this function use HanvonOCR to recognize the Chinese characters
    def recognizeImage(self):
        
        size = self.img2Grey.shape
        imageSize = size[0] * size[1]
        #imageData = (c_ubyte * imageSize)()
        #imageData = (c_char * imageSize)()
   
        '''
        #Copy self.img2Grey data to new memory and change the
        #data to Char type
        for i in range(size[0]):
            for j in range(size[1]):
                #imageData[i * j + j] = chr(self.img2Grey[i][j])
                imageData[i * j + j] = self.img2Grey[i][j]      
        '''

        #print size[0], size[1]
        width = c_int(size[1])
        height =  c_int(size[0])

        #Initialize return result 
        self.recogDll = cdll.LoadLibrary(r'D:\Temp\TA\MGB\hwaudiocr.dll')
        self.recogDll.AudiRecognize.restype = POINTER(AudiResult)

        result = self.recogDll.AudiRecognize(imageData, width, height)
        print result

        '''
        for item in result:
            print item.blockCount
            if item.blockCount is None:
                break
        '''

        '''
        for i in range(result.contents.blockCount):
            print arst.contents.block[i].contents.text
        '''
        
    ########################################
    #Get mask
    def getMask(self, maskPath):       
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
    imagePath = r"D:\Temp\TA\MGB\SaveImage\GrabbedSingleFrame 2018_02_22__10_13_38_040000.png"
    maskPath = r"D:\Temp\TA\Mask\Admin_mask_Green_Row1.xml"
    recogPath = r"D:\Temp\TA\MGB\RecogImage\recogImage1.png"

    testImage = handleImage(imagePath, maskPath, recogPath)
    #print testImage.mask

    testImage.greyROI()

    

        
        
        
    
        
