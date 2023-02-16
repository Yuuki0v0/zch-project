# Creater zch

from RGB_TH.hk_dll import *
import RGB_TH.hk_class as hk_class
from ctypes import *
import struct

import time
import cv2
import threading


# 设备信息申明
# DEV_IP = create_string_buffer(b'192.168.1.84')
# DEV_PORT = 8000
# DEV_USER_NAME = create_string_buffer(b'admin')
# DEV_PASSWORD = create_string_buffer(b'abc12345')


win = None
funcRealDataCallBack_V30 = None

rectangle = False
m_strJpegWithAppenData = None
point_bytes = (c_byte * 4)()
position1 = None
position2 = None
temperature = None
k = None

win_name_rgb = 'rgb'
win_name_the = 'thermal'
# thread_lock = threading.Lock()


# 初始化
def init():
    return NET_DVR_Init()


# 登录
# ip地址，端口，用户名，密码
def login(ip, port, username, password):
    # 注册
    device_info = NET_DVR_DEVICEINFO_V30()
    lUserId = NET_DVR_Login_V30(bytes(ip, 'utf-8'), port, bytes(username, 'utf-8'), bytes(password, 'utf-8'), byref(device_info))
    # lUserId = NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(device_info))
    print('lUserId', lUserId)
    return (lUserId)


# 退出登录
def logout(lUserID):
    NET_DVR_Logout_V30(lUserID)


def DecCBFun(nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
    pass


def RealDataCallBack_V30_RGB(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    '''
    码流回调函数
    '''


def RealDataCallBack_V30_TH(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    '''
    码流回调函数
    '''


def OpenPreview_1(lUserId, callbackFun):
    '''
    打开预览
    '''
    global realplay_mode
    realplay_mode = 'RGB'
    preview_info = NET_DVR_PREVIEWINFO()
    preview_info.hPlayWnd = None
    preview_info.lChannel = 1  # 通道号
    preview_info.dwStreamType = 0  # 主码流
    preview_info.dwLinkMode = 0  # TCP
    preview_info.bBlocked = 1  # 阻塞取流
    callbackFun_RGB = callbackFun
    lRealPlayHandle_RGB = NET_DVR_RealPlay_V40(lUserId, byref(preview_info), callbackFun_RGB, None)
    return lRealPlayHandle_RGB


def OpenPreview_2(lUserId, callbackFun):
    '''
    打开预览
    '''
    global realplay_mode
    realplay_mode = 'TH'
    preview_info = NET_DVR_PREVIEWINFO()
    preview_info.hPlayWnd = None
    preview_info.lChannel = 2  # 通道号
    preview_info.dwStreamType = 0  # 主码流
    preview_info.dwLinkMode = 0  # TCP
    preview_info.bBlocked = 1  # 阻塞取流
    callbackFun_TH = callbackFun
    lRealPlayHandle_TH = NET_DVR_RealPlay_V40(lUserId, byref(preview_info), callbackFun_TH, None)
    return lRealPlayHandle_TH


def es(lRealHandle, cbPlayESCallBack, DEV_IP):
    result = hCNetSDK.NET_DVR_SetESRealPlayCallBack(lRealHandle, cbPlayESCallBack, DEV_IP)
    if result < 0:
        print('接口调用失败，错误码：', NET_DVR_GetLastError())
    else:
        print('接口调用成功！！！')


def ESDataCallBack_V30(lPlayHandle, pstruPackInfo, pUser1):
    '''
    码流回调函数
    '''
    return True


def InputData(fileMp4, Playctrldll):
    while True:
        pFileData = fileMp4.read(4096)
        if pFileData is None:
            break

        if not Playctrldll.PlayM4_InputData(PLAYCTRL_PORT, pFileData, len(pFileData)):
            break

