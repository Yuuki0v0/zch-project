#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask
from app.app_cam.views import *



app = Flask(__name__,
            static_folder='static')


# 蓝图注册区域
app.register_blueprint(app01, url_prefix='/')


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False

    # 开发环境应用
    app.run(debug=True, host="0.0.0.0", port=8001, threaded=True)
    # app.run(debug=True, host="192.168.3.100", port=5000,threaded=True)   

    # 线上环境
    # app.run(debug=False, host="0.0.0.0", port=5000,threaded=True)


