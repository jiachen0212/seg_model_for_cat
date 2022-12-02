# coding=utf-8
import os 
import cv2 

other_cat = '/Users/chenjia/Desktop/200'
out_label_dir = '/Users/chenjia/Desktop/1'
dirs = os.listdir(other_cat)
for dir_ in dirs:
	path = os.path.join(other_cat, dir_)
	# 检查是否只有cat类
	anns_name = open(os.path.join(path, 'label_names.txt'), 'r').readlines()
	assert anns_name[1] == 'CAT\n'
	label_png = cv2.imread(os.path.join(path, 'label.png'), 0)
	image = cv2.imread(os.path.join(path, 'img.png'))
	label_png[label_png !=0] = 1
	cv2.imwrite(os.path.join(out_label_dir, '{}.png'.format(dir_)), label_png)
	cv2.imwrite(os.path.join(out_label_dir, '{}.jpg'.format(dir_)), image)