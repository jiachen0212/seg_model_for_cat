# coding=utf-8
import os 
import cv2
import numpy as np
import onnxruntime as ort
from scipy.special import softmax
import matplotlib.pyplot as plt
from PIL import Image
from postprocess_crf import CRFs 


def label2colormap(label):
    m = label.astype(np.uint8)
    r, c = m.shape[:2]
    cmap = np.zeros((r, c, 3), dtype=np.uint8)
    cmap[:, :, 0] = (m & 1) << 7 | (m & 8) << 3
    cmap[:, :, 1] = (m & 2) << 6 | (m & 16) << 2
    cmap[:, :, 2] = (m & 4) << 5
    return cmap


def sdk_pre(img_t, mean_, std_):
    img_t = img_t[np.newaxis,:,:,:]
    img = np.array(img_t, dtype=np.float32)
    img -= np.float32(mean_)
    img /= np.float32(std_)
    img = np.transpose(img, [0, 3, 1, 2])
    return img


def check_connect_comp(img, label_index):
    mask = np.array(img == label_index, np.uint8)
    num, label = cv2.connectedComponents(mask, 8)
    return mask, num, label


def sdk_post(predict, onnx_predict, Confidence=None, num_thres=None):

    num_class = predict.shape[1]
    map_ = np.argmax(onnx_predict[0], axis=1)
    mask_map = np.max(predict[0, :, :, :], axis=0)
    mask_ = map_[0, :, :]
    temo_predict = np.zeros(mask_.shape)
    for i in range(num_class):
        if i == 0:
            continue
        else:
            _, num, label = check_connect_comp(mask_, i)
            for j in range(num):
                if j == 0:
                    continue
                else:
                    temp = np.array(label == j, np.uint8)
                    score_temp = temp * mask_map
                    locate = np.where(temp > 0)
                    number_thre = len(locate[0])
                    score_j = np.sum(score_temp) / number_thre

                    if number_thre > num_thres[i] and score_j > Confidence[i]:
                        temo_predict += temp * i
            
    return temo_predict  


def my_paste(org_img, gray_mask):
    org1 = org_img[:,:,0]
    org2 = org_img[:,:,1]
    org3 = org_img[:,:,2]
    org1[gray_mask==0]=255
    org2[gray_mask==0]=255
    org3[gray_mask==0]=255

    return cv2.merge([org1, org2, org3])[:,:,::-1]



if __name__ == "__main__":

    root_path = '/Users/chenjia/Downloads/Smartmore/2022/seg_model_for_cat'
    # root_path = r'C:\Users\15974\Desktop\seg_model_for_cat')
    img_path = os.path.join(root_path, 'fugui_data', 'test')

    defcets = ['bg', 'cat']
    Confidence = [0.5] * len(defcets)
    num_thres = [200, 200]   
    # ?????????mean???std
    mean_ = [123.675, 116.28, 103.53]
    std_ = [58.395, 57.12, 57.375]
    # ?????????????????????
    size = [400, 400]

    img_type = ['.JPG', '.jpg', '.png']
    test_paths = [os.path.join(img_path, a) for a in os.listdir(img_path) if a[-4:] in img_type]
    res_dir = os.path.join(root_path, 'seg_res')
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    # ??????onnx
    onnx_path = os.path.join(root_path, 'onnxs', '10000.onnx')
    onnx_session = ort.InferenceSession(onnx_path)


    for test_path in test_paths:
        img_base_name = os.path.basename(test_path)
        img_org = Image.open(test_path) 
        img_org = np.asarray(img_org)
        h_org, w_org = img_org.shape[:2]
        img = cv2.resize(img_org, (size[0], size[1])) 
        img_ = sdk_pre(img, mean_, std_)
        onnx_inputs = {onnx_session.get_inputs()[0].name: img_.astype(np.float32)}
        onnx_predict = onnx_session.run(None, onnx_inputs)
        predict = softmax(onnx_predict[0], 1)
        map_ = sdk_post(predict, onnx_predict, Confidence=Confidence, num_thres=num_thres)        
        mask_vis = label2colormap(map_)
        resize_map_ = cv2.resize(map_, (w_org, h_org))
        # mask_vis = cv2.resize(mask_vis, (w_org, h_org))
        # res = cv2.addWeighted(img_org, 0.2, mask_vis, 0.8, 0)
        
        res = my_paste(img_org, resize_map_)
        # predict_map??????denscrf????????????????????????, gaussian_, bilateral?????????
        try:
            crf_map_ = CRFs(img, map_, gaussian_=3, bilateral_=10)
            # crf_map = label2colormap(crf_map_)
            resize_crf_map_ = cv2.resize(crf_map_, (w_org, h_org))
            res_crf = my_paste(img_org, resize_crf_map_)
        except:
            res_crf = res

        cv2.imwrite(os.path.join(res_dir, img_base_name), res_crf)
        # crf_map = cv2.resize(crf_map, (w_org, h_org))
        # crf_res = cv2.addWeighted(img_org, 0.2, crf_map, 0.8, 0)
        # res_merge = cv2.hconcat([res, crf_res])
        # cv2.imwrite(os.path.join(res_dir, img_base_name), res_merge)
         
        # plt.subplot(121)
        # plt.xlabel('model_result')
        # plt.imshow(res[..., ::-1])
        # plt.subplot(122)
        # plt.xlabel('crf_res')
        # plt.imshow(crf_res[..., ::-1])
        # plt.savefig(os.path.join(res_dir, img_base_name))
  
