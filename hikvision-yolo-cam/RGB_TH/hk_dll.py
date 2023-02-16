# Creater zch

from ctypes import c_int32, c_char_p, c_void_p, c_float, c_size_t, c_ubyte, c_long, cdll, POINTER, CDLL, c_bool, c_long, c_short
import sys
from RGB_TH.hk_class import *
from ctypes import *

path = sys.argv[0].rsplit('/', 1)[0]
# print('path:', path)
if 'linux' == sys.platform:
    hCNetSDK = CDLL(path + '/RGB_TH/lib/libhcnetsdk.so')
    functype = CFUNCTYPE
    WINDOWS_FLAG = False
else:
    hCNetSDK = CDLL(path + '/RGB_TH/lib/HCNetSDK.dll')
    functype = WINFUNCTYPE
    WINDOWS_FLAG = True


SERIALNO_LEN = 48  # 序列号长度
NAME_LEN = 32  # 用户名长度

# 显示回调函数
DISPLAYCBFUN = functype(None, c_long, c_char_p, c_long, c_long, c_long, c_long, c_long, c_long)
DECCBFUN = functype(None, c_long, c_char_p, c_void_p, c_long, c_long, c_long)


PLAYCTRL_PORT = c_long(-1)
Playctrldll = None
FuncDisplayCB = None
# NET_DVR_SetSDKInitCfg = hCNetSDK.NET_DVR_SetSDKInitCfg
# NET_DVR_SetSDKInitCfg.restype = c_bool
# NET_DVR_SetSDKInitCfg.argtypes = (POINTER(NET_SDK_INIT_CFG_TYPE), c_void_p)

# //boolean NET_DVR_Init();
NET_DVR_Init = hCNetSDK.NET_DVR_Init
NET_DVR_Init.restype = c_bool
NET_DVR_Init.argtypes = ()

# NativeLong NET_DVR_Login_V30(String sDVRIP, short wDVRPort, String sUserName, String sPassword, NET_DVR_DEVICEINFO_V30 lpDeviceInfo);
NET_DVR_Login_V30 = hCNetSDK.NET_DVR_Login_V30
NET_DVR_Login_V30.restype = c_long
NET_DVR_Login_V30.argtypes = (c_char_p, c_short, c_char_p, c_char_p, POINTER(NET_DVR_DEVICEINFO_V30))

NET_DVR_Login_V40 = hCNetSDK.NET_DVR_Login_V40
# NET_DVR_Login_V40.restype = c_long
# NET_DVR_Login_V40.argtypes = (POINTER(NET_DVR_USER_LOGIN_INFO), POINTER(NET_DVR_DEVICEINFO_V40))

NET_DVR_SetConnectTime = hCNetSDK.NET_DVR_SetConnectTime
NET_DVR_SetConnectTime.restype = c_bool
NET_DVR_SetConnectTime.argtypes = (c_ulong, c_ulong)

NET_DVR_SetExceptionCallBack_V30 = hCNetSDK.NET_DVR_SetExceptionCallBack_V30
NET_DVR_SetExceptionCallBack_V30.restype = c_long
NET_DVR_SetExceptionCallBack_V30.argtypes = (c_uint, c_char, c_ulong, c_void_p)

NET_DVR_RealPlay_V40 = hCNetSDK.NET_DVR_RealPlay_V40
NET_DVR_RealPlay_V40.restype = c_long
NET_DVR_RealPlay_V40.argtypes = (c_long, POINTER(NET_DVR_PREVIEWINFO))

NET_DVR_RigisterDrawFun = hCNetSDK.NET_DVR_RigisterDrawFun
NET_DVR_RigisterDrawFun.restype = c_bool
NET_DVR_RigisterDrawFun.argtypes = (c_long, c_void_p, c_ushort)

NET_DVR_StopRealPlay = hCNetSDK.NET_DVR_StopRealPlay
NET_DVR_StopRealPlay.restype = c_bool
NET_DVR_StopRealPlay.argtypes = (c_ulong,)

NET_DVR_Logout = hCNetSDK.NET_DVR_Logout
NET_DVR_Logout.restype = c_bool
NET_DVR_Logout.argtypes = (c_ulong,)

NET_DVR_Cleanup = hCNetSDK.NET_DVR_Cleanup
NET_DVR_Cleanup.restype = c_bool
NET_DVR_Cleanup.argtypes = ()

NET_DVR_CaptureJPEGPicture = hCNetSDK.NET_DVR_CaptureJPEGPicture
NET_DVR_CaptureJPEGPicture.restype = c_bool

jpegpara = NET_DVR_JPEGPARA()
jpegpara.wPicSize = 0xff
jpegpara.wPicQuality = 2

# NET_DVR_GetDVRConfig = hCNetSDK.NET_DVR_GetDVRConfig
# NET_DVR_GetDVRConfig.restype = c_bool
# NET_DVR_GetDVRConfig.argtypes = (c_ulong, c_uint, c_ulong, c_void_p, c_ushort, c_uint)
########
# boolean NET_DVR_Logout_V30(NativeLong lUserID);
NET_DVR_Logout_V30 = hCNetSDK.NET_DVR_Logout_V30
NET_DVR_Logout_V30.restype = c_bool
NET_DVR_Logout_V30.argtypes = (c_long,)

# boolean NET_DVR_SetSTDConfig(NativeLong lUserID, int dwCommand, NET_DVR_STD_CONFIG lpInConfigParam);
NET_DVR_SetSTDConfig = hCNetSDK.NET_DVR_SetSTDConfig
NET_DVR_SetSTDConfig.restype = c_bool
# NET_DVR_SetSTDConfig.argtypes = (c_long, c_int32, POINTER(NET_DVR_STD_CONFIG))

# boolean NET_DVR_GetSTDConfig(NativeLong lUserID, int dwCommand, NET_DVR_STD_CONFIG lpOutConfigParam);
NET_DVR_GetSTDConfig = hCNetSDK.NET_DVR_GetSTDConfig
NET_DVR_GetSTDConfig.restype = c_bool
NET_DVR_GetSTDConfig.argtypes = (c_long, c_int32, POINTER(NET_DVR_SENSOR_ADJUSTMENT_INFO))

# boolean NET_DVR_CaptureJPEGPicture_WithAppendData(NativeLong lUserID, int lChannel, NET_DVR_JPEGPICTURE_WITH_APPENDDATA lpJpegWithAppend);
NET_DVR_CaptureJPEGPicture_WithAppendData = hCNetSDK.NET_DVR_CaptureJPEGPicture_WithAppendData
NET_DVR_CaptureJPEGPicture_WithAppendData.restype = c_bool
NET_DVR_CaptureJPEGPicture_WithAppendData.argtypes = (c_long, c_int32, POINTER(NET_DVR_JPEGPICTURE_WITH_APPENDDATA))

# int NET_DVR_GetLastError();
NET_DVR_GetLastError = hCNetSDK.NET_DVR_GetLastError
NET_DVR_GetLastError.restype = c_int32
NET_DVR_GetLastError.argtypes = ()

# 云台控制
NET_DVR_PTZControl = hCNetSDK.NET_DVR_PTZControl
NET_DVR_PTZControl.restype = c_bool
NET_DVR_PTZControl.argtypes = (c_long, c_ushort, c_ushort)

NET_DVR_PTZControlWithSpeed = hCNetSDK.NET_DVR_PTZControlWithSpeed

# 辅助聚焦
NET_DVR_FocusOnePush = hCNetSDK.NET_DVR_FocusOnePush

# 启用日志文件写入接口
# boolean NET_DVR_SetLogToFile(int bLogEnable, String strLogDir, boolean bAutoDel);
NET_DVR_SetLogToFile = hCNetSDK.NET_DVR_SetLogToFile
NET_DVR_SetLogToFile.restype = c_bool
NET_DVR_SetLogToFile.argtypes = (c_int32, c_char_p, c_bool)


# 单帧数据捕获并保存成JPEG存放在指定的内存空间中。

# BOOL NET_DVR_CaptureJPEGPicture_NEW(
#   LONG                 lUserID,
#   LONG                 lChannel,
#   LPNET_DVR_JPEGPARA   lpJpegPara,
#   char                 *sJpegPicBuffer,
#   DWORD                dwPicSize,
#   LPDWORD              lpSizeReturned
# );
NET_DVR_CaptureJPEGPicture_new = hCNetSDK.NET_DVR_CaptureJPEGPicture_NEW
NET_DVR_CaptureJPEGPicture_new.restype = c_bool
NET_DVR_CaptureJPEGPicture_new.argtypes = (c_long, c_long, POINTER(NET_DVR_JPEGPARA), c_char_p, c_ulong, POINTER(c_ulong))

# BOOL NET_DVR_CaptureJPEGPicture_NEW(
#   LONG                 lUserID,
#   LONG                 lChannel,
#   LPNET_DVR_JPEGPARA   lpJpegPara,
#   char                 *sJpegPicBuffer,
#   DWORD                dwPicSize,
#   LPDWORD              lpSizeReturned
# );
NET_DVR_CaptureJPEGPicture = hCNetSDK.NET_DVR_CaptureJPEGPicture
NET_DVR_CaptureJPEGPicture.restype = c_bool
NET_DVR_CaptureJPEGPicture.argtypes = (c_long, c_long, POINTER(NET_DVR_JPEGPARA), c_char_p)

def DisplayCBFun(nPort, pBuf, nSize, nWidth, nHeight, nStamp, nType, nReserved):
    # print(nWidth)
    # print(nReserved)
    '''
    显示回调函数
    '''

    # print(nWidth, nHeight)
# def bUseAsynLogin(lUserID, dwResult, lpDeviceInfo, pUser):
#     pass


def LoadPlayctrlSDK(sdkPath, windowsFlag):
    '''
    加载PlayctrlSDK库
    '''
    global Playctrldll
    if not windowsFlag:
        Playctrldll = cdll.LoadLibrary(sdkPath + r'/lib/libPlayCtrl.so')
    else:
        Playctrldll = WinDLL("./lib/PlayCtrl.dll")
    return Playctrldll

def Playctrl_Getport(Playctrldll):
    '''
    获取未使用的通道号
    '''
    Playctrldll.PlayM4_GetPort(byref(PLAYCTRL_PORT))

    if PLAYCTRL_PORT.value < 0:
        return False
    return True

# 码流回调数据类型
NET_DVR_SYSHEAD = 1
NET_DVR_STREAMDATA = 2
NET_DVR_AUDIOSTREAMDATA = 3
NET_DVR_PRIVATE_DATA = 112

# 码流回调函数
REALDATACALLBACK = functype(None, c_long, c_ulong, POINTER(c_ubyte), c_ulong, c_void_p)
ESREALDATACALLBACK = functype(c_int, c_void_p, LPNET_DVR_PACKET_INFO_EX, c_void_p)
# 码流回调函数 Linux
#REALDATACALLBACK = CFUNCTYPE(None, c_long, c_ulong, POINTER(c_ubyte), c_ulong, c_void_p)


# 云台控制命令
LIGHT_PWRON = 2  #接通灯光电源
WIPER_PWRON = 3  #接通雨刷开关
FAN_PWRON = 4  #接通风扇开关
HEATER_PWRON = 5  #接通加热器开关
AUX_PWRON1 = 6  #接通辅助设备开关
AUX_PWRON2 = 7  #接通辅助设备开关
ZOOM_IN = 11  #焦距变大(倍率变大)
ZOOM_OUT = 12  #焦距变小(倍率变小)
FOCUS_NEAR = 13  #焦点前调
FOCUS_FAR = 14  #焦点后调
IRIS_OPEN = 15  #光圈扩大
IRIS_CLOSE = 16  #光圈缩小
TILT_UP = 21  #云台上仰
TILT_DOWN = 22  #云台下俯
PAN_LEFT = 23  #云台左转
PAN_RIGHT = 24  #云台右转
UP_LEFT = 25  #云台上仰和左转
UP_RIGHT = 26  #云台上仰和右转
DOWN_LEFT = 27  #云台下俯和左转
DOWN_RIGHT = 28  #云台下俯和右转
PAN_AUTO = 29  #云台左右自动扫描
TILT_DOWN_ZOOM_IN = 58  #云台下俯和焦距变大(倍率变大)
TILT_DOWN_ZOOM_OUT = 59  #云台下俯和焦距变小(倍率变小)
PAN_LEFT_ZOOM_IN = 60  #云台左转和焦距变大(倍率变大)
PAN_LEFT_ZOOM_OUT = 61  #云台左转和焦距变小(倍率变小)
PAN_RIGHT_ZOOM_IN = 62  #云台右转和焦距变大(倍率变大)
PAN_RIGHT_ZOOM_OUT = 63  #云台右转和焦距变小(倍率变小)
UP_LEFT_ZOOM_IN = 64  #云台上仰和左转和焦距变大(倍率变大)
UP_LEFT_ZOOM_OUT = 65  #云台上仰和左转和焦距变小(倍率变小)
UP_RIGHT_ZOOM_IN = 66  #云台上仰和右转和焦距变大(倍率变大)
UP_RIGHT_ZOOM_OUT = 67  #云台上仰和右转和焦距变小(倍率变小)
DOWN_LEFT_ZOOM_IN = 68  #云台下俯和左转和焦距变大(倍率变大)
DOWN_LEFT_ZOOM_OUT = 69  #云台下俯和左转和焦距变小(倍率变小)
DOWN_RIGHT_ZOOM_IN = 70  #云台下俯和右转和焦距变大(倍率变大)
DOWN_RIGHT_ZOOM_OUT = 71  #云台下俯和右转和焦距变小(倍率变小)
TILT_UP_ZOOM_IN = 72  #云台上仰和焦距变大(倍率变大)
TILT_UP_ZOOM_OUT = 73  #云台上仰和焦距变小(倍率变小)