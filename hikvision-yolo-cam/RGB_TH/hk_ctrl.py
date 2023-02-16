# Creater zch
from RGB_TH.hk_dll import *
from RGB_TH.hk_thermal import *
import cv2
import time
import threading


rectangle = False
position1_rgb = None
position2_rgb = None
position1_th = None
position2_th = None
temperature = 0

win_name_the = 'thermal'

rgb_width = 1920  # RGB画面的宽（如果更改了RGB画面分辨率该参数也同步更改）
rgb_height = 1080  # RGB画面的高（同上）
th_width = 1280  # 热成像画面的宽（如果更改了热成像的画面分辨率该参数也同步更改）
th_height = 720  # 热成像画面的高（同上）
point1 = (295, 50)  # 可见光中可测温范围的左上角,在测温框内的x,y坐标都要减去这个点的x,y值
point2 = (1542, 967)  # 可见光中可测温范围的右下角,得出可见光画面内测温框的分辨率是(1247, 917)约等于(1250, 920)
rgb_th_width = 1250  # 可见光画面中测温范围的宽x
rgb_th_height = 920  # 可见光画面中测温范围的高y
rgb_to_th_x = th_width/rgb_th_width  # 可见光画面中测温范围的相对x坐标转换成热成像画面的x的比例
rgb_to_th_y = th_height/rgb_th_height  # 可见光画面中测温范围的相对y坐标转换成热成像画面的y的比例
th_to_rgb_x = rgb_th_width/th_width  # 热成像画面的x坐标转换成可见光画面中测温范围内的相对x的比例
th_to_rgb_y = rgb_th_height/th_height  # 热成像画面的x坐标转换成可见光画面中测温范围内的相对y的比例
distance = 3  # 测距:3m，用于校准双目摄像头之间的坐标误差
error_rate1 = 5.3*distance  # 双目摄像头标定的误差值，用于校准（公式并不完善），作用于左上角点
error_rate2 = 5.3*distance  # 双目摄像头标定的误差值，用于校准（公式并不完善），作用于右下角点

path = sys.argv[0].rsplit('/', 1)[0]  # 获取该脚本文件的所在目录
# print('path', path)


# 单次拍照
def capture(UserId, PlayHandle_RGB, PlayHandle_TH):
    global frame_rgb, frame_the, rectangle, point_rgb, position1_rgb, position2_rgb, temperature,\
        lRealPlayHandle_TH, lRealPlayHandle_RGB, lUserId
    # 将输入的参数变为全局变量
    lUserId = UserId
    lRealPlayHandle_RGB = PlayHandle_RGB
    lRealPlayHandle_TH = PlayHandle_TH

    jpgname = path + "/pic/frame_rgb.jpg"
    # 云摄像头拍照并保存路径为jpgname
    suss1 = hCNetSDK.NET_DVR_CaptureJPEGPicture(lUserId, 1, byref(jpegpara), bytes(jpgname, 'utf-8'))
    jpgname_the = path + "/pic/frame_thermal.jpg"
    # 云摄像头拍照并保存路径为jpgname_the
    suss2 = hCNetSDK.NET_DVR_CaptureJPEGPicture(lUserId, 2, byref(jpegpara), bytes(jpgname_the, 'utf-8'))

    if suss1 == 0:
        print(NET_DVR_GetLastError())
        print("可见光抓图不成功")
    if suss2 == 0:
        print(NET_DVR_GetLastError())
        print("热成像抓图不成功")

    frame_rgb = cv2.imread(jpgname)
    # 可见光画面中的测温框，point1, point2是对应的左上角点和右下角点, (255, 215, 0)是框颜色， 2：框大小
    cv2.rectangle(frame_rgb, point1, point2, (255, 215, 0), 2)
    # cv2.rectangle(frame_rgb, (790, 380), (1050, 640), (255, 215, 0), 2)
    #  中心点(1083, 561)
    # 保存添加了测温框的图像
    pic = path + '/pic/frame_rgb_addrect.jpg'
    cv2.imwrite(pic, frame_rgb)

    # 登出设备
    NET_DVR_Logout(lUserId)
    # 释放资源
    NET_DVR_Cleanup()
    return pic


#  对cam_rgb函数设置线程，手动模式的cv画面
def cam_thread(lUserId, PlayHandle_RGB):
    t_cam = threading.Thread(target=cam_rgb, args=[lUserId, PlayHandle_RGB])
    t_cam.start()
    t_cam.join()


#  可见光画面的连续拍照模块
def cam_rgb(UserId, PlayHandle_RGB):
    global lUserId, frame_rgb, frame_the, rectangle, point_rgb, position1_rgb, position2_rgb, temperature, lRealPlayHandle_RGB

    lRealPlayHandle_RGB = PlayHandle_RGB
    lUserId = UserId

    win_name_rgb = 'rgb'
    # 本台电脑bug:创建新线程时会在这一步卡死
    # print(0)
    cv2.namedWindow(win_name_rgb, 0)
    # print(1)
    cv2.resizeWindow(win_name_rgb, 720, 520)
    cv2.setMouseCallback(win_name_rgb, event_rgb)
    while True:
        jpgname = path + "/pic/frame_rgb.jpg"
        # 云摄像头拍照并保存路径为jpgname
        suss = hCNetSDK.NET_DVR_CaptureJPEGPicture(lUserId, 1, byref(jpegpara), bytes(jpgname, 'utf-8'))
        frame_rgb = cv2.imread(jpgname)

        # 可见光画面中的测温框，point1, point2是对应的左上角点和右下角点, (255, 215, 0)是框颜色， 2：框大小
        cv2.rectangle(frame_rgb, point1, point2, (255, 215, 0), 2)
        # cv2.rectangle(frame_rgb, (790, 380), (1050, 640), (255, 215, 0), 2)
        #  中心点(1083, 561)

        # 当ALT+左键时的操作
        if rectangle == True:
            # rgb_point = [[x1, y1], [x2, y2]]
            if temperature != None:
                temperature = float(temperature)
                temperature = '%.2f' % temperature
                temperature = str(temperature)
                cv2.rectangle(frame_rgb, point_rgb[0], point_rgb[1], (0, 0, 255), 2)
                cv2.putText(frame_rgb, temperature, point_rgb[0], cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)
        # 当鼠标按住有移动或点击一次（移动距离0）时
        if position1_rgb != None and position2_rgb != None:
            rectangle = False
            cv2.rectangle(frame_rgb, position1_rgb, position2_rgb, (0, 0, 255), 2)
            if temperature != None:
                temperature = float(temperature)
                temperature = '%.2f' % temperature
                temperature = str(temperature)
                cv2.putText(frame_rgb, temperature, position1_rgb, cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 2)

        cv2.imshow(win_name_rgb, frame_rgb)
        if suss == 0:
            print(NET_DVR_GetLastError())
            print("抓图不成功")

        k = cv2.waitKeyEx(1) & 0xff
        if k == ord('q') or k == ord('Q') or k == 27:
            cv2.destroyAllWindows()
            # 登出设备
            NET_DVR_Logout(lUserId)
            # 释放资源
            NET_DVR_Cleanup()
            print('退出')
            break
    return temperature


#  热成像画面的连续拍照模块
def cam_thermal(lUserId, PlayHandle_TH):
    global frame_rgb, frame_the, rectangle, point_th, position1_th, position2_th, temperature, lRealPlayHandle_TH
    lRealPlayHandle_TH = PlayHandle_TH
    cv2.namedWindow(win_name_the, 0)
    cv2.resizeWindow(win_name_the, 720, 520)
    cv2.setMouseCallback(win_name_the, event_th)

    while True:
        jpgname_the = path + "/pic/frame_thermal.jpg"
        # 云摄像头拍照并保存路径为jpgname_the
        suss = hCNetSDK.NET_DVR_CaptureJPEGPicture(lUserId, 2, byref(jpegpara), bytes(jpgname_the, 'utf-8'))

        frame_the = cv2.imread(jpgname_the)
        # cv2.resize(frame_the, (640, 512))
        # 当ALT+左键时的操作
        if rectangle == True:
            # rgb_point = [[x1, y1], [x2, y2]]
            if temperature != None:
                temperature = float(temperature)
                temperature = '%.2f' % temperature
                temperature = str(temperature)
                cv2.rectangle(frame_the, point_th[0], point_th[1], (255, 255, 255), 2)
                cv2.putText(frame_the, temperature, point_th[0], cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

        # 当鼠标按住有移动或点击一次（移动距离0）时
        if position1_th != None and position2_th != None:
            cv2.rectangle(frame_the, position1_th, position2_th, (255, 255, 255), 2)
            if temperature != None:
                temperature = float(temperature)
                temperature = '%.2f' % temperature
                temperature = str(temperature)
                cv2.putText(frame_the, temperature, position1_th, cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)

        cv2.imshow('thermal', frame_the)
        # print('yes 2')

        if suss == 0:
            print("抓图不成功")

        k = cv2.waitKeyEx(1) & 0xff
        if k == ord('q') or k == ord('Q') or k == 27:
            cv2.destroyAllWindows()
            # 登出设备
            NET_DVR_Logout(lUserId)
            # 释放资源
            NET_DVR_Cleanup()
            print('退出')
            break


# 给定数据集进行测温
def temp(temp_data, pic):
    global rectangle, point_rgb, point_th, position1_rgb, position2_rgb, position1_th, position2_th, temperature

    if pic != None:
        pic_frame = cv2.imread(pic)
        frame_rgb = pic_frame
        frame_th = cv2.imread(path + '/pic/frame_thermal.jpg')
        for data in temp_data:
            # temp_data: [[(左上角坐标), (右下角坐标), 标签名称], ...]
            print('\n')
            position1 = data[0]  # 左上角坐标
            position2 = data[1]  # 右下角坐标
            name = data[2]  # 预测后的标签名称

            x1, y1 = position1[0], position1[1]
            x2, y2 = position2[0], position2[1]
            # 判断坐标是否超出界限
            # 如果在传入数据之前就对坐标进行判断和转换了则可以注释以下判断
            # x1 = point1[0] if x1 < point1[0] else x1
            # y1 = point1[1] if y1 < point1[1] else y1
            # x1 = point2[0] if x1 > point2[0] else x1
            # y1 = point2[1] if y1 > point2[1] else y1
            #
            # x2 = point1[0] if x2 < point1[0] else x2
            # y2 = point1[1] if y2 < point1[1] else y2
            # x2 = point2[0] if x2 > point2[0] else x2
            # y2 = point2[1] if y2 > point2[1] else y2

            print('误差值:', error_rate1, error_rate2, '误差距离:', distance)
            # position1_th, position2_th, rgb中测温范围内相对坐标转换成热成像画面坐标
            position1_th = [round((x1 - point1[0] - error_rate1) * rgb_to_th_x), round((y1 - point1[1]) * rgb_to_th_y)]
            position2_th = [round((x2 - point1[0] - error_rate2) * rgb_to_th_x), round((y2 - point1[1]) * rgb_to_th_y)]
            # 将处于边界的坐标转换成热成像坐标时也是边界坐标
            position1_th[0] = 0 if x1 <= point1[0] else position1_th[0]
            position1_th[1] = 0 if y1 <= point1[1] else position1_th[1]
            position2_th[0] = 0 if x2 <= point1[0] else position2_th[0]
            position2_th[1] = 0 if y2 <= point1[1] else position2_th[1]
            position1_th[0] = th_width if x1 >= point2[0] else position1_th[0]
            position1_th[1] = th_height if y1 >= point2[1] else position1_th[1]
            position2_th[0] = th_width if x2 >= point2[0] else position2_th[0]
            position2_th[1] = th_height if y2 >= point2[1] else position2_th[1]


            print('RGB图对角坐标:', position1, position2)
            print('th图对角坐标:', position1_th, position2_th)
            if position1 != None:
                # 将热成像坐标统一为左上角(x1, y1)到右下角(x2, y2)
                position1_thermal = [position1_th[0], position1_th[1]]
                position2_thermal = [position2_th[0], position2_th[1]]
                if position1_thermal[0] > position2_thermal[0]:
                    position1_thermal[0], position2_thermal[0] = position2_thermal[0], position1_thermal[0]
                if position1_thermal[1] > position2_thermal[1]:
                    position1_thermal[1], position2_thermal[1] = position2_thermal[1], position1_thermal[1]

                rgb_point_th = (position1_thermal, position2_thermal)  # 在测温范围内所框选的范围坐标(左上,右下)
                # print('rgb图内的测温范围相对坐标对应的热成像对角坐标:', rgb_point_th)

                # rgb_point_th:热成像对角坐标, (th_width, th_height)热成像画面分辨率(th_width=1280, th_height=720), id
                print('测温范围:{}, 热成像分辨率:{},{}, id:{}'.format(rgb_point_th, th_width, th_height, lUserId))
                result, temperature, temperature_list, mean_temp = get_temperature_max(rgb_point_th, th_width, th_height, lUserId)

                # print(result)
                if result:
                    print('测温结果:', temperature)
                    # print('测温矩阵:', temperature_list)
                    position1, position2 = tuple(position1), tuple(position2)
                    position1_thermal, position2_thermal = tuple(position1_thermal), tuple(position2_thermal)
                    cv2.rectangle(frame_rgb, position1, position2, (0, 37, 139), 2)
                    cv2.rectangle(frame_th, position1_thermal, position2_thermal, (0, 0, 0), 2)
                    if position1_thermal[1] <= 35:  # 防止文本框写出图片范围外
                        position1_thermal_text = [position1_thermal[0] + 10, position1_thermal[1] + 33]
                        position1_thermal_text = tuple(position1_thermal_text)
                    else:
                        position1_thermal_text = [position1_thermal[0], position1_thermal[1]]
                        position1_thermal_text = tuple(position1_thermal_text)
                    if temperature != None:
                        temperature = float(temperature)
                        temperature = '%.2f' % temperature
                        temperature = str(temperature)
                        text = '{} temp:{}'.format(name, temperature)

                        # cv2.putText(frame_rgb, text, position1, cv2.FONT_HERSHEY_SIMPLEX, 2.0, (205, 0, 0), 2)
                        lw = 3
                        tf = max(lw - 1, 1)
                        w, h = cv2.getTextSize(text, 0, fontScale=2, thickness=tf)[0]  # text width, height
                        outside = position1[1] - h - 3 >= 0  # label fits outside box
                        test_p2 = position1[0] + w, position1[1] - h - 3 if outside else position1[1] + h + 3
                        # RGB画面的字体说明矩形框
                        cv2.rectangle(frame_rgb, position1, test_p2, (255, 0, 255), -1, cv2.LINE_AA)  # filled
                        cv2.putText(frame_rgb,
                                    text, (position1[0], position1[1] - 2 if outside else position1[1] + h + 2),
                                    0,
                                    2,
                                    (255, 255, 255),
                                    thickness=tf,
                                    lineType=cv2.LINE_AA)

                        # 热成像画面的字体说明矩形框
                        # cv2.rectangle(frame_th, position1_thermal_text, test_p2, (255, 0, 255), -1, cv2.LINE_AA)  # filled
                        cv2.putText(frame_th,
                                    text, position1_thermal_text,
                                    0,
                                    1.5,
                                    (255, 255, 255),
                                    thickness=tf,
                                    lineType=cv2.LINE_AA)

                        # cv2.putText(frame_th, text, position1_thermal_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 10), 2)
                else:
                    print('测温失败')

        # 保存图片
        pic = path + '/pic/pred_temp.jpg'
        th_pic = path + '/pic/pred_temp_thermal.jpg'
        cv2.imwrite(pic, frame_rgb)
        cv2.imwrite(th_pic, frame_th)

        # 登出设备
        NET_DVR_Logout(lUserId)
        # 释放资源
        NET_DVR_Cleanup()
        temp_set = {'temperature': temperature, 'list': temperature_list, 'mean_temp': mean_temp}
        return pic, th_pic, temp_set

    else:
        # 登出设备
        NET_DVR_Logout(lUserId)
        # 释放资源
        NET_DVR_Cleanup()
        print('没有图像')
        pic, th_pic, temperature, temperature_list, mean_temp = None, None, None, None, None
        temp_set = {'temperature': temperature, 'list': temperature_list, 'mean_temp': mean_temp}
        return pic, th_pic, temp_set


#  可见光画面的操作控制模块
def event_rgb(event, x, y, flags, param):
    global lUserId, rectangle, frame, point_rgb, point_th, position1_rgb, position2_rgb, position1_th, position2_th, temperature

    # alt+左键:标记坐标并测温,画一个正方形100x100的范围
    if flags == (cv2.EVENT_FLAG_ALTKEY + cv2.EVENT_FLAG_LBUTTON):
        print(x, y)
        #  划定一个100x100的范围
        if x-50 <= point1[0]:
            x = point1[0]+50

        if y-50 <= point1[1]:
            y = point1[1]+50

        if x+50 >= point2[0]:
            x = point2[0]-50

        if y+50 >= point2[1]:
            y = point2[1]-50

        x1 = x-50
        y1 = y-50
        x2 = x+50
        y2 = y+50
        # rgb画面中测温范围相对坐标转换成热成像画面坐标
        x1_th = round((x1 - point1[0]) * rgb_to_th_x)
        y1_th = round((y1 - point1[1]) * rgb_to_th_y)
        x2_th = round((x2 - point1[0]) * rgb_to_th_x)
        y2_th = round((y2 - point1[1]) * rgb_to_th_y)

        point_rgb = ((x1, y1), (x2, y2))
        point_th = ((x1_th, y1_th), (x2_th, y2_th))
        rectangle = True
        print('rgb_point', point_rgb)
        print('th_point', point_th)

        # 鼠标所点的坐标，rgb图像的分辨率(rgb_width=1920, rgb_height=1080)，id
        result, temperature, temperature_list = get_temperature_max(point_rgb, rgb_width, rgb_height, lUserId)
        if result:
            print('测温结果:', temperature)
            # print('测温矩阵:', temperature_list)
        else:
            print('测温失败')

    # 鼠标左键点击或者按住
    elif event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        # (790, 380), (1050, 640)
        # 当在这个矩形范围内时，误差调整
        print('point1:', x1, y1)

        # 当超出测温框时
        x1 = point1[0] if x1 < point1[0] else x1
        y1 = point1[1] if y1 < point1[1] else y1
        x1 = point2[0] if x1 > point2[0] else x1
        y1 = point2[1] if y1 > point2[1] else y1

        position1_rgb = (x1, y1)
        print('position1_rgb:', position1_rgb)
        # position1, rgb中测温范围内相对坐标转换成热成像画面坐标
        position1_th = (round((x1-point1[0]) * rgb_to_th_x), round((y1-point1[1]) * rgb_to_th_y))
        position2_rgb = None
        position2_th = None

    #  鼠标左键按住移动
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        rectangle = False
        x2, y2 = x, y

        # 判断是否超出测温边界
        x2 = point1[0] if x2 < point1[0] else x2
        y2 = point1[1] if y2 < point1[1] else y2
        x2 = point2[0] if x2 > point2[0] else x2
        y2 = point2[1] if y2 > point2[1] else y2


        position2_rgb = (x2, y2)
        # position2, rgb中测温范围内相对坐标转换成热成像画面坐标
        position2_th = (round((x2-point1[0]) * rgb_to_th_x), round((y2-point1[1]) * rgb_to_th_y))

    #  鼠标左键松开
    elif event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        print('point2:', x2, y2)
        # 判断是否超出测温边界
        x2 = point1[0] if x2 < point1[0] else x2
        y2 = point1[1] if y2 < point1[1] else y2
        x2 = point2[0] if x2 > point2[0] else x2
        y2 = point2[1] if y2 > point2[1] else y2


        # 先停止云台控制，如果没有云台功能也无影响
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_RGB, PAN_LEFT, 1, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
            if NET_DVR_GetLastError() == 12:
                lRet = 1

        if lRet != 0:
            position2_rgb = (x2, y2)
            print('position2_rgb', position2_rgb)
            # temp(position1_rgb, position2_rgb, pic=None)
            # position2, rgb中测温范围内相对坐标转换成热成像画面坐标
            position2_th = (round((x2-point1[0]) * rgb_to_th_x), round((y2-point1[1]) * rgb_to_th_y))
            print('RGB图对角坐标:', position1_rgb, position2_rgb)
            print('th图对角坐标:', position1_th, position2_th)
            if position1_rgb != None:
                # 将热成像坐标统一为左上角(x1, y1)到右下角(x2, y2)
                position1_thermal = [position1_th[0], position1_th[1]]
                position2_thermal = [position2_th[0], position2_th[1]]
                if position1_thermal[0] > position2_thermal[0]:
                    position1_thermal[0], position2_thermal[0] = position2_thermal[0], position1_thermal[0]
                if position1_thermal[1] > position2_thermal[1]:
                    position1_thermal[1], position2_thermal[1] = position2_thermal[1], position1_thermal[1]

                rgb_point_th = (position1_thermal, position2_thermal)  # 在测温范围内所框选的范围坐标(左上,右下)

                print('rgb图内的测温范围相对坐标对应的热成像对角坐标:', rgb_point_th)

                # rgb_point_th:热成像对角坐标, (th_width, th_height)热成像画面分辨率(th_width=1280, th_height=720), id
                print('test:', rgb_point_th, th_width, th_height, lUserId)
                result, temperature, temperature_list, temperature_mean = get_temperature_max(rgb_point_th, th_width, th_height, lUserId)
                if result:
                    print('测温结果:', temperature)
                    # print('测温矩阵:', temperature_list)
                else:
                    print('测温失败')


    # Ctrl+左键:左转
    if flags == (cv2.EVENT_FLAG_LBUTTON + cv2.EVENT_FLAG_CTRLKEY):
        TRUN = True
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


#  热成像画面的操作控制模块
def event_th(event, x, y, flags, param):
    global lUserId, rectangle, frame, point_th, point_rgb, position1_rgb, position2_rgb, position1_th, position2_th, temperature

    # ALT+左键:标记坐标并测温
    if flags == (cv2.EVENT_FLAG_ALTKEY + cv2.EVENT_FLAG_LBUTTON):
        print(x, y)
        #  划定一个100x100的范围
        if x-50 <= 0:
            x = 50

        if y-50 <= 0:
            y = 50

        if x+50 >= th_width:
            x = th_width-50

        if y+50 >= th_height:
            y = th_height-50

        x1 = x-50
        y1 = y-50
        x2 = x+50
        y2 = y+50
        # 热成像画面坐标转换成rgb画面中测温范围内的相对坐标
        x1_rgb = round(x1 * th_to_rgb_x + point1[0])
        y1_rgb = round(y1 * th_to_rgb_y + point1[1])
        x2_rgb = round(x2 * th_to_rgb_x + point1[0])
        y2_rgb = round(y2 * th_to_rgb_y + point1[1])

        point_th = ((x1, y1), (x2, y2))
        point_rgb = ((x1_rgb, y1_rgb), (x2_rgb, y2_rgb))
        rectangle = True
        print('the_point', point_th)
        print('rgb_point', point_rgb)

        # 鼠标所点的坐标，热成像图像的分辨率(th_width, th_height)(1280, 720)，id
        result, temperature, temperature_list = get_temperature_max(point_th, th_width, th_height, lUserId)
        if result:
            print('测温结果:', temperature)
            # print('测温矩阵:', temperature_list)
        else:
            print('测温失败')

    #  鼠标左键点击或按住
    elif event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        position1_th = (x1, y1)
        # position1, 热成像坐标转换成可见光画面中测温范围内的相对坐标
        position1_rgb = (round(x1 * th_to_rgb_x + point1[0]), round(y1 * th_to_rgb_y + point1[1]))
        position2_rgb = None
        position2_th = None

    #  鼠标左键按住移动
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        rectangle = False
        x2, y2 = x, y
        if x2 >= th_width:
            x2 = th_width
        if y2 >= th_height:
            y2 = th_height
        position2_th = (x2, y2)
        # position2, 热成像坐标转换成可见光画面中测温范围内的相对坐标
        position2_rgb = (round(x2 * th_to_rgb_x + point1[0]), round(y2 * th_to_rgb_y + point1[1]))

    #  鼠标左键松开
    elif event == cv2.EVENT_LBUTTONUP:
        # 停止云台控制
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, PAN_LEFT, 1, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())

        x2, y2 = x, y
        if x2 >= th_width:
            x2 = th_width
        if y2 >= th_height:
            y2 = th_height
        position2_th = (x2, y2)
        # position2, 热成像坐标转换成可见光画面中测温范围内的相对坐标
        position2_rgb = (round(x2 * th_to_rgb_x + point1[0]), round(y2 * th_to_rgb_y + point1[1]))
        print('热成像图对角坐标:', position1_th, position2_th)
        print('RGB图对角坐标:', position1_rgb, position2_rgb)
        if position1_th != None:
            # 将热成像坐标统一为左上角(x1, y1)到右下角(x2, y2)
            position1_thermal = [position1_th[0], position1_th[1]]
            position2_thermal = [position2_th[0], position2_th[1]]
            if position1_thermal[0] > position2_thermal[0]:
                position1_thermal[0], position2_thermal[0] = position2_thermal[0], position1_thermal[0]
            if position1_thermal[1] > position2_thermal[1]:
                position1_thermal[1], position2_thermal[1] = position2_thermal[1], position1_thermal[1]

            point_th = [position1_thermal, position2_thermal]
            # point_th:热成像对角坐标, (th_width, th_height)热成像画面分辨率(th_width, th_height)(1280, 720), id
            result, temperature, temperature_list = get_temperature_max(point_th, th_width, th_height, lUserId)
            if result:
                print('测温结果:', temperature)
                # print('测温矩阵:', temperature_list)
            else:
                print('测温失败')


    # Ctrl+左键:左转
    if flags == (cv2.EVENT_FLAG_LBUTTON + cv2.EVENT_FLAG_CTRLKEY):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, PAN_LEFT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 左转控制')
        # 停止云台控制
        time.sleep(0.02)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, PAN_LEFT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # Ctrl+右键:右转
    if flags == (cv2.EVENT_FLAG_RBUTTON + cv2.EVENT_FLAG_CTRLKEY):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, PAN_RIGHT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 右转控制')
        # 停止云台控制
        time.sleep(0.04)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, PAN_RIGHT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # Ctrl+左键长按:左持续转
    if flags == (cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_LBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, PAN_LEFT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 左持续转')

    # Ctrl+右键长按:右持续转
    if flags == (cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_FLAG_RBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, PAN_RIGHT, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 右持续转')

    # 右键放起:停止
    if event == cv2.EVENT_RBUTTONUP:
        print('stop')
        # 停止云台控制
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, PAN_RIGHT, 1, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # SHIFT+左键:上仰
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_FLAG_LBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, TILT_UP, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 上仰')
        # 停止云台控制
        time.sleep(0.04)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, PAN_RIGHT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # SHIFT+右键:下俯
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_FLAG_RBUTTON):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, TILT_DOWN, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 下俯')
        # 停止云台控制
        time.sleep(0.04)
        lRet = NET_DVR_PTZControl(lRealPlayHandle_TH, PAN_RIGHT, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # SHIFT+左键长按:上仰持续
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_LBUTTONDOWN):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, TILT_UP, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 上仰持续')

    # SHIFT+右键长按:下俯持续
    if flags == (cv2.EVENT_FLAG_SHIFTKEY + cv2.EVENT_RBUTTONDOWN):
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, TILT_DOWN, 0, 1)
        if lRet == 0:
            print('Start ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            print('ptz 下俯持续')

    # Ctrl+中键放起:停止
    if flags == (cv2.EVENT_FLAG_CTRLKEY + cv2.EVENT_MBUTTONDOWN):
        # 停止云台控制
        lRet = NET_DVR_PTZControlWithSpeed(lRealPlayHandle_TH, PAN_RIGHT, 1, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is:', NET_DVR_GetLastError())
        else:
            pass

    # 滚轮向后:缩小
    if event == cv2.EVENT_MOUSEWHEEL and flags < 0:
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

    # 滚轮向前:放大
    if event == cv2.EVENT_MOUSEWHEEL and flags > 0:
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