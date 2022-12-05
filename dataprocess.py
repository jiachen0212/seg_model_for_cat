import os
import random
import cv2
from shutil import copyfile


def pixel_check(img_path):
    values = []
    img = cv2.imread(img_path, 0)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] not in values:
                values.append(img[i][j])
    print(values)    


data_path = '/newdata/jiachen/project/fugui/voc_cat'   # data   
labels = [a for a in os.listdir(data_path) if 'png' in a]
random.shuffle(labels)
train_txt = open('./train_voc_cat.txt', 'w')
for lab in labels:
    line = '{}||{}\n'.format(os.path.join(data_path, lab[:-3]+'jpg'), os.path.join(data_path, lab))
    train_txt.write(line)


# index_set = []
# for lab in labels:
#     line = '{}||{}\n'.format(os.path.join(data_path, lab[:-3]+'jpg'), os.path.join(data_path, lab))
#     train_txt.write(line)
#     label_img = cv2.imread(os.path.join(data_path, lab), 0)
#     for i in range(label_img.shape[0]):
#         for j in range(label_img.shape[1]):
#             # if label_img[i][j] == 1:
#             #     print(label_img[i][j])
#             if label_img[i][j] not in index_set:
#                 index_set.append(label_img[i][j])   # [1,2,3]
#     # label_img[label_img>=1] = 1
#     # cv2.imwrite(os.path.join(data_path, lab), label_img)
# print(index_set)

# for lab in labels:
#     line = '{}||{}\n'.format(os.path.join(data_path, lab[:-3]+'jpg'), os.path.join(data_path, lab))
#     train_txt.write(line)
#     # 灰度化
#     label_img = cv2.imread(os.path.join(data_path, lab), 0)
#     # label_img[label_img==1] = 1
#     label_img[label_img==2] = 0   # 背景置0
#     label_img[label_img==3] = 1
#     cv2.imwrite(os.path.join(data_path, lab), label_img)

# img = cv2.imread('/newdata/jiachen/project/fugui/data/Sphynx_9.png', 0)
# img[img==1] = 255
# img[img==2] = 0   # png中2是背景, 1是cat内pixel, 3是cat外围pixel
# cv2.imwrite('./1.jpg', img)




# pick voc cat data 
voc_data = '/newdata/jiachen/project/reseach/VOCdevkit/VOC2012/Annotations'
lab_img_dir = '/newdata/jiachen/project/reseach/VOCdevkit/VOC2012/SegmentationClassAug'
lab_img_dir1 = '/newdata/jiachen/project/reseach/VOCdevkit/VOC2012/SegmentationClass'
lab_img_dir2 = '/newdata/jiachen/project/reseach/VOCdevkit/VOC2012/SegmentationObject'
image_data = '/newdata/jiachen/project/reseach/VOCdevkit/VOC2012/JPEGImages'
xmls = os.listdir(voc_data)
voc_cat_dir = './voc_cat'

if not os.path.exists(voc_cat_dir):
    os.makedirs(voc_cat_dir)

images = []
# print(len(xmls))
# count = 0
for xml in xmls:
    path = os.path.join(voc_data, xml)
    lines = open(path, 'r').readlines()
    for line in lines:
        if '<name>cat</name>' in line:
            # print(xml)
            # count += 1
            # print(xml)
            img_p = os.path.join(image_data, xml[:-3]+'jpg')
            lab_p = os.path.join(lab_img_dir, xml[:-3]+'png')
            # lab_p1 = os.path.join(lab_img_dir1, xml[:-3]+'png')
            # lab_p2 = os.path.join(lab_img_dir2, xml[:-3]+'png')
            if os.path.exists(lab_p):
                copyfile(img_p, os.path.join(voc_cat_dir, xml[:-3]+'jpg'))
                label_img = cv2.imread(lab_p, 0)
                label_img[label_img==8] = 1
                label_img[label_img!=8] = 0
                cv2.imwrite(os.path.join(voc_cat_dir, xml[:-3]+'png'), label_img)
            # elif os.path.exists(lab_p1):
            #     label_img = cv2.imread(lab_p1, 0)
            #     pixel_check(lab_p1)
            #     # label_img[label_img==8] = 1
            # elif os.path.exists(lab_p2):
            #     label_img = cv2.imread(lab_p2, 0)
            #     pixel_check(lab_p2)
               
            break
