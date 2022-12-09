# coding=utf-8
'''
对一些seg模型没分割好,但又想拿来"作图"的场景, 
可用次脚本实现: labelme简单标一下然后json2mask把cat"显著出来"
找到你想要的背景, cv2.addweighted融合下~

'''

import os
import cv2
import numpy as np
from json2mask import get_mask_from_json


def rotate_cat(cat_img, cat_mask, rotate=-30):
	h, w = cat_mask.shape[:2]
	M = cv2.getRotationMatrix2D((h//2, w//2), rotate, 1.0)  
	rotated_mask = cv2.warpAffine(cat_mask, M, (w, h))  
	rotated_img = cv2.warpAffine(cat_img, M, (w, h))  
	# cv2.imshow("Rotated by -90 Degrees", rotated) 
	# cv2.waitKey(1000)
	# print(rotated[0][0])

	return rotated_mask, rotated_img



def rotate_cat_and_paste_to_ChristmasTree(fg_mask, fg_img, bg_img, rotate=None, set_xy=[650, 490]):
	
	cat_h, cat_w = fg_mask.shape[:2]
	r_mask, r_img = rotate_cat(fg_img, fg_mask, rotate=rotate)

	#1. cat前景没旋转, 就直接像素覆盖放上去就好
	# bg_img[set_xy[1]:set_xy[1]+cat_w//2, set_xy[0]:set_xy[0]+cat_h//2, :] = r_img

	#2. cat前景旋转了, 则边上会有黑边, 则需要辅助使用mask来把黑边用背景部分补上. 
	fg_zeros = np.zeros(bg_img.shape[:2])
	fg_zeros[set_xy[1]:set_xy[1]+cat_h, set_xy[0]:set_xy[0]+cat_w] = r_mask

	h, w = bg_img.shape[:2]
	for i in range(h):
		for j in range(w):
			if fg_zeros[i][j] == 255:
				bg_img[i][j] = r_img[i-set_xy[1]][j-set_xy[0]]


	# cv2.imshow('', bg_img)
	# cv2.waitKey(1000)
	return bg_img



def resize_cat(cat_img, cat_mask, scale=1.0):

	h, w = cat_mask.shape[:2]
	cat_img = cv2.resize(cat_img, (int(w*scale), int(h*scale)))
	cat_mask = cv2.resize(cat_mask, (int(w*scale), int(h*scale)))

	return cat_mask, cat_img


def padding(img, padd_h, padd_w):
	# 有些时候微信头像比例问题导致我们想展示的部分被截断, 可考虑在四边做点padding
	# 把我们想要的部分"相对缩小", 从而可完整显示在头像框中

	h, w = img.shape[:2]
	temp = np.ones((h+padd_h*2, w+padd_w*2, 3))
	temp[padd_h:padd_h+h, padd_w:padd_w+w] = img

	return temp



if __name__ == '__main__': 
	
	'''
	实现一个把"富贵挂上圣诞树的功能~"

	'''

	# 设置cat旋转角度
	rotate_ = -10
	# 设置放置cat的位置
	set_xy_ = [550, 250]
	# cat是否要做缩放
	scale = 1.0
	# 在paste结果周边再padding下
	need_padding = True
	padd_h, padd_w = 200, 200
	

	cat_json = '/Users/chenjia/Downloads/Smartmore/2022/seg_model_for_cat/fugui_data/test/IMG_6269.json'
	fg_img = cv2.imread('/Users/chenjia/Downloads/Smartmore/2022/seg_model_for_cat/fugui_data/test/IMG_6269.jpg')
	bg_img = cv2.imread('/Users/chenjia/Downloads/Smartmore/2022/seg_model_for_cat/json2mask/IMG_6255.JPG')
	fg_mask = get_mask_from_json(cat_json, to_255=True)

	if scale != 1.0:
		fg_mask, fg_img = resize_cat(fg_img, fg_mask, scale=scale)

	res = rotate_cat_and_paste_to_ChristmasTree(fg_mask, fg_img, bg_img, rotate=rotate_, set_xy=set_xy_)
	
	if need_padding: 
		res = padding(res, padd_h, padd_w)

	cv2.imwrite('./Christmas_fugui.png', res)



