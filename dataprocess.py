# pre_process dataset label.png 
import os
import random
import cv2

data_path = '/newdata/jiachen/project/fugui/data'
labels = [a for a in os.listdir(data_path) if 'png' in a]
random.shuffle(labels)
train_txt = open('./train_cat.txt', 'w')

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

for lab in labels:
    line = '{}||{}\n'.format(os.path.join(data_path, lab[:-3]+'jpg'), os.path.join(data_path, lab))
    train_txt.write(line)
    # 灰度化
    label_img = cv2.imread(os.path.join(data_path, lab), 0)
    # label_img[label_img==1] = 1
    label_img[label_img==2] = 0   # 背景置0
    label_img[label_img==3] = 1
    cv2.imwrite(os.path.join(data_path, lab), label_img)

# img = cv2.imread('/newdata/jiachen/project/fugui/data/Sphynx_9.png', 0)
# img[img==1] = 255
# img[img==2] = 0   # png中2是背景, 1是cat内pixel, 3是cat外围pixel
# cv2.imwrite('./1.jpg', img)