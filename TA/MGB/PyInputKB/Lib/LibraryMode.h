#pragma once
#include <stdio.h>
#include <conio.h>
#include "AbtPlugin_impl.h"
#include <PlateauBasicLib.h>

class LibraryMode
{
public:
	LibraryMode();
	~LibraryMode();

#ifdef _WINDLL
	bool init(long serialNumber, long channel, long hardwareType, long useAudiConfig, long displayIndex, long touchProtocol = 0);
	bool deinit();
	bool pressCoord(long xCoord, long yCoord, long duration, long displayIndex, long UseForce = -1);
	bool dragCoord(long xCoordStart, long yCoordStart, long xCoordEnd, long yCoordEnd, long duration, long displayIndex, long UseForce = -1);
#endif

private:
	AbtPlugin_impl* pAbtImpl;
	log4cplus::Logger gLogger;
};