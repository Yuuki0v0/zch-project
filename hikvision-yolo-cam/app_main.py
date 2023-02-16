#!/usr/bin/env python3
# import rospy
# from std_msgs.msg import String

# Creater zch
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import sys
import cv2

from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import threading

import yolov5_master.detect_app as detect_app
import yolov5_master.detect_video as detect_video
from sound import sound
import RGB_TH.hk_main as hk_main


app = Flask(__name__)  # 实例化，可视为固定格式
app.debug = True  # Flask内置了调试模式，可以自动重载代码并显示调试信息
app.config['JSON_AS_ASCII'] = False  # 解决flask接口中文数据编码问题

# 设置可跨域范围
CORS(app, supports_credentials=True)

# 默认参数设置None
model1 = None
img_stream = None
img_stream2 = None
File_path = None
predict_outcome = None
pred_temp = None
pred_temp_thermal = None
load_model = None

temp_point1 = (295, 50)  # 可见光中热成像画面的左上角,在热成像框内的x,y坐标都要减去这个点的x,y值
temp_point2 = (1542, 967)  # 可见光中热成像画面的右下角,得出可见光画面内热成像画面的分辨率是(1247, 917)约等于(1250, 920)
path = sys.argv[0].rsplit('/', 1)[0]  # 读取该py文件所在的路径父目录

# 海康摄像头信息
hkip = '192.168.201.16'
hkname = 'admin'
hkpwd = 'abc12345'
rtsp_url = 'rtsp://{}:{}@{}/h264/ch1/main/av_stream'.format(hkname, hkpwd, hkip)  # 摄像头取流
firefox_driver_url = '/home/u20/project/driver/geckodriver'  # 火狐浏览器驱动地址


# 展示Flask如何读取服务器本地图片, 并返回图片流给前端显示的例子
def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
    return img_stream


# 点击'浏览'后选取文件读取文件路径
def getLocalFile():
    root = tk.Tk()
    root.withdraw()

    filePath = filedialog.askopenfilename()
    root.destroy()
    return filePath


# 页面初始化
@app.route('/')
def hello_world():
    return render_template('app_main.html')


# 浏览文件
@app.route('/Browse', methods=['POST'])  # 浏览文件路径
def Browse():
    global File_path, img_stream, img_stream2, pred_temp, pred_temp_thermal
    File_path = getLocalFile()
    print('文件路径：', File_path)
    return render_template('app_main.html', img_stream2=pred_temp, img_stream3=pred_temp_thermal, file_path=File_path)


# 声音模型预测
@app.route('/predict', methods=['POST'])
def predict():
    global img_stream, img_stream2, File_path, pred_temp, pred_temp_thermal
    if File_path is not None:  #如果浏览路径
        File_path_type = File_path.rsplit('.', 1)[1]  # 切片文件选取文件格式
        print(File_path_type)
        if File_path_type != 'wav':  # 如果选择的文件不是wav格式
            predict_outcome = '请重新选择一个音频文件'

        if File_path_type == 'wav':  # 选择wav格式的文件后
            # 声音模型文件
            file1 = path + '/sound/saved_models/final_model.hdf5'
            model1 = sound.model_load(file1)
            filename = File_path
            predict_outcome, total_time = sound.model_pred(filename)
            print('total_time:', total_time)

    else:  # 如果没有浏览路径
        predict_outcome = '请浏览一个文件路径'

    return render_template('app_main.html', prediction_display_area1=predict_outcome,
                           img_stream2=pred_temp, img_stream3=pred_temp_thermal, file_path=File_path)


# 视频流读取
def Video():
    # cap = cv2.VideoCapture(rtsp_url)
    global load_model
    # 加载模型判断，初次运行默认没有加载模型，防止模型多次加载导致显存不足卡住
    if load_model == None:
        print('loading model...')
        opt = detect_video.parse_opt(default=rtsp_url)
        detect_video.main(opt)
        load_model = True
    else:
        pass
    while True:
        frame = detect_video.capture()
        # ret, frame = cap.read()
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        ## 使用generator函数输出视频流， 每次请求输出的content类型是image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


# 页面播放视频流
@app.route('/video_feeds', methods=['POST', 'GET'])
def video_feed():
    # 这个地址返回视频流响应
    return Response(Video(), mimetype='multipart/x-mixed-replace; boundary=frame')


# 识别测温
@app.route('/', methods=['POST', 'GET'])  # 识别测温
def recognition_temp():
    global predict_outcome, PIC, pred_temp, pred_temp_thermal
    time1 = time.time()
    cam_msg = {'ip': hkip, 'name': hkname, 'pwd': hkpwd}
    print(cam_msg)

    '''
    mode=0,1,2  0:只拍照  1:传入已识别后的数据集和图片根据数据集的内容进行测温  2:手动测温
    temp_data: 0模式下选择None(写入数据也无影响), 1模式下需要传入测温数据集[[(左上角坐标), (右下角坐标), 标签名称], ...], 2模式同0模式
    PIC_path: 0模式下选择None(写入数据也无影响), 1模式下需要传入测温数据集[[(左上角坐标), (右下角坐标), 标签名称], ...], 2模式同0模式
    cam_msg: 需要登录摄像头的信息: ip地址, 用户名, 密码
    '''
    PIC_path = hk_main.cam_start(mode=0, temp_data=None, PIC_path=None, cam_msg=cam_msg)

    opt = detect_app.parse_opt(default=PIC_path)
    pred_pic, rectangle_msg = detect_app.main(opt)
    # print('test1:', pred_pic, rectangle_msg)

    n = 0
    temp_data = []
    for i in rectangle_msg:
        name = i['label'].split(' ')[0]
        point1 = list(i['point1'])
        point2 = list(i['point2'])
        # 在模型中有的标签选择，可以在yolov5_master/data目录下打开coco128.yaml中的'name'看到所有标签
        # 多标签选择检测
        target_name = ['person', 'tv']
        for target in target_name:
            # 根据特定标签筛选
            if name == target:
                '''
                判断条件: x边的二分之一((x1+x2)/2)或者y边的二分之一((y1+y2)/2)
                temp_point1 = (295, 50) 即(a1, b2) 可见光中的可测温范围的左上角点坐标
                temp_point2 = (1542, 967) 即(a2, b2) 可见光中的可测温范围的右下角点坐标
                如果判断x边或y边的二分之一超出了测温范围, 则不画矩形, 可认为测温范围内没有检测到
                超出检测范围: (x/2<a1 或 x/2>a2 或 y/2<b2  或 y/2>b2)满足其中一个条件即可
                '''
                if (point1[0]+point2[0])/2 < temp_point1[0] or (point1[0]+point2[0])/2 > temp_point2[0] or \
                        (point1[1]+point2[1])/2 < temp_point1[1] or (point1[1]+point2[1])/2 > temp_point2[1]:
                    print('检测超出测温边界')
                    n += 1
                    continue
                # 坐标转换:超出测温范围的点转换成测温边界的坐标
                point1[0] = temp_point1[0] if (point1[0]+point2[0])/2 > temp_point1[0] and point1[0] < temp_point1[0] else point1[0]
                point1[1] = temp_point1[1] if (point1[1]+point2[1])/2 > temp_point1[1] and point1[1] < temp_point1[1] else point1[1]
                point2[0] = temp_point2[0] if (point1[0]+point2[0])/2 < temp_point2[0] and point2[0] > temp_point2[0] else point2[0]
                point2[1] = temp_point2[1] if (point1[1]+point2[1])/2 < temp_point2[1] and point2[1] > temp_point2[1] else point2[1]
                # print('在测温范围内的有:', point1, point2, name)
                temp_msg = [point1, point2, name]
                temp_data.append(temp_msg)

                # temp_point2 = (1542, 967)
                n += 1

    print('测温范围内的数据集:', temp_data)
    if len(temp_data) == 0:
        print('测温范围内没有测温对象')
        return render_template('app_main.html')
    else:
        # mode=0,1,2  0:只拍照，1:传入已识别后的数据集和图片, 根据数据集的内容进行测温
        pred_temp, pred_temp_thermal, temp_set = hk_main.cam_start(mode=1,
                                                                 temp_data=temp_data,
                                                                 PIC_path=PIC_path,
                                                                 cam_msg=cam_msg)
        # print(temp_set)
        pred_temp = return_img_stream(pred_temp)
        pred_temp_thermal = return_img_stream(pred_temp_thermal)
        time2 = time.time()
        print('time:', time2-time1)
        return render_template('app_main.html', img_stream2=pred_temp, img_stream3=pred_temp_thermal)


# 手动测温模式
@app.route('/handle', methods=['POST', 'GET'])
def handle():
    '''
    手动模式：是将测温的模式变成手动测温，点击“手动测温”后会弹出一个cv窗口可以使用鼠标手动进行测温，
    但是由于本台电脑的线程bug，无法和实时展示的另一个画面一起运行，会导致cv的线程卡死。
    '''
    global predict_outcome, PIC, pred_temp, pred_temp_thermal
    # cam_msg = {'ip': hkip, 'name': hkname, 'pwd': hkpwd}
    # PIC_path = hk_main.cam_start(mode=2, temp_data=None, PIC_path=None, cam_msg=cam_msg)
    return render_template('app_main.html', img_stream2=pred_temp, img_stream3=pred_temp_thermal)


def driver_firefox(app_url_http):
    # 设计启动程序时打开界面用来确认ip地址，用户名，密码
    # win = Tk()
    # win.title('键盘事件')
    # txt = StringVar()  # 元组类
    # e = Entry(win, textvariable=app_url_http, validate="focusout", validatecommand=get_url)
    #
    # def get_url():
    #     new_url = e.get()
    #
    # def key_action(event):
    #     print("pressed", repr(event.char))  # 按下时打印在工作台
    #     s = event.char
    #     txt.set(s)  # 按下的字母记录到txt上
    #
    # def callback(event):
    #     L.focus_set()  # 把键盘焦点设置到文本上
    #
    # L = Label(win, width=20, textvariable=txt, bg='cyan')  # 按下后显示在lable上
    # L.bind("<KeyPress>", key_action)
    # L.bind("<Button-1>", callback)  # 鼠标点下将回调回来到我点的地方
    # e.pack()
    # L.pack()
    #
    # win.mainloop()
    try:
        from selenium import webdriver
        time.sleep(2)
        driver = webdriver.Firefox(executable_path=firefox_driver_url)  # 初始化对象
        driver.get(app_url_http)  # 使用get方法获取地址
    except:
        print(f' * 无法自动打开地址，请手动打开')
        print(f' * Open link: {app_url_http}/')
        pass


def login_gui():
    global hkname, hkpwd, hkip, app_url, port, app_url_http, rtsp_url
    win = Tk()
    win.title('login')

    label_admin = Label(win, text='admin:')
    label_pwd = Label(win, text='password:')
    label_ip = Label(win, text='ip:')
    label_url = Label(win, text='url:')
    label_url_port = Label(win, text='url_port:')

    text_cam_admin = Text(win, width=30, height=1)
    text_cam_pwd = Text(win, width=30, height=1)
    text_cam_ip = Text(win, width=30, height=1)
    text_url = Text(win, width=30, height=1)
    text_url_port = Text(win, width=30, height=1)

    label_admin.grid(row=0, column=0)
    label_pwd.grid(row=1, column=0)
    label_ip.grid(row=2, column=0)
    label_url.grid(row=3, column=0)
    label_url_port.grid(row=4, column=0)
    text_cam_admin.grid(row=0, column=1)
    text_cam_pwd.grid(row=1, column=1)
    text_cam_ip.grid(row=2, column=1)
    text_url.grid(row=3, column=1)
    text_url_port.grid(row=4, column=1)

    text_cam_admin.insert(INSERT, f'{hkname}')
    text_cam_pwd.insert(INSERT, f'{hkpwd}')
    text_cam_ip.insert(INSERT, f'{hkip}')
    text_url.insert(INSERT, f'{app_url}')
    text_url_port.insert(INSERT, f'{port}')

    def login():
        global hkname, hkpwd, hkip, app_url, port, app_url_http, rtsp_url
        hkname = text_cam_admin.get('1.0', END).split('\n')[0]
        hkpwd = text_cam_pwd.get('1.0', END).split('\n')[0]
        hkip = text_cam_ip.get('1.0', END).split('\n')[0]
        app_url = text_url.get('1.0', END).split('\n')[0]
        port = text_url_port.get('1.0', END).split('\n')[0]
        port = int(port)
        rtsp_url = f'rtsp://{hkname}:{hkpwd}@{hkip}/h264/ch1/main/av_stream'  # 摄像头取流
        app_url_http = f'http://{app_url}:{port}'
        win.destroy()

    def key_event(event):
        # 如果键盘按下回车键（enter），退出G
        # print(f"事件触发键盘输入:{event.char},对应的ASCII码:{event.keycode}")
        if event.keycode == 36 or 104:
            print(hkname, hkpwd, hkip, app_url, port, app_url_http, rtsp_url)
            login()

    Button(win, text='login', command=login).grid(row=5, column=1)
    # win.bind("<Key>", key_event)

    mainloop()


if __name__ == '__main__':
    '''
    由于app需要主进程下才能ctrl+c退出, rospy.init_node()中的disable_signals=True 一定要设置为True, 否则rosrun时, 
    ros变为主进程无法ctrl+c退出, app则一直占用进程无法完全退出, 下次运行时会因为同样端口的进程被占用则无法运行, 
    disable_signals=True, 设置为True则在ros下可以使用ctrl+c退出这个脚本的ros节点
    '''
    # pub = rospy.Publisher('chatter', String, queue_size=10)
    # rospy.init_node('app_cam', anonymous=True, disable_signals=True)

    port = '7777'
    # print(' * Open link: http://127.0.0.1:{}/'.format(port))

    # 使用线程2秒后自动打开浏览器输入地址执行程序
    app_url = '127.0.0.1'
    app_url_http = f'http://{app_url}:{port}'
    print(app_url_http)
    login_gui()
    t1 = threading.Thread(target=driver_firefox, args=[app_url_http])
    t1.start()
    app.run(app_url, port, debug=False)
