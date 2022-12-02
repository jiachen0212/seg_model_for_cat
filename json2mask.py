# coding=utf-8
import os 
import cv2
import json
import numpy as np 

def get_mask_from_json(json_path):
    
    category_map = ['bg', 'cat']

    with open(json_path, 'r') as r:
        anno = json.loads(r.read())
    inform = anno['shapes']
    height = anno['imageHeight']
    width = anno['imageWidth']
    mask = np.zeros((height, width), dtype=np.uint8)
    for i in inform:
        label_id = i['label']
        label_type = i['shape_type']
        points = i['points']
        for id_, id_category_list in enumerate(category_map):
            if label_id in id_category_list:
                if label_type!='linestrip':
                    cv2.polylines(mask, np.array([points], dtype=np.int32),
                                True, id_)
                    cv2.fillPoly(mask, np.array([points], dtype=np.int32), id_)
                else:
                    cv2.polylines(mask, np.array([points], dtype=np.int32),
                                False, id_, thickness=4)
                break
    return mask


data_path = '/Users/chenjia/Desktop/seg_model_for_cat/fugui_data'
res_mask_dir = os.path.join(data_path, 'mask')
if not os.path.exists(res_mask_dir):
    os.makedirs(res_mask_dir)

jss = [os.path.join(data_path, a) for a in os.listdir(data_path) if '.json' in a]
for js in jss:
    print(js)
    mask = get_mask_from_json(js)
    cv2.imwrite(os.path.join(res_mask_dir, os.path.basename(js)[:-4]+'png'), mask)