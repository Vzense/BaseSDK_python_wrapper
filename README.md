## Python Wrapper for Vzense Base SDK API

Python wrapper is an opensource project of Vzense TOF camera API.

The goal of this project is to help developers use Vzense TOF camera via python method easily.

- PythonSDK version: V3.5.4.1
- VzenseBaseSDK version: V3.5.4

### Supported Devices

- DCAM710 
- DCAM550U
- DCAM550P
- DCAM550E
- DCAM560C
### Requirements

- python version : 3.7.x
- python modules : ctypes, numpy, opencv-python(display only)

### Directory

- **DCAM550**: the API and Sample code for DCAM550U/DCAM550P/DCAM550E
- **DCAM560**: the API and Sample code for DCAM560CPRO/DCAM560CLITE
- **DCAM710**: the API and Sample code for DCAM710
- **Lib**: VzenseBaseSDK dynamic library files
- **install.py**: install file
- **config.txt**: set the config that needed by 'install.py', such as:
```
system = Windows64
url = https://gitee.com
```
|system|details|
|---|---|
|Windows64|windows 64 bit|
|Windows32|windows 32 bit|
|Ubuntu20.04|the same with Ubuntu18.04 PC SDK|
|Ubuntu18.04|for PC with x86_64-linux-gnu(v7.5.0)|
|Ubuntu16.04|for PC with x86_64-linux-gnu(v5.4.0)|
|AArch64|for aarch64 with aarch64-linux-gnu(v5.4.0)|
|Arm-linux-gnueabihf|for arm32 with arm-linux-gnueabihf(v5.4.0)|

|url|
|---|
|https://gitee.com|
|https://github.com|

### Quick Start

- step1. install modules:
         
```	 
	  pip install numpy
	  pip install opencv-python 
```
- step2. Set 'config.txt' according to your needs

- step3. Run the 'python install.py' 

- step4. Switch to Samples under the product directory, run the sample that you need. 
    	 
         For example, go to the DCAM560/Samples/FrameViewer, then run 'python FrameViewer_DCAM560.py'

