# coding=utf-8
import cv2
import os
import threading
from SDK_main import sdk_main
 
def seg_video_frames(video_path, seg_video_name):
    times = 0
    frame_frequency = 1

    # seg_video
    fram_fps = 30
    size = (658, 960)
    video = cv2.VideoWriter(seg_video_name, cv2.VideoWriter_fourcc(*'MJPG'), fram_fps, size) 

    camera = cv2.VideoCapture(video_path)
    while True:
        times = times + 1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        if times % frame_frequency == 0:
            # cv2.imwrite(outPutDirName + '\\' + str(times)+'.jpg', image)
            seg_res, seg_res_crf = sdk_main(image[:,:,::-1])   # bgr2rgb
            # cv2.imwrite(r'C:\Users\15974\Desktop\1\{}.jpg'.format(times), seg_res)
            video.write(seg_res)
    
    camera.release()
    video.release()
    print('seg video Done!')


def write2video(video_name, fram_fps, size):
    '''
    video_name 视频保存的名字
    fram_fps 帧频率, imgs少就设置小些, 影响生成视频的长短
    size=(658, 960) 单帧size
    '''
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'MJPG'), fram_fps, size)
    imgs = os.listdir(r'C:\Users\15974\Desktop\1')
    for im in imgs:
        image = cv2.imread(os.path.join(r'C:\Users\15974\Desktop\1', im))
        video.write(image)
    video.release()

 
if __name__ == "__main__":
    
    video_path = r'C:\Users\15974\Desktop\seg_model_for_cat\fugui_data\fugui.mp4'       
    save_dir = r'C:\Users\15974\Desktop\seg_model_for_cat\fugui_data\video_ims'  
    seg_res_dir = r'C:\Users\15974\Desktop\seg_model_for_cat\fugui_data\seg_video_ims'  
    seg_video_name = r'C:\Users\15974\Desktop\seg_model_for_cat\seg_res\fugui.avi'
    threading.Thread(target=seg_video_frames, args=(video_path, seg_video_name)).start()
    