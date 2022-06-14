from pickle import FALSE, TRUE
import sys
sys.path.append('../../../')

from DCAM550.API.Vzense_api_550 import *
import time

camera = VzenseTofCam()


camera_count = camera.Ps2_GetDeviceCount()
retry_count = 100
while camera_count < 2 and retry_count > 0:
    retry_count = retry_count-1
    camera_count = camera.Ps2_GetDeviceCount()
    time.sleep(1)
    print("scaning......   ",retry_count)


if camera_count < 2: 
    print("there are no camera or only on camera")
    exit()
 
cameras = []

ret, device_infolist=camera.Ps2_GetDeviceListInfo(camera_count)
if ret==0:
    for i in range(camera_count): 
        print('cam uri:  ' + str(device_infolist[i].uri))
        cam = VzenseTofCam()
        ret = cam.Ps2_OpenDevice(device_infolist[i].uri)
        if  ret == 0:
            print(device_infolist[i].alias,"open successful")
            cameras.append(cam)
        else:
            print(device_infolist[i].alias,'Ps2_OpenDevice failed: ' + str(ret))    
else:
    print(' failed:' + ret)  
    exit()  

for i in range(camera_count): 
    ret = cameras[i].Ps2_StartStream()       
    if  ret == 0:
        print(device_infolist[i].alias,"start stream successful")
    else:
        print(device_infolist[i].alias,'Ps2_StartStream failed: ' + str(ret))  

# show image 

while 1:
    for i in range(camera_count): 
        ret, frameready = cameras[i].Ps2_ReadNextFrame()   
        if  ret !=0:
            print("Ps2_ReadNextFrame failed:",ret)
            time.sleep(1)
            continue
                        
        if  frameready.depth:      
            ret,depthframe = cameras[i].Ps2_GetFrame(PsFrameType.PsDepthFrame)
            if  ret == 0:
                print(device_infolist[i].alias,"  depth frameindex: ",depthframe.frameIndex)
            else:
                print("Ps2_GetFrame error", ret)
        if  frameready.ir:
            ret,irframe = cameras[i].Ps2_GetFrame(PsFrameType.PsIRFrame)
            if  ret == 0:
                print(device_infolist[i].alias,"  ir frameindex: ",irframe.frameIndex)
            else:
                print("Ps2_GetFrame error", ret)

for i in range(camera_count): 
    
    ret = cameras[i].Ps2_StopStream()       
    if  ret == 0:
        print("stop stream successful")
    else:
        print('Ps2_StopStream failed: ' + str(ret))  

    ret = cameras[i].Ps2_CloseDevice()       
    if  ret == 0:
        print("close device successful")
    else:
        print('Ps2_CloseDevice failed: ' + str(ret))  
    
           