import glob
import os 
import xml.dom.minidom
import cv2
import shutil


label_png_path = '/Users/chenjia/Downloads/annotations/trimaps'
img_path = '/Users/chenjia/Downloads/images'
cat_img_label_dir = '/Users/chenjia/Desktop/seg'


count = 0
for xmlPath in glob.glob("/Users/chenjia/Downloads/annotations/xmls" + "/*.xml"):
	dom = xml.dom.minidom.parse(xmlPath)
	root = dom.documentElement
	itemList = root.getElementsByTagName('name')
	## 内参
	data = itemList[0].firstChild.data
	if data == 'cat':
		count += 1
		label_path = os.path.join(label_png_path, os.path.basename(xmlPath)[:-3]+'png')
		image_path = os.path.join(img_path, os.path.basename(xmlPath)[:-3]+'jpg')
		shutil.copy(label_path, os.path.join(cat_img_label_dir, os.path.basename(xmlPath)[:-3]+'png'))
		shutil.copy(image_path, os.path.join(cat_img_label_dir, os.path.basename(xmlPath)[:-3]+'jpg'))
print(count)