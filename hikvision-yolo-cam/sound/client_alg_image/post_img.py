import requests,json
import time
import numpy as np
import cv2


def request_alg_det():
	post_file_url = 'http://0.0.0.0:8001/dect_img/'

	img = cv2.imread('test.jpg')
	# cv2.imshow('post_img',img)
	# cv2.waitKey()
	# '.jpg'表示把当前图片img按照jpg格式编码，按照不同格式编码的结果不一样
	img_encode = cv2.imencode('.jpg', img)[1]

	data_encode = np.array(img_encode)
	str_encode = data_encode.tobytes()
	# print('--------{}'.format(str_encode))
	headers = {'alg_type': 'det'}
	r = requests.post(url=post_file_url,data=str_encode, headers=headers)
	print(r.text)

def request_alg_rec():
	post_file_url = 'http://0.0.0.0:8001/dect_img/'

	img = cv2.imread('test.jpg')
	# cv2.imshow('post_img',img)
	# cv2.waitKey()
	# '.jpg'表示把当前图片img按照jpg格式编码，按照不同格式编码的结果不一样
	img_encode = cv2.imencode('.jpg', img)[1]

	data_encode = np.array(img_encode)
	str_encode = data_encode.tobytes()
	# print('--------{}'.format(str_encode))
	headers = {'alg_type': 'rec'}
	r = requests.post(url=post_file_url, data=str_encode, headers=headers)

	print(r.text)


if __name__ == '__main__':
	while True:
		request_alg_det()
		print('yes1')
		request_alg_rec()
		print('yes2')
		time.sleep(10)
