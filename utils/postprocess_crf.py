import numpy as np
import pydensecrf.densecrf as dcrf
import cv2 
from pydensecrf.utils import unary_from_labels, create_pairwise_bilateral, create_pairwise_gaussian

  
def CRFs(img, predicted_img, gaussian_=5, bilateral_=9):

    # _gaussian(sdims=(5, 5) 
    # feats = create_pairwise_bilateral(sdims=(9, 9) ..


    h, w = img.shape[:2]
    anno_rgb = predicted_img.astype(np.uint32)
    anno_lbl = anno_rgb[:, :] + (anno_rgb[:, :] << 8) + (anno_rgb[:, :] << 16)

    _, labels = np.unique(anno_lbl, return_inverse=True)
    n_labels = len(set(labels.flat))

    use_2d = False
    if use_2d:
        d = dcrf.DenseCRF2D(img.shape[1], img.shape[0], n_labels)
        U = unary_from_labels(labels, n_labels, gt_prob=0.2, zero_unsure=None)
        d.setUnaryEnergy(U)
        d.addPairwiseGaussian(sxy=(3, 3), compat=3, kernel=dcrf.DIAG_KERNEL,
                              normalization=dcrf.NORMALIZE_SYMMETRIC)

        d.addPairwiseBilateral(sxy=(80, 80), srgb=(13, 13, 13), rgbim=img, compat=10,
                               kernel=dcrf.DIAG_KERNEL,
                               normalization=dcrf.NORMALIZE_SYMMETRIC)
    else:
        d = dcrf.DenseCRF(img.shape[1] * img.shape[0], n_labels)
        U = unary_from_labels(labels, n_labels, gt_prob=0.7, zero_unsure=None)
        d.setUnaryEnergy(U)

        feats = create_pairwise_gaussian(sdims=(gaussian_, gaussian_), shape=img.shape[:2])
        d.addPairwiseEnergy(feats, compat=3, kernel=dcrf.DIAG_KERNEL,
                            normalization=dcrf.NORMALIZE_SYMMETRIC)

        feats = create_pairwise_bilateral(sdims=(bilateral_, bilateral_), schan=(11, 11, 11),
                                          img=img, chdim=2)
        d.addPairwiseEnergy(feats, compat=10,
                            kernel=dcrf.DIAG_KERNEL,
                            normalization=dcrf.NORMALIZE_SYMMETRIC)
        Q = d.inference(5)
        MAP = np.argmax(Q, axis=0)

        return MAP.reshape((w, h))
 