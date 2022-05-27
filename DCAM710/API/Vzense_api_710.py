from DCAM710.API.Vzense_define_710 import * 
import sys, os
import ctypes
from ctypes import *
gCallbackFuncList=[]

class VzenseTofCam():
    device_handle = c_void_p(0)
    session = c_uint(0)
    def __init__(self):
        if platform.system() == 'Linux':
            libpath = (os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + "../../"))+"/Lib/libvzense_api.so"
            print(libpath)
            self.ps_cam_lib = cdll.LoadLibrary(libpath)
        elif platform.system() == 'Windows':          
            lib_name = "../../Lib/"
            lib_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + lib_name
            lib_path = ';'+lib_path
            os.environ['path']+= lib_path
            
            libpath = (os.path.abspath(os.path.dirname(os.getcwd()) + os.path.sep + "../../"))+"/Lib/vzense_api.dll"
            print(libpath)
            self.ps_cam_lib = cdll.LoadLibrary(libpath)    
        else:
            print('do not supported OS')
            exit()
            
        self.device_handle = c_void_p(0)
        self.session = c_uint(0)
        self.ps_cam_lib.Ps2_Initialize()

    def __del__(self):
        self.ps_cam_lib.Ps2_Shutdown()
    
    def Ps2_GetDeviceCount(self):
        count = c_int()
        self.ps_cam_lib.Ps2_GetDeviceCount(byref(count))
        return count.value
    
    def Ps2_GetDeviceListInfo(self, cam_count = 1):
        tmp  = PsDeviceInfo* cam_count
        device_infolist = tmp() 
        return self.ps_cam_lib.Ps2_GetDeviceListInfo(device_infolist, cam_count),device_infolist
    
    def Ps2_GetDeviceInfo(self, cam_index = 0):
        device_info = PsDeviceInfo()
        return self.ps_cam_lib.Ps2_GetDeviceInfo(byref(device_info), cam_index), device_info
         
    def Ps2_OpenDevice(self,  uri=c_char_p()):
        if uri:
            return self.ps_cam_lib.Ps2_OpenDevice(uri, byref(self.device_handle))
        else:
            return PsReturnStatus.PsRetInputPointerIsNull
    
    def Ps2_CloseDevice(self):
        return self.ps_cam_lib.Ps2_CloseDevice(byref(self.device_handle))

    def Ps2_StartStream(self):
        return self.ps_cam_lib.Ps2_StartStream(self.device_handle, self.session)
         
    def Ps2_StopStream(self):
        return self.ps_cam_lib.Ps2_StopStream(self.device_handle, self.session)
         
    def Ps2_ReadNextFrame(self):
        frameready = PsFrameReady()
        return self.ps_cam_lib.Ps2_ReadNextFrame(self.device_handle, self.session, byref(frameready)), frameready

    def Ps2_GetFrame(self,  frametype = PsFrameType.PsDepthFrame):   
        psframe = PsFrame() 
        return self.ps_cam_lib.Ps2_GetFrame(self.device_handle, self.session, frametype.value, byref(psframe)), psframe
    
    def Ps2_SetDataMode(self,  datamode = PsDataMode.PsDepthAndRGB_30):
        return self.ps_cam_lib.Ps2_SetDataMode(self.device_handle, self.session, datamode.value)
         
    def Ps2_GetDataMode(self):
        datamode = c_int(0)
        return self.ps_cam_lib.Ps2_GetDataMode(self.device_handle, self.session, byref(datamode)), datamode
    
    def Ps2_SetDepthRange(self,  depthrange = PsDepthRange.PsNearRange):
        return self.ps_cam_lib.Ps2_SetDepthRange(self.device_handle, self.session, depthrange.value) 
       
    def Ps2_GetDepthRange(self):
        depthrange = c_int(0)
        return self.ps_cam_lib.Ps2_GetDepthRange(self.device_handle, self.session, byref(depthrange)), depthrange

    def Ps2_SetThreshold(self,  threshold = c_uint16(20)):
        return self.ps_cam_lib.Ps2_SetThreshold(self.device_handle, self.session, threshold) 
               
    def Ps2_GetThreshold(self):
        thres = c_uint16()
        return self.ps_cam_lib.Ps2_GetThreshold(self.device_handle, self.session, byref(thres)), thres.value

    def Ps2_SetPulseCount(self,  pulsecount = c_uint16(20)):
        return self.ps_cam_lib.Ps2_SetPulseCount(self.device_handle, self.session, pulsecount) 
     
    def Ps2_GetPulseCount(self):
        pulsecount = c_uint16()
        return self.ps_cam_lib.Ps2_GetPulseCount(self.device_handle, self.session, byref(pulsecount)), pulsecount.value
    
    def Ps2_SetGMMGain(self, gmmgain = c_uint16(20)):
        gmmgain_ = PsGMMGain()
        gmmgain_.gmmgain = gmmgain
        gmmgain_.option = 0
        return self.ps_cam_lib.Ps2_SetGMMGain(self.device_handle, self.session, gmmgain_) 
     
    def Ps2_GetGMMGain(self):
        gmmgain = c_uint16(1)
        return self.ps_cam_lib.Ps2_GetGMMGain(self.device_handle, self.session, byref(gmmgain)), gmmgain

    def Ps2_GetCameraParameters(self, sensorType = PsSensorType.PsDepthSensor):
        CameraParameters = PsCameraParameters()
        return self.ps_cam_lib.Ps2_GetCameraParameters(self.device_handle, self.session, sensorType.value, byref(CameraParameters)), CameraParameters

    def Ps2_GetCameraExtrinsicParameters(self):
        CameraExtrinsicParameters = PsCameraExtrinsicParameters()
        return self.ps_cam_lib.Ps2_GetCameraExtrinsicParameters(self.device_handle, self.session, byref(CameraExtrinsicParameters)), CameraExtrinsicParameters
           
    def Ps2_SetColorPixelFormat(self, pixelFormat = PsPixelFormat.PsPixelFormatBGR888):
        return self.ps_cam_lib.Ps2_SetColorPixelFormat(self.device_handle, self.session, pixelFormat.value) 
       
    def Ps2_SetRGBResolution(self, resolution = PsResolution.PsRGB_Resolution_640_480):
        return self.ps_cam_lib.Ps2_SetRGBResolution(self.device_handle, self.session, resolution.value) 
     
    def  Ps2_GetRGBResolution(self):
        resolution = c_int(0)
        return self.ps_cam_lib.Ps2_GetRGBResolution(self.device_handle, self.session, byref(resolution)), resolution

    def Ps2_SetWDROutputMode(self, WDRMode = PsWDROutputMode()):
        return self.ps_cam_lib.Ps2_SetWDROutputMode(self.device_handle, self.session, byref(WDRMode)) 
     
    def Ps2_GetWDROutputMode(self):
        WDRMode = PsWDROutputMode()
        return self.ps_cam_lib.Ps2_GetWDROutputMode(self.device_handle, self.session, byref(WDRMode)), WDRMode

    def Ps2_SetWDRStyle(self, wdrStyle = PsWDRStyle.PsWDR_FUSION):
        return self.ps_cam_lib.Ps2_SetWDRStyle(self.device_handle, self.session, wdrStyle.value) 
                
    def Ps2_GetMeasuringRange(self,  range = PsDepthRange.PsNearRange):
        MeasuringRange = PsMeasuringRange()
        rst = self.ps_cam_lib.Ps2_GetMeasuringRange(self.device_handle, self.session, range.value, byref(MeasuringRange))
        if rst == 0:
            if range == PsDepthRange.PsNearRange or range == PsDepthRange.PsXNearRange or range == PsDepthRange.PsXXNearRange:
                return rst, MeasuringRange.depthMaxNear, MeasuringRange.effectDepthMinNear, MeasuringRange.effectDepthMaxNear
            elif range == PsDepthRange.PsMidRange or range == PsDepthRange.PsXMidRange or range == PsDepthRange.PsXXMidRange:
                return rst, MeasuringRange.depthMaxMid, MeasuringRange.effectDepthMinMid, MeasuringRange.effectDepthMaxMid
            elif range == PsDepthRange.PsFarRange or range == PsDepthRange.PsXFarRange or range == PsDepthRange.PsXXFarRange:
                return rst, MeasuringRange.depthMaxFar, MeasuringRange.effectDepthMinFar, MeasuringRange.effectDepthMaxFar
        else:
            return rst, 0, 0, 0

    def Ps2_ConvertDepthFrameToWorldVector(self, depthFrame = PsFrame()): 
        len = depthFrame.width*depthFrame.height
        tmp =PsVector3f*len
        pointlist = tmp()
        return self.ps_cam_lib.Ps2_ConvertDepthFrameToWorldVector(self.device_handle, self.session, depthFrame,pointlist),pointlist

    def Ps2_SetSynchronizeEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetSynchronizeEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetSynchronizeEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetSynchronizeEnabled(self.device_handle, self.session, byref(enabled)),enabled
    
    def Ps2_SetDepthDistortionCorrectionEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetDepthDistortionCorrectionEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetDepthDistortionCorrectionEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetDepthDistortionCorrectionEnabled(self.device_handle, self.session, byref(enabled)),enabled
    
    def Ps2_SetRGBDistortionCorrectionEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetRGBDistortionCorrectionEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetRGBDistortionCorrectionEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetRGBDistortionCorrectionEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetComputeRealDepthCorrectionEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetComputeRealDepthCorrectionEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetComputeRealDepthCorrectionEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetSpatialFilterEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetSpatialFilterEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetSpatialFilterEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetSpatialFilterEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetTimeFilterEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetTimeFilterEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetTimeFilterEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetTimeFilterEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetDepthFrameEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetDepthFrameEnabled(self.device_handle, self.session, enabled)

    def Ps2_SetIrFrameEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetIrFrameEnabled(self.device_handle, self.session, enabled)

    def Ps2_SetRgbFrameEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetRgbFrameEnabled(self.device_handle, self.session, enabled)

    def Ps2_SetImageMirror(self, type = c_int32(0)): 
        return self.ps_cam_lib.Ps2_SetImageMirror(self.device_handle, self.session, type)
    
    def Ps2_SetImageRotation(self, type = c_int32(0)): 
        return self.ps_cam_lib.Ps2_SetImageRotation(self.device_handle, self.session, type)
    
    def Ps2_SetMapperEnabledDepthToRGB(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetMapperEnabledDepthToRGB(self.device_handle, self.session, enabled)
    
    def Ps2_GetMapperEnabledDepthToRGB(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetMapperEnabledDepthToRGB(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetMapperEnabledRGBToDepth(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetMapperEnabledRGBToDepth(self.device_handle, self.session, enabled)
    
    def Ps2_GetMapperEnabledRGBToDepth(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetMapperEnabledRGBToDepth(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetHotPlugStatusCallback(self,callbackfunc= c_void_p): 
        callbackFunc_= ctypes.CFUNCTYPE(c_void_p,POINTER(PsDeviceInfo),c_int32)(callbackfunc)    
        gCallbackFuncList.append(callbackFunc_)
        return self.ps_cam_lib.Ps2_SetHotPlugStatusCallback(callbackFunc_)

    def Ps2_SetWDRPulseCount(self,wdrpulseCount = PsWDRPulseCount()): 
        return self.ps_cam_lib.Ps2_SetWDRPulseCount(self.device_handle, self.session, wdrpulseCount)

    def Ps2_GetWDRPulseCount(self): 
        wdrpulseCount = PsWDRPulseCount()
        return self.ps_cam_lib.Ps2_GetWDRPulseCount(self.device_handle, self.session, byref(wdrpulseCount)),wdrpulseCount

    def Ps2_GetSerialNumber(self): 
        tmp = c_char * 64
        sn = tmp()
        return self.ps_cam_lib.Ps2_GetSerialNumber(self.device_handle, self.session, sn, 63),sn.value

    def Ps2_GetFirmwareVersionNumber(self): 
        tmp = c_char * 64
        fw = tmp()
        return self.ps_cam_lib.Ps2_GetFirmwareVersionNumber(self.device_handle, self.session, fw, 63),fw.value

    def Ps2_SetDSPEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetDSPEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_GetDSPEnabled(self): 
        enabled = c_bool(True)
        return self.ps_cam_lib.Ps2_GetDSPEnabled(self.device_handle, self.session, byref(enabled)),enabled

    def Ps2_SetSlaveModeEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetSlaveModeEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_SetTofFrameRate(self, rate = c_uint8(30)): 
        return self.ps_cam_lib.Ps2_SetTofFrameRate(self.device_handle, self.session, rate)
    
    def Ps2_GetTofFrameRate(self): 
        rate = c_uint8(30)
        return self.ps_cam_lib.Ps2_GetTofFrameRate(self.device_handle, self.session, byref(rate)),rate

    def Ps2_SetStandByEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetStandByEnabled(self.device_handle, self.session, enabled)
    
    def Ps2_OpenDeviceByAlias(self,  alias=c_char_p()):
        if alias:
            return self.ps_cam_lib.Ps2_OpenDeviceByAlias(alias, byref(self.device_handle))
        else:
            return PsReturnStatus.PsRetInputPointerIsNull
    
    def Ps2_SetWaitTimeOfReadNextFrame(self, time = c_uint16(33)): 
        return self.ps_cam_lib.Ps2_SetWaitTimeOfReadNextFrame(self.device_handle, self.session, time)
    
    def Ps2_GetSDKVersion(self): 
        tmp = c_char * 64
        version = tmp()
        return self.ps_cam_lib.Ps2_GetSDKVersion(version, 63),version.value
 
    def Ps2_GetMappedPointDepthToRGB(self, depthPoint = PsDepthVector3(),rgbSize = PsVector2u16(640,480)): 
        PosInRGB = PsVector2u16()
        return self.ps_cam_lib.Ps2_GetMappedPointDepthToRGB(self.device_handle, self.session, depthPoint, rgbSize, byref(PosInRGB)),PosInRGB

    def Ps2_RebootCamera(self): 
        return self.ps_cam_lib.Ps2_RebootCamera(self.device_handle, self.session)

    def Ps2_SetLegacyAlgorithmicEnabled(self, enabled = c_bool(True)): 
        return self.ps_cam_lib.Ps2_SetLegacyAlgorithmicEnabled(self.device_handle, self.session, enabled)
     
 



 














