import time
import numpy as np
import cv2


def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


# c++算法封装，单例模式

@singleton
class Alg2(object):

    def __init__(self):
        self.gpu_id_ = 0
        self.alg_sys_ = None
        self.is_initialized_ = False
        # self.img = np.zeros((1080, 1920), dtype=np.uint8)

    # c++算法初始化
    # 返回是否初始化成功
    # data_dir 数据文件夹
    # batch_size 批数量
    # gpu_id 显卡ID
    # conf_th 检测阈值
    # nms_th nms阈值
    def Initial(self, data_dir, batch_size, gpu_id, conf_th, nms_th):

        if self.is_initialized_:
            return True

        if True:
            self.is_initialized_ = True
            return True

    # 批量检测
    def DetectBatch(self,img):
        self.img = img
        num = 1
        return num
