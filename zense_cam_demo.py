from zense_cam_api import *
import zense_cam_api
import cv2



print(zense_cam_api.__version__)
print(zense_cam_api.__author__)

camera = PicoTofCam()
status = 'init'

camera_count = camera.get_cam_count()


for x in range(0, camera_count):
    print(str(x) + ':' + str(camera.get_cam_info(x)))

if camera_count > 1:
    index = input("chose open camera:")
elif camera_count == 1:
    index = 0
    print("only one cam, auto chose")        
else: 
    print("there are no camera found")
    exit()

rst, handle = camera.open_cam(int(index))
depthrange = DepthRange.NEAR_Range
depth_max, value_min, value_max = camera.get_measuring_range(handle, 0, depthrange)
qvga_frame = numpy.zeros((240, 320), dtype = numpy.uint16, order = 'C')

if  rst == 'success':
    print(camera.get_threshold(handle))
    print(camera.get_pulsecnt(handle))
    camera.start_stream(handle)
    camera.set_data_mode(handle, 0, DataMode.IR_AND_RGB_30)
    while 1:
        frameready = camera.read_next_frame(handle)
        #print('frame ready:',(frameready.depth, frameready.ir, frameready.rgb))
        if frameready.depth:
            rst,depthframe,width,height = camera.get_frame(handle)
            if rst == 'success':
                cv2.namedWindow("depthimage")
                #convert ushort value to 0xff is just for display
                img = numpy.int32(depthframe)
                img = img*255/depth_max
                img = numpy.clip(img, 0, 255)
                img = numpy.uint8(img)
                depthframe = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
                cv2.imshow("depthimage", depthframe)
        if frameready.ir:
            rst,irframe,width,height = camera.get_frame(handle, 0, FrameType.IR_FRAME)
            if rst == 'success':
                img = numpy.int32(irframe)
                intimg = numpy.int32(irframe)
                img = img*255/4095
                img = numpy.clip(img, 0, 255)
                irframe = numpy.uint8(img)
                for cols in range(0, 320):
                    for rows in range(0, 240):
                        mean = intimg[2 * rows, 2 * cols] + intimg[2 * rows, 2 * cols + 1] + intimg[2 * rows + 1, 2 * cols] + intimg[2 * rows + 1, 2 * cols + 1]
                        qvga_frame[rows, cols] = numpy.uint16(mean/4)
                qvgaimg = numpy.int32(qvga_frame)
                qvgaimg = qvgaimg*255/4095
                qvgaimg = numpy.clip(qvgaimg, 0, 255)
                qvgaimg = numpy.uint8(qvgaimg)
                resized_img = cv2.resize(qvgaimg, (640, 480), interpolation = cv2.INTER_LINEAR)
                cv2.namedWindow("qvairimage")
                cv2.imshow("qvairimage", qvgaimg)
                cv2.namedWindow("resized IR")
                cv2.imshow("resized IR", resized_img)
                cv2.namedWindow("irimage")
                cv2.imshow("irimage", irframe)
                
        if frameready.rgb:
            rst,rgbframe,width,height = camera.get_frame(handle, 0, FrameType.RGB_FRAME)
            if rst == 'success':
                cv2.namedWindow("rgbimage")
                cv2.imshow("rgbimage", rgbframe)
        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            exit()
        elif key == ord('m'):
            print("mode:")
            for index, element in enumerate(DataMode):
                print(index, element)
            mode_input = input("chose:")
            for index, element in enumerate(DataMode):
                if index == int(mode_input):
                    camera.set_data_mode(handle, 0, element)
        elif key == ord('r'):
            print("resolution:")
            for index, element in enumerate(RGBResolution):
                print(index, element)
            mode_input = input("chose:")
            for index, element in enumerate(RGBResolution):
                if index == int(mode_input):
                    camera.set_rgb_resolution(handle, 0, element)
        elif key == ord('d'):
            print("depth range:")
            for index, element in enumerate(DepthRange):
                print(index, element)
            mode_input = input("chose:")
            for index, element in enumerate(DepthRange):
                if index == int(mode_input):
                    camera.set_depth_range(handle, 0, element)
                    depth_max, value_min, value_max = camera.get_measuring_range(handle, 0, element)
        # elif key == ord('s'):
        #     print("save ir image!!")
        #     numpy.save("irframe.bin", irframe)

            

        
