from pickle import FALSE, TRUE
import sys
sys.path.append('../../../')

from DCAM550.API.Vzense_api_550 import *
import cv2
import time

camera = VzenseTofCam()


def HotPlugStateCallback(type_struct,  state = c_int32(0)):
    print("callback done")
    print(str(type_struct.contents.alias) + "   "+str(state))

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

if  ret == 0:
    while 1:
        time.sleep(1)
        continue
else:
    print('Ps2_OpenDevice failed: ' + str(ret))  

ret = camera.Ps2_CloseDevice()     
if  ret == 0:
    print("close device successful")
else:
    print('Ps2_CloseDevice failed: ' + str(ret))   
                       
