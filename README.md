# zch-project
该项目是海康威视网络摄像头的python二次开发使用，并部署yolov5目标识别检测算法，用于双目摄像头（RGB摄像头和热成像摄像头），其使用原理是在RGB成像画面中通过yolov5算法自动识别检测对应目标并获取该目标的坐标，并对坐标进行转换成热成像所需的坐标，传入热成像摄像头后自动测温并返回测温数据。该摄像头可以连接网络，在相同网络下可以直接根据局域网ip登录摄像头。

使用前需要的主要python包在文件中已注明，最主要的是pytorch-gpu版本和TensorFlow-gpu版本的选择，以及cuda和cudnn的安装

主程序是app_main.py
非ros环境可直接python运行（ros环境下需要将开头的两个import注释取消）
![屏幕截图(1)](https://user-images.githubusercontent.com/114372018/219323051-1fed4c1b-987f-4fd6-871a-64d779297133.png)

登录时的默认设置可以在下图这修改，登录的ui也可更改登录信息，
其中ip的信息是网络摄像头的ip地址，需要提前知道摄像头ip，url则是浏览器输入地址可以看到项目部署在本地服务器上（如果安装了python的selenium库和火狐浏览器的驱动会自动打开，没有则可以手动输入如http://127.0.0.1:7777的地址或者在终端会输出一个地址）
![屏幕截图(4)](https://user-images.githubusercontent.com/114372018/219327320-833fc748-f7d2-4eac-955e-44af890be489.png)

![屏幕截图(5)](https://user-images.githubusercontent.com/114372018/219328823-96c4ee37-b274-40c1-8ebb-b14fdc24ad98.png)

登录地址后如下所示，如果摄像头没问题可以被搜索到是有画面存在的（web前端做的很简陋，有很大的优化空间 0v0）
![image](https://user-images.githubusercontent.com/114372018/219329251-d2ce5a6e-9f66-4853-ac21-c785d0c9cb94.png)
