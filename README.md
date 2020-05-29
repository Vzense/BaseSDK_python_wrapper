

## Python Wrapper for Vzense Base SDK API

Python wrapper is an opensource project of Vzense TOF camera API.

The goal of this project is to help developers use Vzense TOF camera via python method easily.

### Requirements

- Vzense library: vzense_api.dll / libvzense_api.so
- python modules : ctypes, numpy, opencv-python(display only)

### Directory

- **linux_lib / windows_lib**: The dynamic library folder

  ```
  /libImgPreProcess.so
  /libvzense_api.so
  ```

- **zense_cam_api.py**: zense tof wrapper code 

- **zense_cam_demo.py**: python api using demo code

### How to use

1. make sure copy the right dynamic library files to project root directory
2. Run zense_cam_demo.py

User can refrence the demo code to create your project.

### FAQ:

Which version do you use?

python3.6, [Vzense_SDK_linux](https://github.com/Vzense/Vzense_SDK_linux) v3.0.0.8 Ubuntu18.04, [Vzense_SDK_windows](https://github.com/Vzense/Vzense_SDK_windows) v3.0.0.8

Which devices can this project support?

This demo only support DCAM710. If you want to use other product, you can modify the code based on different API. But there have very little difference.

