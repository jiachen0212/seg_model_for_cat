# coding=utf-8
import cv2
import numpy as np 


img = cv2.imread('/Users/chenjia/Downloads/Smartmore/2022/seg_model_for_cat/seg_res/3.jpg')
img = img[50:, :, :]
h,w = img.shape[:2]
# print(h, w)
# 左右边分别加上300像素
ones_bg = np.ones((h, w+600, 3))*255
# cv2.imwrite('./fg.jpg', ones_bg)
ones_bg[:, 300:w+300] = img
# cv2.imshow('', ones_bg)
# cv2.waitKey(1000)
cv2.imwrite('./fg.jpg', ones_bg)
