from pickle import FALSE, TRUE
import sys
sys.path.append('../../../')

from DCAM710.API.Vzense_api_710 import *
import cv2
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
            print("open device successful")
            cameras.append(cam)
        else:
            print('Ps2_OpenDevice failed: ' + str(ret))    
else:
    print(' failed:' + ret)  
    exit()  

for i in range(camera_count): 
    ret = cameras[i].Ps2_StartStream()       
    if  ret == 0:
        print("start stream successful")
    else:
        print('Ps2_StartStream failed: ' + str(ret))  

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
 
                frametmp = numpy.ctypeslib.as_array(depthframe.pFrameData, (1, depthframe.width * depthframe.height * 2))
                frametmp.dtype = numpy.uint16
                frametmp.shape = (depthframe.height, depthframe.width)
                
                #convert ushort value to 0xff is just for display
                img = numpy.int32(frametmp)
                img = img*255/6000
                img = numpy.clip(img, 0, 255)
                img = numpy.uint8(img)
                frametmp = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
                if 0==i:
                    cv2.imshow("depthimage", frametmp)
                if 1==i:
                    cv2.imshow("depthimage1", frametmp)
            else:
                print("Ps2_GetFrame error", ret)
        if  frameready.ir:
            ret,irframe = cameras[i].Ps2_GetFrame(PsFrameType.PsIRFrame)
            if  ret == 0:
                frametmp = numpy.ctypeslib.as_array(irframe.pFrameData, (1, irframe.width * irframe.height * 2))
                frametmp.dtype = numpy.uint16
                frametmp.shape = (irframe.height, irframe.width)
                img = numpy.int32(frametmp)
                img = img*255/3840
                img = numpy.clip(img, 0, 255)
                irframe = numpy.uint8(img)
                if 0==i:
                    cv2.imshow("irimage", frametmp)
                if 1==i:
                    cv2.imshow("irimag1", frametmp)
            else:
                print("Ps2_GetFrame error", ret)

    key = cv2.waitKey(1)
    if  key == 27:
        cv2.destroyAllWindows()
        print("---end---")
        exit()

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
    
           