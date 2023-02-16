# Creater zch

from RGB_TH.hk_sdk import *
import RGB_TH.hk_ctrl


lRealPlayHandle_RGB = None
def cam_start(mode, temp_data, PIC_path, cam_msg):
    # mode=0,1,2  0:只拍照，1:传入已识别后的数据集和图片根据数据集的内容进行测温，2:手动测温模式(未测试)
    global lUserId
    init()
    ip = cam_msg['ip']
    port = 8000
    name = cam_msg['name']
    pwd = cam_msg['pwd']

    # 登录设备
    # DEV_IP = create_string_buffer(b'192.168.201.16')
    # DEV_PORT = 8000
    # DEV_USER_NAME = create_string_buffer(b'admin')
    # DEV_PASSWORD = create_string_buffer(b'abc12345')

    lUserId = login(ip, port, name, pwd)
    if lUserId < 0:
        print('Login device fail, error code is:', NET_DVR_GetLastError())
        # 释放资源
        NET_DVR_Cleanup()
        exit()


    # 定义码流回调函数
    funcRealDataCallBack_V30_RGB = REALDATACALLBACK(RealDataCallBack_V30_RGB)
    funcRealDataCallBack_V30_TH = REALDATACALLBACK(RealDataCallBack_V30_TH)
    # 开启预览
    ESRealDataCallBack_V30 = ESREALDATACALLBACK(ESDataCallBack_V30)
    lRealPlayHandle_RGB = OpenPreview_1(lUserId, funcRealDataCallBack_V30_RGB)
    lRealPlayHandle_TH = OpenPreview_2(lUserId, funcRealDataCallBack_V30_TH)

    if mode == 0:
        capture = RGB_TH.hk_ctrl.capture
        # 设置线程显示画面
        # cam_rgb = RGB_TH.hk_ctrl.cam_rgb(lUserId, lRealPlayHandle_RGB)
        # cam_thermal = RGB_TH.hk_ctrl.cam_thermal
        # thread_rgb = threading.Thread(target=cam_rgb, args=[lUserId, lRealPlayHandle_RGB, ])
        # thread_the = threading.Thread(target=cam_thermal, args=[lUserId, lRealPlayHandle_TH, ])

        # thread_rgb.start()
        # thread_rgb.join()

        PIC = capture(lUserId, lRealPlayHandle_RGB, lRealPlayHandle_TH)

        return PIC
    if mode == 1:
        # PIC:测温后的rgb图, pred_temp_thermal:测温后的热成像图, temp:最高温, temp_list:矩形范围内所有测温温度列表
        PIC, pred_temp_thermal, temp_set = RGB_TH.hk_ctrl.temp(temp_data, PIC_path)
        print('\n')
        # temp_set:测温后的数据集（可自定义设置）
        return PIC, pred_temp_thermal, temp_set

    if mode == 2:  # 手动测温模式，即点击测温直接cv2一直展示摄像头画面，并可框选测温
        print('mode=2')
        # bug:可能在app上已经展示的video的线程，再打开新的cv线程会导致新的cv卡死，这个电脑的打开多个cv画面bug
        cam_rgb = RGB_TH.hk_ctrl.cam_thread(lUserId, lRealPlayHandle_RGB)
        return cam_rgb