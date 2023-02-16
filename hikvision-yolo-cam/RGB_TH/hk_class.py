# Creater zch

from ctypes import *
from ctypes.wintypes import WORD, DWORD, BYTE

SERIALNO_LEN = 48  # 序列号长度
NAME_LEN = 32  # 用户名长度py
IP_MAX_LEN = 20  # IP域名长度

LPVOID = c_void_p
HANDLE = c_void_p
COLORKEY = c_int
COLORREF = c_int
HWND = c_uint

class NET_DVR_DEVICEINFO_V30(Structure):
    _fields_ = [
        ("sSerialNumber", c_byte * 48),  # 序列号
        ("byAlarmInPortNum", c_byte),  # 模拟报警输入个数
        ("byAlarmOutPortNum", c_byte),  # 模拟报警输出个数
        ("byDiskNum", c_byte),  # 硬盘个数
        ("byDVRType", c_byte),  # 设备类型，详见下文列表
        ("byChanNum", c_byte),  # 设备模拟通道个数，数字(IP)通道最大个数为byIPChanNum + byHighDChanNum*256
        ("byStartChan", c_byte),  # 模拟通道的起始通道号，从1开始。数字通道的起始通道号见下面参数byStartDChan
        ("byAudioChanNum", c_byte),  # 设备语音对讲通道数
        ("byIPChanNum", c_byte),
        # 设备最大数字通道个数，低8位，搞8位见byHighDChanNum. 可以根据ip通道个数是否调用NET_DVR_GetDVRConfig (配置命令NET_DVR_GET_IPPARACFG_V40)获得模拟和数字通道的相关参数
        ("byZeroChanNum", c_byte),  # 零通道编码个数
        ("byMainProto", c_byte),  # 主码流传输协议类型： 0 - private, 1 - rtsp, 2- 同时支持私有协议和rtsp协议去留（默认采用私有协议取流）
        ("bySubProto", c_byte),  # 字码流传输协议类型： 0 - private , 1 - rtsp , 2 - 同时支持私有协议和rtsp协议取流 （默认采用私有协议取流）

        # 能力，位与结果为0表示不支持，1
        # 表示支持
        # bySupport & 0x1，表示是否支持智能搜索
        # bySupport & 0x2，表示是否支持备份
        # bySupport & 0x4，表示是否支持压缩参数能力获取
        # bySupport & 0x8, 表示是否支持双网卡
        # bySupport & 0x10, 表示支持远程SADP
        # bySupport & 0x20, 表示支持Raid卡功能
        # bySupport & 0x40, 表示支持IPSAN目录查找
        # bySupport & 0x80, 表示支持rtp over rtsp
        ("bySupport", c_byte),
        # 能力集扩充，位与结果为0表示不支持，1
        # 表示支持
        # bySupport1 & 0x1, 表示是否支持snmp
        # v30
        # bySupport1 & 0x2, 表示是否支持区分回放和下载
        # bySupport1 & 0x4, 表示是否支持布防优先级
        # bySupport1 & 0x8, 表示智能设备是否支持布防时间段扩展
        # bySupport1 & 0x10, 表示是否支持多磁盘数（超过33个）
        # bySupport1 & 0x20, 表示是否支持rtsp over http
        # bySupport1 & 0x80, 表示是否支持车牌新报警信息，且还表示是否支持NET_DVR_IPPARACFG_V40配置
        ("bySupport1", c_byte),
        # 能力集扩充，位与结果为0表示不支持，1
        # 表示支持
        # bySupport2 & 0x1, 表示解码器是否支持通过URL取流解码
        # bySupport2 & 0x2, 表示是否支持FTPV40
        # bySupport2 & 0x4, 表示是否支持ANR(断网录像)
        # bySupport2 & 0x20, 表示是否支持单独获取设备状态子项
        # bySupport2 & 0x40, 表示是否是码流加密设备
        ("bySupport2", c_byte),
        ("wDevType", c_uint16),  # 设备型号，详见下文列表
        # 能力集扩展，位与结果：0 - 不支持，1 - 支持
        # bySupport3 & 0x1, 表示是否支持多码流
        # bySupport3 & 0x4, 表示是否支持按组配置，具体包含通道图像参数、报警输入参数、IP报警输入 / 输出接入参数、用户参数、设备工作状态、JPEG抓图、定时和时间抓图、硬盘盘组管理等
        # bySupport3 & 0x20,表示是否支持通过DDNS域名解析取流
        ("bySupport3", c_byte),
        # 是否支持多码流，按位表示，位与结果：0 - 不支持，1 - 支持
        # byMultiStreamProto & 0x1, 表示是否支持码流3
        # byMultiStreamProto & 0x2, 表示是否支持码流4
        # byMultiStreamProto & 0x40, 表示是否支持主码流
        # byMultiStreamProto & 0x80, 表示是否支持子码流
        ("byMultiStreamProto", c_byte),
        ("byStartDChan", c_byte),  # 起始数字通道号，0表示无数字通道，比如DVR或IPC
        ("byStartDTalkChan", c_byte),  # 起始数字对讲通道号，区别于模拟对讲通道号，0表示无数字对讲通道
        ("byHighDChanNum", c_byte),  # 数字通道个数，高8位

        # 能力集扩展，按位表示，位与结果：0 - 不支持，1 - 支持
        # bySupport4 & 0x01, 表示是否所有码流类型同时支持RTSP和私有协议
        # bySupport4 & 0x10, 表示是否支持域名方式挂载网络硬盘
        ("bySupport4", c_byte),
        # 支持语种能力，按位表示，位与结果：0 - 不支持，1 - 支持
        # byLanguageType == 0，表示老设备，不支持该字段
        # byLanguageType & 0x1，表示是否支持中文
        # byLanguageType & 0x2，表示是否支持英文
        ("byLanguageType", c_byte),

        ("byVoiceInChanNum", c_byte),  # 音频输入通道数
        ("byStartVoiceInChanNo", c_byte),  # 音频输入起始通道号，0表示无效
        ("byRes3", c_byte * 2),  # 保留，置为0
        ("byMirrorChanNum", c_byte),  # 镜像通道个数，录播主机中用于表示导播通道
        ("wStartMirrorChanNo", c_uint16),  # 起始镜像通道号
        ("byRes2", c_byte * 2)]  # 保留，置为0


class NET_DVR_DEVICEINFO_V40(Structure):
    _fields_ = [
        ("struDeviceV30", NET_DVR_DEVICEINFO_V30),  # 设备参数
        ("bySupportLock", c_byte),  # 设备是否支持锁定功能，bySuportLock 为1时，dwSurplusLockTime和byRetryLoginTime有效
        ("byRetryLoginTime", c_byte),  # 剩余可尝试登陆的次数，用户名，密码错误时，此参数有效

        # 密码安全等级： 0-无效，1-默认密码，2-有效密码，3-风险较高的密码，
        # 当管理员用户的密码为出厂默认密码（12345）或者风险较高的密码时，建议上层客户端提示用户名更改密码
        ("byPasswordLevel", c_byte),

        ("byProxyType", c_byte),  # 代理服务器类型，0-不使用代理，1-使用标准代理，2-使用EHome代理
        # 剩余时间，单位：秒，用户锁定时次参数有效。在锁定期间，用户尝试登陆，不算用户名密码输入对错
        # 设备锁定剩余时间重新恢复到30分钟
        ("dwSurplusLockTime", c_ulong),
        # 字符编码类型（SDK所有接口返回的字符串编码类型，透传接口除外）：
        # 0 - 无字符编码信息（老设备）
        # 1 - GB2312
        ("byCharEncodeType", c_byte),
        # 支持v50版本的设备参数获取，设备名称和设备类型名称长度扩展为64字节
        ("bySupportDev5", c_byte),
        # 登录模式（不同的模式具体含义详见"Remarks"说明：0- SDK私有协议，1- ISAPI协议）
        ("byLoginMode", c_byte),
        # 保留，置为0
        ("byRes2", c_byte * 253),
    ]


class NET_DVR_PREVIEWINFO(Structure):
    _fields_ = [('lChannel', c_long), ('dwStreamType', c_ulong), ('dwLinkMode', c_ulong), ('hPlayWnd', c_void_p),
                ('bBlocked', c_ulong), ('bPassbackRecord', c_ulong), ('byPreviewMode', c_ubyte), ('byStreamID', c_ubyte*32),
                ('byProtoType', c_ubyte), ('byRes1', c_ubyte), ('byVideoCodingType', c_ubyte), ('dwDisplayBufNum', c_ubyte),
                ('byNPQMode', c_ubyte), ('byRes', c_ubyte*215)]


class NET_DVR_USER_LOGIN_INFO(Structure):
    _fields_ = [
        ("sDeviceAddress", c_byte * 129),  # 设备地址，IP或者普通域名
        ("byUseTransport", c_byte),  # 是否启用能力透传 0：不启动，默认  1：启动
        ("wPort", c_uint16),  # 设备端口号
        ("sUserName", c_byte * 64),  # 登录用户名
        ("sPassword", c_byte * 64),  # 登录密码
        # ("fLoginResultCallBack",)  #

        ("bUseAsynLogin", c_bool),  # 是否异步登录, 0:否 1:是
        ("byProxyType", c_byte),  # 代理服务器类型：0- 不使用代理，1- 使用标准代理，2- 使用EHome代理

        # 是否使用UTC时间：
        # 0 - 不进行转换，默认；
        # 1 - 输入输出UTC时间，SDK进行与设备时区的转换；
        # 2 - 输入输出平台本地时间，SDK进行与设备时区的转换
        ("byUseUTCTime", c_byte),
        # 登录模式(不同模式具体含义详见“Remarks”说明)：
        # 0- SDK私有协议，
        # 1- ISAPI协议，
        # 2- 自适应（设备支持协议类型未知时使用，一般不建议）
        ("byLoginMode", c_byte),
        # ISAPI协议登录时是否启用HTTPS(byLoginMode为1时有效)：
        # 0 - 不启用，
        # 1 - 启用，
        # 2 - 自适应（设备支持协议类型未知时使用，一般不建议）
        ("byHttps", c_byte),
        # 代理服务器序号，添加代理服务器信息时相对应的服务器数组下表值
        ("iProxyID", c_long),
        # 保留，置为0
        ("byRes3", c_byte * 120),
    ]


class NET_DVR_Login_V40(Structure):
    _fields_ = [
        ("pLoginInfo", NET_DVR_USER_LOGIN_INFO),
        ("lpDeviceInfo", NET_DVR_DEVICEINFO_V40)
    ]


class NET_DVR_TIME(Structure):
    _fields_ = [('dwYear', c_int32), ('dwMonth', c_int32), ('dwDay', c_int32), ('dwHour', c_int32),
                ('dwMinute', c_int32), ('dwSecond', c_int32)]


class NET_DVR_JPEGPARA(Structure):
    _fields_ = [('PicSize', c_long), ('PicQuality', c_long)]


class NET_DVR_DEVICECFG(Structure):
    _fields_ = [('dwSize', c_ulong), ('sDVRName', c_ubyte*NAME_LEN), ('dwDVRID', c_ulong), ('dwRecycleRecord', c_long),
                ('sSerialNumber', c_ubyte*SERIALNO_LEN), ('dwSoftwareVersion', c_ulong), ('dwSoftwareBuildDate', c_ulong),
                ('dwDSPSoftwareVersion', c_ulong), ('dwDSPSoftwareBuildDate', c_ulong), ('dwPanelVersion', c_ulong),
                ('dwHardwareVersion', c_ulong), ('byAlarmInPortNum', c_ubyte), ('byAlarmOutPortNum', c_ubyte),
                ('byRS232Num', c_ubyte), ('byRS485Num', c_ubyte), ('byNetworkPortNum', c_ushort),
                ('byDiskCtrlNum', c_ubyte), ('byDiskNum', c_ubyte), ('byDVRType', c_ubyte), ('byChanNum', c_ubyte),
                ('byStartChan', c_ubyte), ('byDecordChans', c_ubyte), ('byVGANum', c_ubyte), ('byUSBNum', c_ubyte),
                ('byAuxoutNum', c_ubyte), ('byAudioNum', c_ubyte), ('byIPChanNum', c_ubyte)]


class NET_DVR_I_FRAME(Structure):
    _fields_ = [('dwSize', c_ulong), ('sStreamID', c_byte*48), ('dwChan', c_ulong),
                ('byStreamType', c_byte), ('byRes', c_byte*63)]

####
class NET_VCA_POINT(Structure):
    _fields_ = [('fX', c_float), ('fY', c_float)]


class NET_VCA_POLYGON(Structure):
    _fields_ = [('dwPointNum', c_ulong), ('struPos',NET_VCA_POINT * 10)]


class NET_DVR_THERMOMETRY_PRESETINFO_PARAM(Structure):
    _fields_ = [('byEnabled', c_byte), ('byRuleID', c_short), ('wDistance', c_short), ('fEmissivity', c_float),
                ('byDistanceUnit', c_byte), ('byRes', c_ubyte * 2), ('byReflectiveEnabled', c_byte),
                ('fReflectiveTemperature', c_float), ('szRuleName', c_ubyte * NAME_LEN), ('byRes1', c_ubyte * 63),
                ('byRuleCalibType', c_byte), ('struPoint', NET_VCA_POINT), ('struRegion', NET_VCA_POLYGON)]


class NET_DVR_THERMOMETRY_PRESETINFO(Structure):
    _fields_ = [('dwSize', c_ulong), ('wPresetNo', c_short), ('byRes', c_ubyte * 2),
                ('struPresetInfo', NET_DVR_THERMOMETRY_PRESETINFO_PARAM * 40)]


class NET_DVR_THERMOMETRY_COND(Structure):
    _fields_ = [('dwSize', c_ulong), ('dwChannel', c_ulong),
                ('wPresetNo', c_short), ('byRes', c_ubyte * 62)]


class BYTE_ARRAY(Structure):
    _fields_ = [('byValue', c_byte * 2097152)]


class NET_DVR_STD_CONFIG_THERMOETRY(Structure):
    _fields_ = [('lpCondBuffer', POINTER(NET_DVR_THERMOMETRY_COND)), ('dwCondSize', c_ulong),
                ('lpInBuffer', POINTER(NET_DVR_THERMOMETRY_PRESETINFO)), ('dwInSize', c_ulong),
                ('lpOutBuffer', POINTER(NET_DVR_THERMOMETRY_PRESETINFO)), ('dwOutSize', c_ulong),
                ('lpStatusBuffer', POINTER(BYTE_ARRAY)), ('dwStatusSize', c_ulong), ('lpXmlBuffer', c_void_p),
                ('dwXmlSize', c_ulong), ('byDataType', c_bool), ('byRes', c_ubyte * 23)]


class NET_DVR_SENSOR_ADJUSTMENT_INFO(Structure):
    _fields_ = [('dwSize', c_ulong), ('iPan', c_int), ('iTilt', c_int), ('iRotation', c_int),
                ('iFieldAngle', c_int), ('byRes', c_byte * 128)]


class NET_DVR_STD_CONFIG_SENSOR(Structure):
    _fields_ = [('lpCondBuffer', c_void_p), ('dwCondSize', c_ulong),
                ('lpInBuffer', POINTER(NET_DVR_SENSOR_ADJUSTMENT_INFO)), ('dwInSize', c_ulong),
                ('lpOutBuffer', POINTER(NET_DVR_SENSOR_ADJUSTMENT_INFO)), ('dwOutSize', c_ulong),
                ('lpStatusBuffer', POINTER(BYTE_ARRAY)), ('dwStatusSize', c_ulong), ('lpXmlBuffer', c_void_p),
                ('dwXmlSize', c_ulong), ('byDataType', c_bool), ('byRes', c_ubyte * 23)]


class NET_VCA_RECT(Structure):
    _fields_ = [('fX', c_char), ('fY', c_char), ('fWidth', c_char), ('fHeight', c_char)]


class NET_DVR_JPEGPICTURE_WITH_APPENDDATA(Structure):
    _fields_ = [('dwSize', c_int32), ('dwChannel', c_int32), ('dwJpegPicLen', c_int32), ('pJpegPicBuff', POINTER(BYTE_ARRAY)),
                ('dwJpegPicWidth', c_int32), ('dwJpegPicHeight', c_int32), ('dwP2PDataLen', c_int32),
                ('pP2PDataBuff', POINTER(BYTE_ARRAY)), ('byIsFreezedata', c_byte), ('byRes', c_byte * 255)]

# JPEG图像信息结构体。

# struct{
#   WORD     wPicSize;
#   WORD     wPicQuality;
# }NET_DVR_JPEGPARA,*LPNET_DVR_JPEGPARA;

class NET_DVR_JPEGPARA(Structure):
    _fields_ = [('wPicSize', c_ulong), ('wPicQuality', c_ulong)]


class NET_DVR_PACKET_INFO_EX(Structure):
    _fields_ = [
        ('wWidth', WORD),
        ('wHeight', WORD),
        ('dwTimeStamp', DWORD),
        ('dwTimeStampHigh', DWORD),
        ('dwYear', DWORD),
        ('dwMonth', DWORD),
        ('dwDay', DWORD),
        ('dwHour', DWORD),
        ('dwMinute', DWORD),
        ('dwSecond', DWORD),
        ('dwMillisecond', DWORD),
        ('dwFrameNum', DWORD),
        ('dwFrameRate', DWORD),
        ('dwFlag', DWORD),
        ('dwFilePos', DWORD),
        ('dwPacketType', DWORD),
        ('dwPacketSize', DWORD),
        ('pPacketBuffer', c_char_p),
        ('byRes1', BYTE * 4),
        ('dwPacketMode', DWORD),
        ('byRes2', BYTE * 16),
        ('dwReserved', DWORD * 6),
    ]

LPNET_DVR_PACKET_INFO_EX = POINTER(NET_DVR_PACKET_INFO_EX)