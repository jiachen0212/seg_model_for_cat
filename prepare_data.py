#coding=utf-8
import os
import shutil 
import cv2

count = 0
list_txt = '/Users/chenjia/Downloads/annotations/list.txt'
label_path = '/Users/chenjia/Downloads/annotations/trimaps'
# image_path = '/Users/chenjia/Downloads/images'
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
		# shutil.copy(os.path.join(image_path, name+'.jpg'), os.path.join(dir_, name+'.jpg'))
print(count)
# print(len(cat_imgs))

index_set = []
labels = os.listdir(dir_)
# for lab in labels:
#     label_img = cv2.imread(os.path.join(dir_, lab), 0)
#     for i in range(label_img.shape[0]):
#         for j in range(label_img.shape[1]):
#             # if label_img[i][j] == 1:
#             #     print(label_img[i][j])
#             if label_img[i][j] not in index_set:
#                 index_set.append(label_img[i][j])   # [1,2,3]
#     # label_img[label_img>=1] = 1
#     # cv2.imwrite(os.path.join(data_path, lab), label_img)
# print(index_set)

for lab in labels:
    # 灰度化
    label_img = cv2.imread(os.path.join(dir_, lab), 0)
    # label_img[label_img==1] = 1
    label_img[label_img==2] = 0   # 背景置0
    label_img[label_img==3] = 0   # cat边缘也标为0 
    cv2.imwrite(os.path.join(dir_, lab), label_img)
