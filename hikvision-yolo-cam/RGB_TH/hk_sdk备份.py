# Creater zch
from hk_dll import *
import hk_class as hk_class
from ctypes import *
import struct

import os
import time
from tkinter import *
import cv2
import threading



# 设备信息申明
DEV_IP = create_string_buffer(b'192.168.201.47')
DEV_PORT = 8000
DEV_USER_NAME = create_string_buffer(b'admin')
DEV_PASSWORD = create_string_buffer(b'abc12345')
WINDOWS_FLAG = False

win = None
funcRealDataCallBack_V30 = None

rectangle = False
m_strJpegWithAppenData = None
point_bytes = (c_byte * 4)()
position1 = None
position2 = None
temperature = None
# thread_lock = threading.Lock()

def init():
    a = NET_DVR_Init()
    if a == True:
        print('初始化成功')
    return a

# 登录


def login():
    # global DEV_IP, DEV_USER_NAME, DEV_PASSWORD
    # 注册
    device_info = NET_DVR_DEVICEINFO_V30()
    lUserId = NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, byref(device_info))
    return (lUserId)
    # DEV_IP = bytes('192.168.201.47', "ascii")
    # DEV_USER_NAME = bytes('admin', "ascii")
    # DEV_PASSWORD = bytes('abc12345', "ascii")
    # port = 8000
    #
    # struLoginInfo = hk_class.NET_DVR_USER_LOGIN_INFO()
    # # struLoginInfo.bUseAsynLogin = 0
    #
    # i = 0
    # for o in DEV_IP:
    #     struLoginInfo.sDeviceAddress[i] = o
    #     i += 1
    #
    # struLoginInfo.wPort = port
    # i = 0
    # for o in DEV_USER_NAME:
    #     struLoginInfo.sUserName[i] = o
    #     i += 1
    #
    # i = 0
    # for o in DEV_PASSWORD:
    #     struLoginInfo.sPassword[i] = o
    #     i += 1
    #
    # device_info = hk_class.NET_DVR_DEVICEINFO_V40()
    # loginInfo1 = byref(struLoginInfo)
    # loginInfo2 = byref(device_info)
    # print(loginInfo1,loginInfo2)
    # lUserId = NET_DVR_Login_V40("NET_DVR_Login_V40", loginInfo1, loginInfo2)
    #
    # if lUserId == -1:  # -1表示失败，其他值表示返回的用户ID值。
    #     error_info = NET_DVR_GetLastError
    #     print("登录错误信息：" + str(error_info))
    #
    # # 打开SDK写日志的功能
    # NET_DVR_SetLogToFile(3, b'./sdklog', False)
    # print('设备信息', device_info.byRetryLoginTime, device_info.bySupportLock)
    # print(lUserId)
    #
    # return lUserId

# 退出登录


def logout(lUserID):
    NET_DVR_Logout_V30(lUserID)


def DecCBFun(nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
    global Frame_YUV
    Frame_YUV = pFrameInfo
    # Playctrldll.PlayM4_ConvertToBmpFile(nPort, Frame_YUV)
    # print(nSize)
    # print(Frame_YUV)
    # print(nUser)
    # print(nReserved2)
    # print()

def RealDataCallBack_V30_RGB(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    '''
    码流回调函数
    '''
    # print(dwDataType)
    # if dwDataType == NET_DVR_SYSHEAD:
    #     # 设置流播放模式
    #     Playctrldll.PlayM4_SetStreamOpenMode(PLAYCTRL_PORT, 0)
    #     if Playctrldll.PlayM4_OpenStream(PLAYCTRL_PORT, pBuffer, dwBufSize, 1024 * 1000):
    #         # FuncDisplayCB = DISPLAYCBFUN(DisplayCBFun)
    #         FuncDisplayCB = DECCBFUN(DecCBFun)
    #         # Playctrldll.PlayM4_SetDisplayCallBack(PLAYCTRL_PORT, FuncDisplayCB)
    #         Playctrldll.PlayM4_SetDecCallBackExMend(PLAYCTRL_PORT, FuncDisplayCB)
    #
    #         if Playctrldll.PlayM4_Play(PLAYCTRL_PORT, hwnd):
    #             print(u'播放库播放成功')
    #         else:
    #             print(u'播放库播放失败')
    #     else:
    #         print(u'播放库打开流失败')
    #
    # elif dwDataType == NET_DVR_STREAMDATA:
    #     Playctrldll.PlayM4_InputData(PLAYCTRL_PORT, pBuffer, dwBufSize)
    #
    #
    # else:
    #     print(u'其他数据,长度:', dwBufSize)
    #
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     print('yes')
    #     exit()
    # return RealDataCallBack_V30_RGB


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


def cam_rgb():
    global frame_rgb, frame_the, rectangle, rgb_point, position1, position2, temperature
    cv2.namedWindow(win_name_rgb, 0)
    cv2.resizeWindow(win_name_rgb, 720, 520)
    while True:
        jpgname = "frame_rgb.jpg"
        suss = hCNetSDK.NET_DVR_CaptureJPEGPicture(lUserId, 1, byref(jpegpara), bytes(jpgname, 'utf-8'))
        print(NET_DVR_GetLastError())

        frame_rgb = cv2.imread(jpgname)

        if rectangle == True:
            # rgb_point = [[x1, y1], [x2, y2]]
            temperature = float(temperature)
            temperature = '%.2f' % temperature
            temperature = str(temperature)
            cv2.rectangle(frame_rgb, rgb_point[0], rgb_point[1], (0, 0, 255), 2)
            cv2.putText(frame_rgb, temperature, rgb_point[0], cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        if position1 != None and position2 != None:
            cv2.rectangle(frame_rgb, position1, position2, (0, 0, 255), 2)
            if temperature != None:
                temperature = float(temperature)
                temperature = '%.2f' % temperature
                temperature = str(temperature)
                cv2.putText(frame_rgb, temperature, position1, cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
        # cv2.resize(frame_rgb, (640, 512))
        cv2.imshow('rgb', frame_rgb)
        # cv2.resizeWindow(win_name_rgb, 640, 512)
        cv2.setMouseCallback(win_name_rgb, event_rgb)
        # thread_lock.release()

        if suss == 0:
            print("抓图不成功")

        k = cv2.waitKeyEx(1) & 0xff
        if k == ord('q'):
            exit()


def cam_thermal():
    global frame_rgb, frame_the, rectangle, rgb_point, position1, position2, temperature
    cv2.namedWindow(win_name_the, 0)
    cv2.resizeWindow(win_name_the, 720, 520)
    while True:
        jpgname_the = "frame_thermal.jpg"
        suss = hCNetSDK.NET_DVR_CaptureJPEGPicture(lUserId, 2, byref(jpegpara), bytes(jpgname_the, 'utf-8'))

        frame_the = cv2.imread(jpgname_the)
        # cv2.resize(frame_the, (640, 512))
        if rectangle == True:
            # rgb_point = [[x1, y1], [x2, y2]]
            temperature = float(temperature)
            temperature = '%.2f' % temperature
            temperature = str(temperature)
            cv2.rectangle(frame_the, rgb_point[0], rgb_point[1], (0, 0, 255), 2)
            cv2.putText(frame_the, temperature, rgb_point[0], cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        if position1 != None and position2 != None:
            cv2.rectangle(frame_the, position1, position2, (0, 0, 255), 2)
            if temperature != None:
                temperature = float(temperature)
                temperature = '%.2f' % temperature
                temperature = str(temperature)
                cv2.putText(frame_the, temperature, position1, cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        cv2.imshow('thermal', frame_the)

        # thread_lock.release()

        if suss == 0:
            print(NET_DVR_GetLastError)
            print("抓图不成功")

        k = cv2.waitKeyEx(1) & 0xff
        if k == ord('q'):
            exit()


def es(lRealHandle, cbPlayESCallBack):
    result = hCNetSDK.NET_DVR_SetESRealPlayCallBack(lRealHandle, cbPlayESCallBack, DEV_IP)
    if result < 0:
        print('接口调用失败，错误码：', NET_DVR_GetLastError())
    else:
        print('接口调用成功！！！')

def ESDataCallBack_V30(lPlayHandle, pstruPackInfo, pUser1):
    '''
    码流回调函数
    '''

    # print('进入ESDataCallBack_V30回调函数！！！')
    # print('lPlayHandle:', type(lPlayHandle))
    # print('pstruPackInfo:', type(pstruPackInfo))
    # print('pUser1:', type(pUser1))
    # print(lPlayHandle)
    # print(pstruPackInfo)
    # pstruPackInfo = pstruPackInfo.contents
    # pstruPackInfo = cast(pstruPackInfo, LPNET_DVR_PACKET_INFO_EX).contents

    # if pstruPackInfo.dwPacketType >= 1 and pstruPackInfo.dwPacketType <= 3:
    #     # 摄像头信息
    #     print(str(pstruPackInfo.dwYear) + '年' + str(pstruPackInfo.dwMonth) + '月' + str(pstruPackInfo.dwDay) + '日 ' + str(
    #         pstruPackInfo.dwHour) + ':' + str(pstruPackInfo.dwMinute) + ':' + str(
    #         pstruPackInfo.dwSecond) + ' wWidth:' + str(
    #         pstruPackInfo.wWidth) + ' wHeight:' + str(pstruPackInfo.wHeight) + ' dwTimeStamp:' + str(
    #         pstruPackInfo.dwTimeStamp) + ' dwTimeStampHigh :' + str(pstruPackInfo.dwTimeStampHigh), 'PacketType:'
    #           + str(pstruPackInfo.dwPacketType), '摄像头帧率:' + str(pstruPackInfo.dwFrameRate))
    #     pass


    return True


def InputData(fileMp4, Playctrldll):
    while True:
        pFileData = fileMp4.read(4096)
        if pFileData is None:
            break

        if not Playctrldll.PlayM4_InputData(PLAYCTRL_PORT, pFileData, len(pFileData)):
            break


# 获取抓拍图片最高温度
def get_temperature_all(lUserID):

    ret, m_strJpegWithAppenData = get_temperature0(lUserID)
    max_temperature = -50
    min_temperature = 120

    byValue = m_strJpegWithAppenData.pP2PDataBuff.contents.byValue


    if ret:
        # print(m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)
        for x in range(m_strJpegWithAppenData.dwJpegPicWidth):
            for y in range(m_strJpegWithAppenData.dwJpegPicHeight):

                temperature = struct.unpack('<f', struct.pack('4b', *get_bytes(byValue, (m_strJpegWithAppenData.dwJpegPicWidth * y + x) * 4, 4)))[0]

                max_temperature = temperature if temperature > max_temperature else max_temperature
                min_temperature = temperature if temperature < min_temperature else min_temperature

        return True, max_temperature, min_temperature

    return False, max_temperature, min_temperature


# 获取给定点列表最高温度
def get_temperature_max(points, sourceWidth, sourceHeight, lUserID):

    ret, m_strJpegWithAppenData = get_temperature0(lUserID)

    if(len(points) < 2):
        return False, -2

    if ret:
        x1, y1 = point2point(points[0][0], points[0][1], sourceWidth, sourceHeight,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)

        x2, y2 = point2point(points[1][0], points[1][1], sourceWidth, sourceHeight,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)

        if x1 > x2 or y1 > y2:  #  画面的坐标来测温
            return False, -3

        byValue = m_strJpegWithAppenData.pP2PDataBuff.contents.byValue

        max_temperature = -50.0
        temperature_list = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                temperature = struct.unpack('<f', struct.pack('4b', *get_bytes(byValue,  (m_strJpegWithAppenData.dwJpegPicWidth * y + x) * 4, 4)))[0]
                max_temperature = temperature if temperature > max_temperature else max_temperature
                # temperature_list.append(max_temperature)

        return True, max_temperature

    return False, -1


# 获取给定点列表最高温度
def get_temperature_max(points, sourceWidth, sourceHeight, lUserID):

    ret, m_strJpegWithAppenData = get_temperature0(lUserID)

    if(len(points) < 2):
        return False, -2

    if ret:
        thermal_x1, thermal_y1 = point2point(points[0][0], points[0][1], sourceWidth, sourceHeight,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)

        thermal_x2, thermal_y2 = point2point(points[1][0], points[1][1], sourceWidth, sourceHeight,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)

        if thermal_x1 > thermal_x2 or thermal_y1 > thermal_y2:  #  画面的坐标来测温
            return False, -3

        byValue = m_strJpegWithAppenData.pP2PDataBuff.contents.byValue

        max_temperature = -50.0
        temperature_list = []
        for x in range(thermal_x1, thermal_x2 + 1):
            for y in range(thermal_y1, thermal_y2 + 1):
                # 160 * 120
                temperature = struct.unpack('<f', struct.pack('4b', *get_bytes(byValue, (
                            m_strJpegWithAppenData.dwJpegPicWidth * y + x) * 4, 4)))[0]
                max_temperature = temperature if temperature > max_temperature else max_temperature
                temperature_list.append(temperature)

        return True, max_temperature, temperature_list

    return False, -1


# 截取指定下标的和长度的返回数据
def get_bytes(src_bytes, offset, length):
    global point_bytes

    for i in range(length):
        point_bytes[i] = src_bytes[offset + i]

    # del src_bytes

    return point_bytes


# 获取温度
def get_temperature0(lUserID):
    bRet = False
    global m_strJpegWithAppenData

    if m_strJpegWithAppenData is None:
        m_strJpegWithAppenData = hk_class.NET_DVR_JPEGPICTURE_WITH_APPENDDATA()

        m_strJpegWithAppenData.byRes = (c_byte * 255)()
        m_strJpegWithAppenData.dwChannel = 2
        m_strJpegWithAppenData.pJpegPicBuff = pointer(
            hk_class.BYTE_ARRAY((c_byte * 2097152)()))
        m_strJpegWithAppenData.pP2PDataBuff = pointer(
            hk_class.BYTE_ARRAY((c_byte * 2097152)()))

        m_strJpegWithAppenData.dwSize = sizeof(m_strJpegWithAppenData)

    bRet = NET_DVR_CaptureJPEGPicture_WithAppendData(lUserID, 2, byref(m_strJpegWithAppenData))
    if bRet:
        # 测温数据
        print('测温数据', m_strJpegWithAppenData.dwP2PDataLen)
        if m_strJpegWithAppenData.dwP2PDataLen > 0:
            return True, m_strJpegWithAppenData
    else:
        print('测温错误消息', NET_DVR_GetLastError())
        return False, None


# 坐标转换
# @njit
# (x, y, 1920, 1080, 640, 512)
def point2point(x, y, sourceWidth, sourceHeight, targetWidth, targetHeight):
    thermal_x = x * targetWidth / sourceWidth
    thermal_y = y * targetHeight / sourceHeight

    # thermal_x = x if x <= targetWidth else targetWidth
    # thermal_x = 0 if x < 0 else x
    #
    # thermal_y = y if y <= targetHeight else targetHeight
    # thermal_y = 0 if y < 0 else y

    print('转换后的坐标是:', thermal_x, thermal_y)
    return int(thermal_x), int(thermal_y)


def xFunc1(event):
    print(f"特殊按键触发:{event.char},对应的ASCII码:{event.keycode}")


def event_rgb(event, x, y, flags, param):
    global lUserId, rectangle, frame, rgb_point, position1, position2, temperature
    # 双击左键:标记坐标并测温
    if flags == (cv2.EVENT_FLAG_ALTKEY + cv2.EVENT_FLAG_LBUTTON):
        position1 = None
        position2 = None
        print(x, y)
        #  划定一个100x100的范围
        if x-50 <= 0:
            x = 50

        if y-50 <= 0:
            y = 50

        if x+50 >= 1920:
            x = 1870

        if y+50 >= 1080:
            y = 1030

        x1 = x-50
        y1 = y-50
        x2 = x+50
        y2 = y+50

        rgb_point = [[x1, y1], [x2, y2]]
        rectangle = True

        result, temperature, temperature_list = get_temperature_max(rgb_point, 1920, 1080, lUserId)
        if result:
            print('测温结果:', temperature)
            # print('测温矩阵:', temperature_list)
        else:
            print('测温失败')


    elif event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        position1 = (x1, y1)
        position2 = None

    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        rectangle = False
        x2, y2 = x, y
        position2 = (x2, y2)

    elif event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        position2 = (x2, y2)

        if position1 != None:
            rgb_point_ex = [position1, position2]
            result, temperature, temperature_list = get_temperature_max(rgb_point_ex, 1920, 1080, lUserId)
            if result:
                print('测温结果:', temperature)
                # print('测温矩阵:', temperature_list)
            else:
                print('测温失败')


    # Ctrl+左键:左转
    if flags == (cv2.EVENT_FLAG_LBUTTON + cv2.EVENT_FLAG_CTRLKEY):
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, PAN_LEFT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 左转控制')
        # 停止云台控制
        time.sleep(0.04)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, PAN_LEFT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # Ctrl+右键:右转
    if flags == (cv2.EVENT_FLAG_RBUTTON + cv2.EVENT_FLAG_CTRLKEY):
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, PAN_RIGHT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 右转控制')
        # 停止云台控制
        time.sleep(0.04)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, PAN_RIGHT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # Ctrl+左键长按:左持续转
    if flags == (cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, PAN_LEFT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 左持续转')

    # 左键放起:停止
    if event == cv2.EVENT_LBUTTONUP:
        print('stop')
        # 停止云台控制
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, PAN_LEFT, 1, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # Ctrl+右键长按:右持续转
    if flags == (cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_RBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, PAN_RIGHT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 右持续转')

    # 右键放起:停止
    if event == cv2.EVENT_RBUTTONUP:
        print('stop')
        # 停止云台控制
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, PAN_RIGHT, 1, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # SHIFT+左键:上仰
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_FLAG_LBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, TILT_UP, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 上仰')
        # 停止云台控制
        time.sleep(0.04)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, PAN_RIGHT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # SHIFT+右键:下俯
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_FLAG_RBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, TILT_DOWN, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 下俯')
        # 停止云台控制
        time.sleep(0.04)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, PAN_RIGHT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # SHIFT+左键长按:上仰持续
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_LBUTTONDOWN):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, TILT_UP, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 上仰持续')

    # SHIFT+右键长按:下俯持续
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_RBUTTONDOWN):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, TILT_DOWN, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 下俯持续')

    # Ctrl+中键放起:停止
    if flags == (cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_MBUTTONDOWN):
        # 停止云台控制
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, PAN_RIGHT, 1, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # 滚轮向后:缩小
    if event == cv2.EVENT_MOUSEWHEEL and flags < 0:
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_OUT, 0)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 缩小')
        time.sleep(0.2)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_OUT, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # 滚轮向前:放大
    if event == cv2.EVENT_MOUSEWHEEL and flags > 0:
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 0)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 放大')
        time.sleep(0.2)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # if flags == (cv2.EVENT_FLAG_LBUTTON + cv2.EVENT_FLAG_ALTKEY):
    #     lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 0)
    #     lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 0)
    #     if lRet_RGB == 0 and lRet_TH == 0:
    #         print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    #     else:
    #         print('ptz 放大')
    #     time.sleep(0.2)
    #     lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 1)
    #     lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 1)
    #     if lRet_RGB == 0 and lRet_TH == 0:
    #         print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    #     else:
    #         pass
    #
    # if flags == (cv2.EVENT_FLAG_RBUTTON + cv2.EVENT_FLAG_ALTKEY):
    #     lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_OUT, 0)
    #     lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_OUT, 0)
    #     if lRet_RGB == 0 and lRet_TH == 0:
    #         print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    #     else:
    #         print('ptz 放大')
    #     time.sleep(0.2)
    #     lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_OUT, 1)
    #     lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_OUT, 1)
    #     if lRet_RGB == 0 and lRet_TH == 0:
    #         print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    #     else:
    #         pass


def event_th(event, x, y, flags, param):
    global frame, lUserId

    lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_OUT, 0)
    if lRet == 0:
        print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    else:
        print('ptz 缩小')
    time.sleep(0.2)
    lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_OUT, 1)
    if lRet == 0:
        print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    else:
        pass

    lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 0)
    if lRet == 0:
        print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    else:
        print('ptz 放大')
    time.sleep(0.2)
    lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 1)
    if lRet == 0:
        print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
    else:
        pass


def on_press(key):
    '按下按键时执行。'
    try:
        lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 0)
        lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 0)
        if lRet_RGB == 0 and lRet_TH == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 放大')
        time.sleep(0.2)
        lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 1)
        lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 1)
        if lRet_RGB == 0 and lRet_TH == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass
    except AttributeError:
        pass
    #通过属性判断按键类型。

def on_release(key):
    '松开按键时执行。'
    # 停止云台控制
    lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, PAN_RIGHT, 1, 1)
    if lRet == 0:
        print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
    else:
        pass


def test_a():
    while True:
        k = cv2.waitKeyEx(1) & 0xff

        if k == ord('a'):
            lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 0)
            lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 0)
            if lRet_RGB == 0 and lRet_TH == 0:
                print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
            else:
                print('ptz 放大')
            time.sleep(0.2)
            lRet_RGB = NET_DVR_PTZControl(lRealPlayHandle_RGB, ZOOM_IN, 1)
            lRet_TH = NET_DVR_PTZControl(lRealPlayHandle_TH, ZOOM_IN, 1)
            if lRet_RGB == 0 and lRet_TH == 0:
                print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
            else:
                pass
        if k == 81:
            print("down")
        if k == 82:
            print("enter")
        if k == 83:
            print("space")
        if k == ord('q'):
            exit()

def get_config():
    global lUserId
    config = NET_DVR_STD_CONFIG_SENSOR()
    config.lpCondBuffer = None
    config.dwCondSize = sizeof(config)
    config.lpInBuffer = None
    config.dwInSize = (c_int)()
    # config.iRotation = (c_int)()
    # config.iFieldAngle = (c_int)()
    # config.byRes = (c_byte * 128)()
    ret = NET_DVR_GetSTDConfig(lUserId, 3763, byref(config))
    # ret = NET_DVR_GetDVRConfig(lUserId, 1015, 0xFFFFFFFF, lpOutBuffer, dwOutBufferSize, byref(n))
    print(ret, NET_DVR_GetLastError())
    print(config.dwSize, config.iPan, config.iTilt, config.iRotation, config.iFieldAngle)


def end():
    exit()


if __name__ == '__main__':

    # 创建窗口
    # win = Tk()
    # win.geometry('200x50')
    # b1 = Button(win, text='关闭', bd=2, command=end)
    # b1.pack()

    # 创建一个Canvas，设置其背景色为白色
    # cv = Canvas(win, bg='white', width=640, height=512)
    # cv.pack()
    # hwnd = cv.winfo_id()
    win_name_rgb = 'rgb'
    win_name_the = 'thermal'
    # cv2.namedWindow(win_name_rgb, 0)
    # cv2.resizeWindow(win_name_rgb, 640, 512)
    # cv2.namedWindow(win_name_the, 0)
    # cv2.resizeWindow(win_name_the, 640, 512)
    # hwnd = win32gui.FindWindow(None, win_name)
    # cv2.setMouseCallback(win_name_rgb, event_rgb)
    # cv2.setMouseCallback(win_name, event_th)
    # thread_rgb_ctrl = threading.Thread(target=thread_rgb, args=(win_name, ))
    # thread_th_ctrl = threading.Thread(target=thread_th, args=(win_name, ))
    # thread_rgb_ctrl.start()
    # thread_th_ctrl.start()
    # thread_rgb_ctrl.join()
    # thread_th_ctrl.join()
    # print('hwnd', hwnd)
    # 获取系统平台
    # load library
    # (sdkPath, tempfilename) = os.path.split('./lib')
    Playctrldll = LoadPlayctrlSDK('.', WINDOWS_FLAG)
    if not Playctrl_Getport(Playctrldll):
        print(u'获取播放库通道号失败')
        # exit()

    # 加载HCNetSDK库
    # Objdll = LoadHCNetSDK()

    # 初始化HCNetSDK库
    # InitHCNetSDK(Objdll)
    init()
    # 登录设备

    (lUserId) = login()
    if lUserId < 0:
        print('Login device fail, error code is:', NET_DVR_GetLastError())
        # 释放资源
        NET_DVR_Cleanup()
        exit()

    # if lUserId >= 0:
    #     capture()

    # 定义码流回调函数
    funcRealDataCallBack_V30_RGB = REALDATACALLBACK(RealDataCallBack_V30_RGB)
    funcRealDataCallBack_V30_TH = REALDATACALLBACK(RealDataCallBack_V30_TH)
    # 开启预览
    ESRealDataCallBack_V30 = ESREALDATACALLBACK(ESDataCallBack_V30)

    lRealPlayHandle_RGB = OpenPreview_1(lUserId, funcRealDataCallBack_V30_RGB)
    lRealPlayHandle_TH = OpenPreview_2(lUserId, funcRealDataCallBack_V30_TH)

    esHandle = c_long(-1)
    esHandle = es(lRealPlayHandle_RGB, ESRealDataCallBack_V30)


    if lRealPlayHandle_RGB < 0:
        print('Open preview fail, error code is:', NET_DVR_GetLastError())

        # 登出设备
        NET_DVR_Logout(lUserId)
        # 释放资源
        NET_DVR_Cleanup()
        exit()

    # get_time(lUserId)

    # show Windows
    if lUserId >= 0:
        # thread_frame = threading.Thread(target=capture)
        # thread_ctrl = threading.Thread(target=test_a)
        # thread_frame.start()
        # thread_ctrl.start()
        # keyboard.add_hotkey('a', test_a)
        thread_rgb = threading.Thread(target=cam_rgb)
        # thread_the = threading.Thread(target=cam_thermal)
        thread_rgb.start()
        # thread_the.start()


    NET_DVR_Logout(lUserId)
    # 释放资源
    NET_DVR_Cleanup()
    exit()
    Playctrldll.PlayM4_Stop(PLAYCTRL_PORT)
    Playctrldll.PlayM4_CloseStream(PLAYCTRL_PORT)
    Playctrldll.PlayM4_FreePort(PLAYCTRL_PORT)
    PLAYCTRL_PORT = c_long(-1)



    # 关闭预览
    NET_DVR_StopRealPlay(lRealPlayHandle_RGB)

    # 登出设备
    NET_DVR_Logout(lUserId)

    # 释放资源
    NET_DVR_Cleanup()
