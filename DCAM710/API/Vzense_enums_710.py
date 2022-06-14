import os, platform, numpy
from ctypes import *
from enum import Enum
 
class PsDepthRange(Enum):
    PsNearRange     = 0
    PsMidRange      = 1
    PsFarRange      = 2
    PsXNearRange    = 3
    PsXMidRange     = 4
    PsXFarRange     = 5
    PsXXNearRange   = 6
    PsXXMidRange    = 7
    PsXXFarRange    = 8
    PsUnknown       = -1

class PsDataMode(Enum):
    PsDepthAndRGB_30        = 0
    PsIRAndRGB_30           = 1
    PsDepthAndIR_30         = 2
    PsDepthAndIR_15_RGB_30  = 10
    PsWDR_Depth             = 11

class PsFrameType(Enum):
    PsDepthFrame       = 0     
    PsIRFrame          = 1        
    PsRGBFrame         = 3       
    PsMappedRGBFrame   = 4                       
    PsMappedDepthFrame = 5                      
    PsWDRDepthFrame    = 9     
        
class PsSensorType(Enum):
    PsDepthSensor = 0x01
    PsRgbSensor   = 0x02

class PsPixelFormat(Enum):
    PsPixelFormatDepthMM16 = 0
    PsPixelFormatGray16    = 1 
    PsPixelFormatGray8     = 2  
    PsPixelFormatRGB888    = 3  
    PsPixelFormatBGR888    = 4    

class PsReturnStatus(Enum):
    PsRetOK                         =  0
    PsRetNoDeviceConnected          = -1
    PsRetInvalidDeviceIndex         = -2
    PsRetDevicePointerIsNull        = -3
    PsRetInvalidFrameType           = -4
    PsRetFramePointerIsNull         = -5
    PsRetNoPropertyValueGet         = -6
    PsRetNoPropertyValueSet         = -7
    PsRetPropertyPointerIsNull      = -8
    PsRetPropertySizeNotEnough      = -9
    PsRetInvalidDepthRange          = -10
    PsRetReadNextFrameTimeOut       = -11
    PsRetInputPointerIsNull         = -12
    PsRetCameraNotOpened            = -13
    PsRetInvalidCameraType          = -14
    PsRetInvalidParams              = -15
    PsRetCurrentVersionNotSupport   = -16
    PsRetUpgradeImgError            = -17
    PsRetUpgradeImgPathTooLong      = -18
    PsRetUpgradeCallbackNotSet		= -19
    PsRetNoAdapterConnected			= -100
    PsRetReInitialized				= -101
    PsRetNoInitialized				= -102
    PsRetCameraOpened				= -103
    PsRetCmdError					= -104
    PsRetCmdSyncTimeOut				= -105
    PsRetOthers                     = -255

class PsWDRTotalRange(Enum):
    PsWDRTotalRange_Two   = 2
    PsWDRTotalRange_Three = 3

class PsWDRStyle(Enum):
    PsWDR_FUSION      = 0
    PsWDR_ALTERNATION = 1

class PsResolution(Enum):
    PsRGB_Resolution_1920_1080   = 0
    PsRGB_Resolution_1280_720    = 1
    PsRGB_Resolution_640_480     = 2
    PsRGB_Resolution_640_360     = 3

class PsConnectStatus(Enum):
    ConnectUNKNOWN   = 0
    Unconnected      = 1
    Connected        = 2
    Opened           = 3

class PsDeviceType(Enum):
	NONE           = 0
	DCAM305        = 305
	DCAM500        = 500
	CSI100	       = 501
	DCAM510        = 510
	DCAM550U       = 550
	DCAM550P       = 551
	DCAM550E       = 552
	DCAM560        = 560
	DCAM560CPRO    = 561
	DCAM560CLITE   = 562
	DCAM710        = 710
	DCAM800        = 800
	DCAM_MIPI      = 801
	DCAM800LITE    = 802
	DCAM800LITEUSB = 803
	DCAM101        = 804

 

