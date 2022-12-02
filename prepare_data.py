#coding=utf-8
import os
import shutil 

count = 0
list_txt = '/Users/chenjia/Downloads/annotations/list.txt'
label_path = '/Users/chenjia/Downloads/annotations/trimaps'
image_path = '/Users/chenjia/Downloads/images'
dir_ = '/Users/chenjia/Desktop/1'
'''
#Image CLASS-ID SPECIES BREED ID
#ID: 1:37 Class ids
#SPECIES: 1:Cat 2:Dog
#BREED ID: 1-25:Cat 1:12:Dog
#All images with 1st letter as captial are cat images
#images with small first letter are dog images

Sphynx_9 class_id:34 SPECIES:1 BREED ID:12
'''

cat_imgs = []
lines = open(list_txt, 'r')
for line in lines:
	a = line[0]
	# 大写开头是猫
	if a.isupper():
		count += 1
		name = line.split(' ')[0]
		# cat_imgs.append(name)
		shutil.copy(os.path.join(label_path, name+'.png'), os.path.join(dir_, name+'.png'))
		shutil.copy(os.path.join(image_path, name+'.jpg'), os.path.join(dir_, name+'.jpg'))
print(count)
# print(len(cat_imgs))




