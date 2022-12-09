# coding=utf-8 
import numpy as np
import pydensecrf.densecrf as dcrf
import cv2
from pydensecrf.utils import unary_from_labels, create_pairwise_bilateral, create_pairwise_gaussian



def CRFs(img, anno_rgb, gaussian_=5, bilateral_=10):

    colors, labels = np.unique(anno_rgb, return_inverse=True)
    n_labels = len(set(labels.flat))

    use_2d = False               

    if use_2d:                   
        # 使用densecrf2d类
        d = dcrf.DenseCRF2D(img.shape[1], img.shape[0], n_labels)
    
        # 得到一元势（负对数概率）
        U = unary_from_labels(labels, n_labels, gt_prob=0.2, zero_unsure=None)
        #U = unary_from_labels(labels, n_labels, gt_prob=0.2, zero_unsure=HAS_UNK)## 如果有不确定区域，用这一行代码替换上一行
        d.setUnaryEnergy(U)
    
        # 增加了与颜色无关的术语，只是位置-----会惩罚空间上孤立的小块分割,即强制执行空间上更一致的分割
        d.addPairwiseGaussian(sxy=(gaussian_, gaussian_), compat=3, kernel=dcrf.DIAG_KERNEL,
                              normalization=dcrf.NORMALIZE_SYMMETRIC)
    
        # 增加了颜色相关术语，即特征是(x,y,r,g,b)-----使用局部颜色特征来细化它们
        d.addPairwiseBilateral(sxy=(bilateral_, bilateral_), srgb=(13, 13, 13), rgbim=img,compat=10,
                               kernel=dcrf.DIAG_KERNEL,
                               normalization=dcrf.NORMALIZE_SYMMETRIC)

    else:
        d = dcrf.DenseCRF(img.shape[1] * img.shape[0], n_labels)
        # 得到一元势（负对数概率）
        U = unary_from_labels(labels, n_labels, gt_prob=0.5, zero_unsure=None)  
        d.setUnaryEnergy(U)
    
        # 这将创建与颜色无关的功能，然后将它们添加到CRF中
        feats = create_pairwise_gaussian(sdims=(gaussian_, gaussian_), shape=img.shape[:2])
        d.addPairwiseEnergy(feats, compat=8,kernel=dcrf.DIAG_KERNEL,
                            normalization=dcrf.NORMALIZE_SYMMETRIC)
    
        # 这将创建与颜色相关的功能，然后将它们添加到CRF中
        feats = create_pairwise_bilateral(sdims=(bilateral_, bilateral_), schan=(13, 13, 13),
                                          img=img, chdim=2)
        d.addPairwiseEnergy(feats, compat=10,
                            kernel=dcrf.DIAG_KERNEL,
                            normalization=dcrf.NORMALIZE_SYMMETRIC)
    
    Q = d.inference(10)

    MAP = np.argmax(Q, axis=0)

    return MAP.reshape(img.shape[:2])