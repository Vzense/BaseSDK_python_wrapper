import sys
import subprocess
import os
import re
import shutil

# check modules
import numpy
import cv2
import ctypes
 

system_config = "Ubuntu18.04"
url_config = "https://gitee.com"

# py version >= 3.5 
def execSysCommand(arglist):
    ret = subprocess.run(arglist)
    if ret.returncode == 0:
        return 'success'
    else:
        return 'fail'

def pullSDK(url):  
    curPath = os.path.dirname(os.path.abspath(__file__))
    sdkPath = curPath + "/tmp"
    if not os.path.exists(sdkPath):
        os.makedirs(sdkPath)
    
    os.chdir(sdkPath)
    curPath_ = os.getcwd()
    if execSysCommand(url) == 'success':
        # Windows
        if system_config == 'Windows64' or system_config == 'Windows32':
            src = sdkPath + "/Vzense_SDK_windows/Bin/x64"
            if system_config != 'Windows64':
                src = sdkPath + "/Vzense_SDK_windows/Bin/x86"
            dst = curPath+ "/Lib"
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print("pull SDK success")
        elif system_config == 'Ubuntu20.04' or system_config == 'Ubuntu18.04':
            src = sdkPath + "/Vzense_SDK_linux/%s/Lib" %('Ubuntu18.04')
            dst = curPath + "/Lib"
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.move(src, dst)
            print("pull SDK success")
        else:
            src = sdkPath + "/Vzense_SDK_linux/%s/Lib" %(system_config)
            dst = curPath + "/Lib"
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.move(src, dst)
            print("pull SDK success")
    else:
        print("pull SDK fail")

def checkConfig():
    global system_config
    global url_config
    
    curPath = os.path.dirname(os.path.abspath(__file__))
    filename = curPath + "/config.txt"
    with open(filename,"r") as fr:
        lines = fr.readlines()
        if len(lines) == 2 :
            if re.search(r'system',lines[0], re.M|re.I) \
                and re.search(r'url',lines[1], re.M|re.I):
                
                tmp_list = lines[0].split('=')
                if len(tmp_list) == 2: 
                    system_config = tmp_list[1].strip()

                tmp_list = lines[1].split('=')
                if len(tmp_list) == 2:
                    if system_config == 'Windows64' or system_config == 'Windows32':
                        url_config = tmp_list[1].strip()+ '/Vzense/Vzense_SDK_windows.git'
                    else:
                        url_config = tmp_list[1].strip()+ '/Vzense/Vzense_SDK_linux.git'
                return True    
            else:
                return False 
        else:
            return False 

# check config.txt
if checkConfig() == True:   
    print(system_config)
    print(url_config)
else:
    print('check config.txt error, exit')
    exit()

# git clone basesdk to tmp
cmdlist = ['git','clone','-b','V3.5.4','--depth=1',url_config]
pullSDK(cmdlist)

