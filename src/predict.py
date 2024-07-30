#   !/usr/bin/python3
#   -*- coding: UTF-8 -*-
#   @author：lin
#   data：2021-12-28


#   *************************************
#   此程序用于捕捉视频中的帧，便于后续的弹孔识别
#   用户可以根据自己的视频格式选择mode
#   *************************************

import cv2
import numpy as np
from PIL import Image
import time

#   此处引入相关调用函数
from align import *

#   加载参考图像
refFilename = "img/1.jpg"
print("Reading reference image : ", refFilename)
imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

#   ***********************************************
#   模式选择
#   mode用于指定测试的模式：
#   'pic'用于单张图片检测，如保存图片，截取对象等
#   'video'用于摄像头检测，可调用摄像头或者视频进行检测
#   ***********************************************
default_mode = "video"


def detect():
    mode = default_mode

    #   ********************************************************************
    #   video_path用于指定视频的路径，video_path=0时表示启用摄像头检测
    #   video_save_path表示视频的保存路径，当video_save_path=""时表示不保存视频
    #   video_fps用于保存视频的fps
    #   保存视频时需要ctrl+c退出或者运行到最后一帧才会完成完整的保存步骤
    #   ********************************************************************

    video_path = 0
    video_save_path = ""
    video_fps = 25.0

    #   **********************************************
    #   test_interval用于指定测量fps的时候，图片检测的次数
    #   test_interval越大，fps越准确
    #   **********************************************
    test_interval = 100

    #   **********************************************
    #   dir_origin_path指定用于检测图片的文件夹路径
    #   dir_save_path指定了检测图片的完整路径
    #   dir_origin_path和dir_save_path仅在mode=pic有效
    #   **********************************************
    dir_origin_path = ""
    dir_save_path = ""

    if mode == "pic":
        #   此处进行单一图片的检测
        while True:
            img = input("Input image filename:")
            try:
                image = Image.open(img)
            except:
                print("Open Error! Try Again!")
                continue
            else:
                #   读取image进行对齐操作
                im = cv2.imread(image, cv2.IMREAD_COLOR)
                imReg, h = alignImages(im, imReference)
                #   将与标准靶纸对齐后的靶纸图像放入弹孔检测算法中
                #   此处函数名还没有确定，暂且定为bulletRec
                r_image = bulletRec(imReg)
                r_image.show()

    elif mode == "video":
        #   此处进行视频的检测
        capture = cv2.VideoCapture(video_path)
        if video_save_path != "":
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            size = (int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            out = cv2.VideoWriter(video_save_path, fourcc, video_fps, size)

        ref, frame = capture.read()
        if not ref:
            raise ValueError("未能正确读取摄像头（视频），请注意是否正确安装摄像头（是否正确填写视频路径）。")
        fps = 0.0

        while True:
            t1 = time.time()
            #   读取某一帧
            ref, frame = capture.read()
            if not ref:
                break
            #   格式转变，BGR2RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            #   转变成Image
            frame = Image.fromarray(np.uint8(frame))
            #   进行检测
            #   声明一下错误，因为函数名字待定的问题，暂且取名为bulletRec
            #   这里同样需要进行跟图像识别相同的步骤,首先要对需要检测的帧实行对齐的操作
            im = cv2.imread(frame, cv2.IMREAD_COLOR)
            imReg, h = alignImages(im, imReference)
            frame = np.array(bulletRec(imReg))
            # RGBtoBGR满足opencv显示格式
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            fps = (fps + (1. / (time.time() - t1))) / 2
            print("fps= %.2f" % (fps))
            frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("video", frame)
            c = cv2.waitKey(1) & 0xff
            if video_save_path != "":
                out.write(frame)

            if c == 27:
                capture.release()
                break

        print("Video Detection Done!")
        capture.release()
        if video_save_path != "":
            print("Save processed video to the path :" + video_save_path)
            out.release()
        cv2.destroyAllWindows()

    else:
        raise AssertionError("Please specify the correct mode: 'img', 'video' ")


if __name__ == "__main__":
    detect()