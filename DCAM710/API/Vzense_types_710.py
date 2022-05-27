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
 
class PsVector3f(Structure):
    _pack_ = 1
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float)]  

class PsVector2u16(Structure):
    _pack_ = 1
    _fields_ = [("x", c_uint16),
                ("y", c_uint16)]  

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

class PsTimeStamp(Structure):
    _pack_ = 1       
    _fields_ = [("tm_sec", c_uint16),
                ("tm_min", c_uint16),
                ("tm_hour", c_uint16),
                ("tm_msec", c_uint16)]     

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
                ("height", c_uint16),
                ("timestamp", PsTimeStamp),
                ("hardwaretimestamp", c_uint64)]

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
                ("alias", c_char * 64),
                ("status", c_int32),
                ("ip", c_char * 16)]

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
 
class PsTalDelay(Structure):
    _pack_ = 1
    _fields_ = [("range", c_uint8),
                ("value0", c_uint16),
                ("value1", c_uint16),
                ("value2", c_uint16),
                ("value3", c_uint16),
                ("value4", c_uint16)]

class PsWDRPulseCount(Structure):
    _pack_ = 1
    _fields_ = [("pulseCount1", c_uint16),
                ("pulseCount2", c_uint16),
                ("pulseCount3", c_uint16),
                ("option", c_uint8)]

