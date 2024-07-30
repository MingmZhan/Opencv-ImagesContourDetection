#-*- codeing = utf-8 -*-
#@Time : 2021-12-28 15:25
#@Author : Jasmine
#@File : matchDiff.py
#@Software : PyCharm


import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse

def matchAB(fileA, fileB):
    # 读取图像数据
    imgA = cv2.imread(fileA)
    imgB = cv2.imread(fileB)


    # image灰度化->GrayImage
    grayImageA = cv2.cvtColor(imgA, cv2.COLOR_BGR2GRAY)
    grayImageB = cv2.cvtColor(imgB, cv2.COLOR_BGR2GRAY)

    # 进行阈值分割,将弹孔与背景分割
    ret1, thresh1 = cv2.threshold(grayImageA, 85, 255, cv2.THRESH_BINARY_INV)

    # 开运算 先腐蚀后膨胀->opening
    kernel = np.ones((3, 3), np.uint8)
    dilateA = cv2.dilate(thresh1, kernel)
    # cv2.imshow('dilateA', dilateA)


    # 进行阈值分割,将弹孔与背景分割
    ret2, thresh2 = cv2.threshold(grayImageB, 85, 255, cv2.THRESH_BINARY_INV)

    # 开运算 先腐蚀后膨胀->opening
    kernel = np.ones((3, 3), np.uint8)
    dilateB = cv2.dilate(thresh2, kernel)
    # cv2.imshow('dilateB', dilateB)



    # 获取图片A的大小
    height, width = dilateA.shape

    # 取局部图像，寻找匹配位置
    result_window = np.zeros((height, width), dtype=dilateB.dtype)
    for start_y in range(0, height-100, 10):
        for start_x in range(0, width-100, 10):
            window = dilateB[start_y:start_y+100, start_x:start_x+100]
            match = cv2.matchTemplate(dilateA, window, cv2.TM_CCOEFF_NORMED)
            _, _, _, max_loc = cv2.minMaxLoc(match)
            matched_window = dilateB[max_loc[1]:max_loc[1]+100, max_loc[0]:max_loc[0]+100]
            result = cv2.absdiff(matched_window, window)
            result_window[start_y:start_y+100, start_x:start_x+100] = result
    plt.imshow(result_window)
    plt.show()


    # 用四边形圈出不同部分
    _, result_window_bin = cv2.threshold(result_window, 10, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(result_window, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imgC = imgA.copy()
    for contour in contours:
        min = np.nanmin(contour, 0)
        max = np.nanmax(contour, 0)
        loc1 = (min[0][0], min[0][1])
        loc2 = (max[0][0], max[0][1])
        cv2.rectangle(imgC, loc1, loc2, 255, 3)

    plt.subplot(1, 3, 1), plt.imshow(cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)), plt.title('A'), plt.xticks([]), plt.yticks([])
    plt.subplot(1, 3, 2), plt.imshow(cv2.cvtColor(imgB, cv2.COLOR_BGR2RGB)), plt.title('B'), plt.xticks([]), plt.yticks([])
    plt.subplot(1, 3, 3), plt.imshow(cv2.cvtColor(imgC, cv2.COLOR_BGR2RGB)), plt.title('Answer'), plt.xticks([]), plt.yticks([])
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--source_image',
        type=str,
        default='../img/source.jpg',
        help='source image'
    )

    parser.add_argument(
        '--target_image',
        type=str,
        default='../img/target1.jpg',
        help='target image'
    )

    FLAGS, unparsed = parser.parse_known_args()

    matchAB(FLAGS.source_image, FLAGS.target_image)
