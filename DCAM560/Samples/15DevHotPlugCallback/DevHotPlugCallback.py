from pickle import FALSE, TRUE
import sys
sys.path.append('../../../')

from DCAM560.API.Vzense_api_560 import *
import time

camera = VzenseTofCam()


def HotPlugStateCallback(type_struct,  state = c_int32(0)):
    global camera
    if state ==0:
        print(str(type_struct.contents.alias) + "   add")
        ret = camera.Ps2_OpenDevice(type_struct.contents.uri)
        if  ret == 0:
            print(str(type_struct.contents.alias) + " open success")
        else:
            print(str(type_struct.contents.alias) + " open failed",ret)
        ret = camera.Ps2_StartStream()
        if  ret == 0:
            print(str(type_struct.contents.alias) + " startstream success")
        else:
            print(str(type_struct.contents.alias) + " startstream failed",ret)
    else:
        print(str(type_struct.contents.alias) + "   remove")
        ret = camera.Ps2_StopStream()
        if  ret == 0:
            print(str(type_struct.contents.alias) + " stopstream success")
        else:
            print(str(type_struct.contents.alias) + " stopstream failed",ret)
        ret = camera.Ps2_CloseDevice()
        if  ret == 0:
            print(str(type_struct.contents.alias) + " close success")
        else:
            print(str(type_struct.contents.alias) + " close failed",ret)

camera.Ps2_SetHotPlugStatusCallback(HotPlugStateCallback)

camera_count = camera.Ps2_GetDeviceCount()
retry_count = 100
while camera_count==0 and retry_count > 0:
    retry_count = retry_count-1
    camera_count = camera.Ps2_GetDeviceCount()
    time.sleep(1)
    print("scaning......   ",retry_count)

device_info=PsDeviceInfo()

if camera_count > 1:
    ret,device_infolist=camera.Ps2_GetDeviceListInfo(camera_count)
    if ret==0:
        device_info = device_infolist[0]
        for info in device_infolist: 
            print('cam uri:  ' + str(info.uri))
    else:
        print(' failed:' + ret)  
        exit()  
elif camera_count == 1:
    ret,device_info=camera.Ps2_GetDeviceInfo()
    if ret==0:
        print('cam uri:' + str(device_info.uri))
    else:
        print(' failed:' + ret)   
        exit() 
else: 
    print("there are no camera found")
    exit()

print("uri: "+str(device_info.uri))
ret = camera.Ps2_OpenDevice(device_info.uri)

if  ret == 0 or ret == -103:
    ret = camera.Ps2_StartStream()
    if  ret == 0:
        print("startstream success")
    else:
        print("startstream failed",ret)

    while 1:
        ret, frameready = camera.Ps2_ReadNextFrame()
        if  ret !=0:
            print("Ps2_ReadNextFrame failed:",ret)
            time.sleep(1)
            continue
  
        if  frameready.depth:      
            ret,frame = camera.Ps2_GetFrame(PsFrameType.PsDepthFrame)
            if  ret ==0:
                print("frameIndex: ",frame.frameIndex)
            else:
                print("get depth frame failed ",ret)
            time.sleep(1)
            continue
else:
    print('Ps2_OpenDevice failed: ' + str(ret))  

ret = camera.Ps2_StopStream()
if  ret == 0:
    print("stopstream success")
else:
    print("stopstream failed",ret)

ret = camera.Ps2_CloseDevice()     
if  ret == 0:
    print("close device successful")
else:
    print('Ps2_CloseDevice failed: ' + str(ret))   
                       
