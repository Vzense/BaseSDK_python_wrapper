from pickle import FALSE, TRUE
import sys
sys.path.append('../../../')

from DCAM560.API.Vzense_api_560 import *
import time

camera = VzenseTofCam()


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

if  PsConnectStatus.Connected.value != device_info.status:
	print("connect statu:",device_info.status)  
	print("Call Ps2_OpenDevice with connect status :",PsConnectStatus.Connected.value)
	exit()
else:
    print("uri: "+str(device_info.uri))
    print("alias: "+str(device_info.alias))
    print("connectStatus: "+str(device_info.status))

ret = camera.Ps2_OpenDevice(device_info.uri)
if  ret == 0:
    print("open device successful")
else:
    print('Ps2_OpenDevice failed: ' + str(ret))   
            
ret = camera.Ps2_CloseDevice()   
if  ret == 0:
    print("close device successful")
else:
    print('Ps2_CloseDevice failed: ' + str(ret))   
           