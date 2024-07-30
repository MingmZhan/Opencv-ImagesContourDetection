#-*- codeing = utf-8 -*-
#@Time : 2021-12-10 16:14
#@Author : Jasmine
#@File : OpeningCaculate.py
#@Software : PyCharm

import cv2 as cv
import numpy as np
import cv2
from matplotlib import pyplot as plt


# 读取image
img = cv2.imread('../img/12.jpg')

# image灰度化->GrayImage
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('GrayImage', grayImage)
# cv2.waitKey(0)

# 进行阈值分割,将弹孔与背景分割

'''

    thresh = cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, C)
    src：输入图像。该图像须是8位单通道图像
    maxValue：最大值
    adaptiveMethod：自适应方法:
    cv2.ADAPTIVE_THRESH_MEAN_C 和 cv2.ADAPTIVE_THRESH_GAUSSIAN_C 。
    前者领域所有像素点的权重值一致；后者与邻域各个像素点到中心点的距离有关，通过高斯方程获得各点的权重。
    thresholdType：阈值处理方式  cv2.THRESH_BINARY 或 cv2.THRESH_BINARY_INV
    blockSize：像素在计算其阈值时参考的邻域尺寸大小，通常为3，5，7
    C ：常量


'''
thresh = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 15)
# ret, thresh = cv2.threshold(grayImage, 138,255,cv2.THRESH_BINARY_INV)
cv2.imshow('threshImage', thresh)
cv2.waitKey(0)

# 开运算 先腐蚀后膨胀->opening
kernel = np.ones((3, 3), np.uint8)
origin = cv.dilate(thresh, kernel)
# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
cv2.imshow('originDilateImage', origin)
cv2.waitKey(0)

# 轮廓提取->contoursImage
contours, hierarchy = cv2.findContours(origin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for i in range(0,len(contours)):
#     x, y, w, h = cv2.boundingRect(contours[i])
#     cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2)

areas = list()
for i in range(len(contours)):
    area = cv.contourArea(contours[i], False)
    areas.append(area)
    print("轮廓%d的面积:%d" % (i, area))
area_avg = np.average(areas)
print("轮廓平均面积:", area_avg)
print(len(contours))

for i in contours:
    # 最小闭圆检测
    # (1)计算最小闭圆的中心和半径
    (x, y), radius = cv2.minEnclosingCircle(i)

    # (2)坐标归一化为整型
    center = (int(x), int(y))
    radius = int(radius)

    # (3)绘制圆
    img = cv2.circle(img, center, radius, (255, 0, 0), 2)

    # print(center)
    # centers = list()
    # centers.extend(center)
    # print(centers)


# print(centers[0][0], centers[0][1])


plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('A'), plt.xticks([]), plt.yticks([])
plt.show()
# cv2.imshow('contoursImage', img)
# cv2.waitKey(0)