#-*- codeing = utf-8 -*-
#@Time : 2021-12-29 21:18
#@Author : Jasmine
#@File : targetLocationContour.py
#@Software : PyCharm


import cv2 as cv
import numpy as np
import cv2
from matplotlib import pyplot as plt
from targetImg import *


def newHoleLocation(origin_file, newfile):
    new_coordinate = newHole(origin_file, newfile)

    print("---------------- 以下为新弹孔检测位置画轮廓-----------------")

    # 读取image
    img = cv2.imread(newfile)

    # image灰度化->GrayImage
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 进行阈值分割,将弹孔与背景分割
    thresh = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 15)

    # 闭运算 先膨胀后腐蚀->closing
    kernel = np.ones((3, 3), np.uint8)
    target = cv.dilate(thresh, kernel)  # 膨胀操作

    # 轮廓提取->contoursImage
    contours, hierarchy = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for i in contours:
        # 3.最小闭圆检测
        # (1)计算最小闭圆的中心和半径
        (x, y), radius = cv2.minEnclosingCircle(i)

        # (2)坐标归一化为整型
        for j in new_coordinate:
            center = j
        radius = int(radius)
        # (3)绘制圆
        img = cv2.circle(img, center, radius, (255, 0, 0), 2)

    # 输出新弹孔位置的坐标
    print("新增弹孔位置坐标为：", center)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('B'), plt.xticks([]), plt.yticks([])
    plt.show()
    return new_coordinate


if __name__ == "__main__":
    newHoleLocation('../images/darkTest1.jpg', '../images/darkTest2.jpg')
