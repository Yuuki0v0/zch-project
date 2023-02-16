# Creater zch

from RGB_TH.hk_dll import *
import RGB_TH.hk_class as hk_class
from ctypes import *
import struct
import numpy as np


m_strJpegWithAppenData = None
point_bytes = (c_byte * 4)()
# position1 = None
# position2 = None
temperature = None
k = None


# 坐标转换
# (x, y, 1280, 720, 256, 192) (需要转换的x, 需要转换的y, 热成像画面分辨率宽, 热成像画面分辨率高, 测温分辨率宽, 测温分辨率高)
def point2point(x, y, sourceWidth, sourceHeight, targetWidth, targetHeight):
    thermal_x = x * targetWidth / sourceWidth
    thermal_y = y * targetHeight / sourceHeight

    return int(thermal_x), int(thermal_y)


# 截取指定下标的和长度的返回数据
def get_bytes(src_bytes, offset, length):
    global point_bytes

    for i in range(length):
        point_bytes[i] = src_bytes[offset + i]

    # del src_bytes

    return point_bytes


# 获取抓拍图片全部范围内最高温度
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
# 测温范围，热成像分辨率宽，热成像分辨率高，摄像头ID
def get_temperature_max(points, sourceWidth, sourceHeight, lUserID):
    global m_strJpegWithAppenData

    ret, m_strJpegWithAppenData = get_temperature0(lUserID)

    if(len(points) < 2):
        return False, -2

    if ret:
        print('测温分辨率', m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)
        thermal_x1, thermal_y1 = point2point(points[0][0], points[0][1], sourceWidth, sourceHeight,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)
        print('左上角坐标转换测温的坐标是:', thermal_x1, thermal_y1)

        thermal_x2, thermal_y2 = point2point(points[1][0], points[1][1], sourceWidth, sourceHeight,
                             m_strJpegWithAppenData.dwJpegPicWidth, m_strJpegWithAppenData.dwJpegPicHeight)
        print('右下角坐标转换测温的坐标是:', thermal_x2, thermal_y2)

        if thermal_x1 > thermal_x2 or thermal_y1 > thermal_y2:  # 画面的坐标来测温
            print('坐标错误')
            return False, None, None, None

        byValue = m_strJpegWithAppenData.pP2PDataBuff.contents.byValue

        # max_temperature = -50.0
        temperature_list = []
        for x in range(thermal_x1, thermal_x2 + 1):
            for y in range(thermal_y1, thermal_y2 + 1):
                # 160 * 120
                temperature = struct.unpack('<f', struct.pack('4b', *get_bytes(byValue, (
                            m_strJpegWithAppenData.dwJpegPicWidth * y + x) * 4, 4)))[0]
                # max_temperature = temperature if temperature > max_temperature else max_temperature
                temperature_list.append(temperature)
        max_temp = max(temperature_list)
        min_temp = min(temperature_list)
        mean_temp = np.mean(temperature_list)
        print('最高温:{}, 最低温:{}, 平均温:{}'.format(max_temp, min_temp, mean_temp))
        return True, max_temp, temperature_list, mean_temp
    print('无法测温')
    return False, None, None, None


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
        if m_strJpegWithAppenData.dwP2PDataLen > 0:
            return True, m_strJpegWithAppenData
    else:
        print('测温错误消息', NET_DVR_GetLastError())
        return False, None