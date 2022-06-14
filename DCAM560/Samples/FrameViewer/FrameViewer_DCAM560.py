from pickle import FALSE, TRUE
import sys
sys.path.append('../../../')

from DCAM560.API.Vzense_api_560 import *
import cv2
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

print("uri: "+str(device_info.uri))
ret = camera.Ps2_OpenDevice(device_info.uri)

if  ret == 0:

    ret = camera.Ps2_StartStream()
    if  ret == 0:
        print("start stream successful")
    else:
        print("Ps2_StartStream failed:",ret)

    ret, depthrange = camera.Ps2_GetDepthRange()
    if  ret == 0:
        print("Ps2_GetDepthRange :",depthrange.value)
    else:
        print("Ps2_GetDepthRange failed:",ret)

    ret, depth_max, value_min, value_max = camera.Ps2_GetMeasuringRange(PsDepthRange(depthrange.value))
    if  ret == 0:
        print("Ps2_GetMeasuringRange: ",depth_max,",",value_min,",",value_max)
    else:
        print("Ps2_GetMeasuringRange failed:",ret)

    print("/**********************************************************************/")
    print("M/m: Change data mode: input corresponding index in terminal")
    print("D/d: Change depth range: input corresponding index in terminal")
    print("R/r: Change the RGB resolution: input corresponding index in terminal")
    print("Esc: Program quit ")
    print("/**********************************************************************/")

    try:
        while 1:
            ret, frameready = camera.Ps2_ReadNextFrame()
            if  ret !=0:
                print("Ps2_ReadNextFrame failed:",ret)
                time.sleep(1)
                continue
                                
            if  frameready.depth:      
                ret,depthframe = camera.Ps2_GetFrame(PsFrameType.PsDepthFrame)
                if  ret == 0:
                    frametmp = numpy.ctypeslib.as_array(depthframe.pFrameData, (1, depthframe.width * depthframe.height * 2))
                    frametmp.dtype = numpy.uint16
                    frametmp.shape = (depthframe.height, depthframe.width)

                    #convert ushort value to 0xff is just for display
                    img = numpy.int32(frametmp)
                    img = img*255/value_max
                    img = numpy.clip(img, 0, 255)
                    img = numpy.uint8(img)
                    frametmp = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
                    cv2.imshow("Depth Image", frametmp)
                else:
                    print("---end---")
            if  frameready.ir:
                ret,irframe = camera.Ps2_GetFrame(PsFrameType.PsIRFrame)
                if  ret == 0:
                    frametmp = numpy.ctypeslib.as_array(irframe.pFrameData, (1, irframe.width * irframe.height * 2))
                    frametmp.dtype = numpy.uint16
                    frametmp.shape = (irframe.height, irframe.width)
                    img = numpy.int32(frametmp)
                    img = img*255/3840
                    img = numpy.clip(img, 0, 255)
                    frametmp = numpy.uint8(img)
                    cv2.imshow("IR Image", frametmp)
            if  frameready.rgb:      
                ret,rgbframe = camera.Ps2_GetFrame(PsFrameType.PsRGBFrame)
                if  ret == 0:
                    frametmp = numpy.ctypeslib.as_array(rgbframe.pFrameData, (1, rgbframe.width * rgbframe.height * 3))
                    frametmp.dtype = numpy.uint8
                    frametmp.shape = (rgbframe.height, rgbframe.width,3)
                    cv2.imshow("RGB Image", frametmp)
                else:
                    print("---end---")
            key = cv2.waitKey(1)
            if  key == 27:
                cv2.destroyAllWindows()
                print("---end---")
                exit()
            elif  key == ord('m') or key == ord('M'):
                print("mode:")
                for index, element in enumerate(PsDataMode):
                    print(index, element)
                mode_input = input("choose:")
                for index, element in enumerate(PsDataMode):
                    if index == int(mode_input):
                        if index == 3:
                            WDRMode = PsWDROutputMode()
                            WDRMode.totalRange = 2
                            WDRMode.range1 = 0
                            WDRMode.range1Count = 1
                            WDRMode.range2 = 2
                            WDRMode.range2Count = 1
                            WDRMode.range3 = 5
                            WDRMode.range3Count = 1

                            ret = camera.Ps2_SetWDROutputMode(WDRMode)
                            if  ret != 0:  
                                print("Ps2_SetWDROutputMode failed:",ret)
                            
                            ret = camera.Ps2_SetDataMode(element)
                            if  ret == 0:
                                print("Ps2_SetDataMode {} success".format(element))
                            else:
                                print("Ps2_SetDataMode {} failed {}".format(element,ret))
                        else:
                            ret = camera.Ps2_SetDataMode(element)
                            if  ret == 0:
                                print("Ps2_SetDataMode {} success".format(element))
                            else:
                                print("Ps2_SetDataMode {} failed {}".format(element,ret))
            elif  key == ord('r') or key == ord('R'):
                print("resolution:")
                for index, element in enumerate(PsResolution):
                    print(index, element)
                mode_input = input("choose:")
                for index, element in enumerate(PsResolution):
                    if  index == int(mode_input):
                        camera.Ps2_SetRGBResolution(element)
            elif  key == ord('d') or key == ord('D'):
                print("depth range:")
                for index, element in enumerate(PsDepthRange):
                    print(index, element)
                mode_input = input("choose:")
                for index, element in enumerate(PsDepthRange):
                    if  index == int(mode_input):
                        ret = camera.Ps2_SetDepthRange(element)
                        if  ret == 0:
                            print("Ps2_SetDepthRange {} success".format(element))
                            ret, depth_max, value_min, value_max = camera.Ps2_GetMeasuringRange(PsDepthRange(element))
                            if  ret == 0:
                                print(PsDepthRange(element)," Ps2_GetMeasuringRange: ",depth_max,",",value_min,",",value_max)
                            else:
                                print(PsDepthRange(element)," Ps2_GetMeasuringRange failed:",ret)

                        else:
                            print("Ps2_SetDepthRange {} failed {}".format(element,ret))
                       
    except Exception as e :
        print(e)
    finally :
        print('end')
else:
    print('Ps2_OpenDevice failed: ' + str(ret))   
            

        
