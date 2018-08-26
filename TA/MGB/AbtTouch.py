# -*- coding: utf-8 -*-
"""
Module for realizing abtplugin touch the screen.
"""
# coding: utf8
import ctypes
import os
import sys
import time

#===================
class CTouchScreen():
#===================
	"""
	Class CTouchScreen is to realize the fuction like init, deinit and touch screen
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
	characterPostion = {}
	
	#===========================
	def __init__(self, isVirtual=False):
	#===========================
		"""
		Load AbtPlugin library and write library directory
		"""
		
		self.isVirtual = isVirtual
		bSuccess = True
	
	#===========================
	def initParams(self, serialNumber, channel, hardwareType, displayIndex):
	#===========================
		"""
		init AbtPlugin -> set following parameter:
		*serialNumber*: serial number of CAN Case (MIB-CAN), if set to
		0 the first serial will be used
		*channel*: channel number of MIB-CAN
		*hardwareType*: CAN-Case hardware Type (e.g. CANCaseXL or CANCardXL, see constants)
		*displayIndex*: index of display which should be used (e.g. TOP or BOT) 
		"""
		if self.isVirtual:
			print "initialized"
			return True
		
		try:
			print "PyHID: init with serial nr:", serialNumber
			self.libabt = ctypes.cdll.LoadLibrary('AbtPlugin.dll')
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
		
		print "Initialization was successfull"
		return True
		

		 

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
	def touchScreen(self, xValue, yValue, duration=200, displayIndex=DISPLAY_TOP, forceUsage=1):
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
				forceValue = 99
				if forceUsage == 0:
						forceValue = -1
								
				self.libabt.pressCoord(self.instaceOfAbt, xValue, yValue, duration, displayIndex, forceValue)
		except KeyError:
				print "ERROR: character: " + character + " not available."
				bSuccess = False

		return bSuccess

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
	touch = CTouchScreen()
	if touch.initParams(26839, 1, touch.CANCaseXL, touch.DISPLAY_TOP):
		#touch.touchScreen(355, 155, 500, 1, 1)
		#time.sleep(1)

		touch.dragCoords(620,680,620,320)
		time.sleep(1)
		touch.dragCoords(620,680,620,660)
		
		
		touch.deinitParams()
		
	
	
	
