__version__ = "0.0.1"
__author__ = "peter.liu@picovr.com"
import os, platform, numpy
from ctypes import *
from enum import Enum

class PsRGB888Pixel(Structure):
    _pack_ = 1
    _fields_ = [("r", c_uint8),
                ("g", c_uint8),
                ("b", c_uint8)]
class PsBGR888Pixel(Structure):
    _pack_ = 1
    _fields_ = [("g", c_uint8),
                ("g", c_uint8),
                ("r", c_uint8)]
class PsFrameMode(Structure):
    _pack_ = 1
    _fields_ = [("pixelFormat", c_int32),
                ("resolutionWidth", c_int32),
                ("resolutionHeight", c_int32),
                ("fps", c_int32)]     
class PsVector3f(Structure):
    _pack_ = 1
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float)]  
class PsDepthVector3(Structure):
    _pack_ = 1
    _fields_ = [("depthX", c_int),
                ("depthY", c_int),
                ("depthZ", c_uint16)] 
class PsCameraParameters(Structure):
    _pack_ = 1
    _fields_ = [("fx", c_double),
                ("fy", c_double),
                ("cx", c_double),
                ("cy", c_double),
                ("k1", c_double),
                ("k2", c_double),
                ("p1", c_double),
                ("p2", c_double),
                ("k3", c_double),
                ("k4", c_double),
                ("k5", c_double),
                ("k6", c_double)] 
class PsCameraExtrinsicParameters(Structure):
    _pack_ = 1
    _fields_ = [("rotation", c_double * 9),
                ("translation", c_double * 3)]  
class PsFrame(Structure):
    _pack_ = 1
    _fields_ = [("frameIndex", c_uint32),
                ("frameType", c_int32),
                ("pixelFormat", c_int32),
                ("imuFrameNo", c_uint8),
                ("pFrameData", POINTER(c_uint8)),
                ("dataLen", c_uint32),
                ("exposureTime", c_float),
                ("depthRange", c_int32),
                ("width", c_uint16),
                ("height", c_uint16)]
class PsWDROutputMode(Structure):
    _pack_ = 1
    _fields_ = [("totalRange", c_int32),
                ("range1", c_int32),
                ("range1Count", c_uint8),
                ("range2", c_int32),
                ("range2Count", c_uint8),
                ("range3", c_int32),
                ("range3Count", c_uint8)]
class PsGMMGain(Structure):
    _pack_ = 1
    _fields_ = [("gain", c_uint16),
                ("option", c_uint8)]  
class PsFrameReady(Structure):
    _pack_ = 1
    _fields_ = [("depth", c_uint, 1),
                ("ir", c_uint, 1),
                ("rgb", c_uint, 1),
                ("mappedRGB", c_uint, 1),
                ("mappedDepth", c_uint, 1),
                ("mappedIR", c_uint, 1),
                ("confidence", c_uint, 1),
                ("wdrDepth", c_uint, 1),
                ("reserved", c_uint, 24)]

class PsDeviceInfo(Structure):
    _pack_ = 1
    _fields_ = [("SessionCount", c_int),
                ("devicetype", c_int32),
                ("uri", c_char * 256),
                ("fw", c_char * 50),
                ("status", c_int32)]

class PsDataModeList(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint8),
                ("count", c_uint8),
                ("datamodelist", c_uint8 * 32)]
class PsDepthRangeList(Structure):
    _pack_ = 1
    _fields_ = [("index", c_uint8),
                ("count", c_uint8),
                ("depthrangelist", c_uint8 * 9)]
class PsMeasuringRange(Structure):
    _pack_ = 1
    _fields_ = [("depthMode", c_uint8),
                ("depthMaxNear", c_uint16),
                ("depthMaxMid", c_uint16),
                ("depthMaxFar", c_uint16),
                ("effectDepthMaxNear", c_uint16),
                ("effectDepthMaxMid", c_uint16),
                ("effectDepthMaxFar", c_uint16),
                ("effectDepthMinNear", c_uint16),
                ("effectDepthMinMid", c_uint16),
                ("effectDepthMinFar", c_uint16)]

class DataMode(Enum):
    DEPTH_AND_RGB_30        = 0
    IR_AND_RGB_30           = 1
    DEPTH_AND_IR_30         = 2
    DEPTH_AND_IR_15_RGB_30  = 10
    STANDBY                 = 102
class FrameType(Enum):
    DEPTH_FRAME         = 0
    IR_FRAME            = 1
    RGB_FRAME           = 3
    MAPPED_RGB_FRAME    = 4
    MAPPED_DEPTH_FRAME  = 5
    MAPPED_IR_FRAME     = 6
class DepthRange(Enum):
	NEAR_Range      = 0
	MID_Range       = 1
	FAR_Range       = 2
	XNEAR_Range     = 3
	XMID_Range      = 4
	XFAR_Range      = 5
	XXNEAR_Range    = 6
	XXMID_Range     = 7
	XXFAR_Range     = 8
class RGBResolution(Enum):
    RGB_Resolution_1920_1080   = 0
    RGB_Resolution_1280_720    = 1
    RGB_Resolution_640_480     = 2
    RGB_Resolution_640_360     = 3


class PicoTofCam():
    psframe = PsFrame()
    device_handle = c_int64(0)
    frame = numpy.zeros((480, 640), dtype = numpy.uint16, order = 'C')

    def __init__(self):
        if platform.system() == 'Linux':
            self.ps_cam_lib = cdll.LoadLibrary('./linux_lib/libvzense_api.so')
        elif platform.system() == 'Windows':
            lib_name = "windows_lib"
            lib_path = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + lib_name
            lib_path = ';'+lib_path
            os.environ['path']+= lib_path
            self.ps_cam_lib = cdll.LoadLibrary('vzense_api.dll')
        else:
            print('do not supported OS')
            exit()
        
        self.ps_cam_lib.Ps2_Initialize()
    def __del__(self):
        if self.device_handle != 0:
            self.ps_cam_lib.Ps2_CloseDevice(self.device_handle)
        self.ps_cam_lib.Ps2_Shutdown()
    def get_cam_count(self):
        count = c_int()
        self.ps_cam_lib.Ps2_GetDeviceCount(byref(count))
        return count.value
    def get_cam_info(self, cam_index = 0):
        device_info = PsDeviceInfo()
        rst = self.ps_cam_lib.Ps2_GetDeviceInfo(byref(device_info), cam_index)
        if rst == 0:
            return device_info.uri
        else:
            return 'null'
    def open_cam(self, cam_index = 0):
        device_info = PsDeviceInfo()
        self.ps_cam_lib.Ps2_GetDeviceInfo(byref(device_info), cam_index)
        rst = self.ps_cam_lib.Ps2_OpenDevice(device_info.uri, byref(self.device_handle))
        if rst == 0:
            return 'success', self.device_handle
        else:
            return 'fail', 0
    def close_cam(self, handle):
        if handle != 0 and handle == self.device_handle:
            self.ps_cam_lib.Ps2_CloseDevice(handle)
            self.device_handle = 0
    def start_stream(self, handle, session = 0):
        rst = self.ps_cam_lib.Ps2_StartStream(handle, session)
        if rst == 0:
            return 'success'
        else:
            return 'fail'
    def stop_stream(self, handle, session = 0):
        rst = self.ps_cam_lib.Ps2_StopStream(handle, session)
        if rst == 0:
            return 'success'
        else:
            return 'fail'
    def read_next_frame(self, handle, session = 0):
        frameready = PsFrameReady()
        rst = self.ps_cam_lib.Ps2_ReadNextFrame(handle, session, byref(frameready))
        return frameready
    def get_frame(self, handle, session = 0, frametype = FrameType.DEPTH_FRAME):
        rst = self.ps_cam_lib.Ps2_GetFrame(handle, session, frametype.value, byref(self.psframe))
        if rst == 0: 
            if self.psframe.frameType == FrameType.DEPTH_FRAME.value: #or self.psframe.frameType == FrameType.IR_FRAME.value:
                frametmp = numpy.ctypeslib.as_array(self.psframe.pFrameData, (1, self.psframe.width * self.psframe.height * 2))
                frametmp.dtype = numpy.uint16
                frametmp.shape = (480, 640)
                self.frame = frametmp.copy()
                return 'success', self.frame, self.psframe.width,self.psframe.height
            elif self.psframe.frameType == FrameType.RGB_FRAME.value:
                frametmp = numpy.ctypeslib.as_array(self.psframe.pFrameData, (1, self.psframe.width * self.psframe.height * 3))
                frametmp.dtype = numpy.uint8
                frametmp.shape = (self.psframe.height, self.psframe.width, 3)
                self.frame = frametmp.copy()
                return 'success', self.frame, self.psframe.width,self.psframe.height
            elif self.psframe.frameType == FrameType.IR_FRAME.value:
                frametmp = numpy.ctypeslib.as_array(self.psframe.pFrameData, (1, self.psframe.width * self.psframe.height * 2))
                frametmp.dtype = numpy.uint16
                frametmp.shape = (480, 640)
                self.frame = frametmp.copy()
                return 'success', self.frame, self.psframe.width,self.psframe.height
            else:
                return 'fail', 0, 0, 0
        else:
            return 'fail', 0, 0, 0
    def set_data_mode(self, handle, session = 0, datamode = DataMode.DEPTH_AND_RGB_30):
        rst = self.ps_cam_lib.Ps2_SetDataMode(handle, session, datamode.value)
        if rst == 0:
            return 'success'
        else:
            return 'fail'
    def get_data_mode(self,handle, session = 0):
        datamode = c_int(0)
        rst = self.ps_cam_lib.Ps2_GetDataMode(handle, session, byref(datamode))
        if rst == 0:
            return 'success', DataMode(datamode.value)
        else:
            return 'fail', 0
    def get_measuring_range(self, handle, session = 0, range = DepthRange.NEAR_Range):
        MeasuringRange = PsMeasuringRange()
        rst = self.ps_cam_lib.Ps2_GetMeasuringRange(handle, session, range.value, byref(MeasuringRange))
        if rst == 0:
            if range == DepthRange.NEAR_Range or range == DepthRange.XNEAR_Range or range == DepthRange.XXNEAR_Range:
                return MeasuringRange.depthMaxNear, MeasuringRange.effectDepthMinNear, MeasuringRange.effectDepthMaxNear
            elif range == DepthRange.MID_Range or range == DepthRange.XMID_Range or range == DepthRange.XXMID_Range:
                return MeasuringRange.depthMaxMid, MeasuringRange.effectDepthMinMid, MeasuringRange.effectDepthMaxMid
            elif range == DepthRange.FAR_Range or range == DepthRange.XFAR_Range or range == DepthRange.XXFAR_Range:
                return MeasuringRange.depthMaxFar, MeasuringRange.effectDepthMinFar, MeasuringRange.effectDepthMaxFar
    def get_threshold(self, handle, session = 0):
        thres = c_uint16(20)
        self.ps_cam_lib.Ps2_GetThreshold(handle, session, byref(thres))
        return thres.value
    def get_pulsecnt(self, handle, session = 0):
        pulsecnt = c_uint16(20)
        self.ps_cam_lib.Ps2_GetPulseCount(handle, session, byref(pulsecnt))
        return pulsecnt.value
    def set_rgb_resolution(self, handle, session, resolution = RGBResolution.RGB_Resolution_640_360):
        rst = self.ps_cam_lib.Ps2_SetRGBResolution(handle, session, resolution.value)
        if rst == 0:
            return 'success'
        else:
            return 'fail'
    def set_depth_range(self, handle, session, range = DepthRange.NEAR_Range):
        rst = self.ps_cam_lib.Ps2_SetDepthRange(handle, session, range.value)
        if rst == 0:
            return 'success'
        else:
            return 'fail'





