#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
import time
import sys
import os
import cv2
import numpy as np
from vosp_sample.server_alg_image.algorithm_module.method_modules.vosp_det import Alg1
from vosp_sample.server_alg_image.algorithm_module.method_modules.vosp_rec import Alg2

pre_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(pre_path, "./app/app_cam"))


app01 = Blueprint('app01', __name__)
CORS(app01, supports_credentials=True)


@app01.route('/dect_img/', methods=["GET", "POST"])
def process_img():
    res = {}
    try:
        str_encode = request.data     #bytes
        # print('request.data---{}'.format(type(str_encode)))
        image = np.asarray(bytearray(str_encode), dtype="uint8")
        # print('image.np.asarray---{}'.format(type(image)))
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # print('image.imdecode---{}'.format(type(image)))
        alg_type = request.headers.get('alg_type')
        if alg_type == 'det':
            num = Alg1().DetectBatch(image)
        else:
            num = Alg2().DetectBatch(image)
        # print('box--{}  num--{}'.format(box,num))
        # draw_person(image,box,num)
        # print('code--{}'.format(code))
        res['code'] = 200
        res['data'] = num
    except Exception as e:
        res['code'] = 500
    return jsonify(res)


