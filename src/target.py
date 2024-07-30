#-*- codeing = utf-8 -*-
#@Time : 2021-12-29 17:12
#@Author : Jasmine
#@File : targetImg.py
#@Software : PyCharm

import cv2 as cv
import numpy as np
import cv2
from matplotlib import pyplot as plt

# 读取image
img = cv2.imread('../images/darkTest2.jpg')

# image灰度化->GrayImage
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('GrayImage', grayImage)
# cv2.waitKey(0)

# 进行阈值分割,将弹孔与背景分割
thresh = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 15)
# ret, thresh = cv2.threshold(grayImage, 138, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('threshImage', thresh)
# cv2.waitKey(0)

# 闭运算 先膨胀后腐蚀->closing
kernel = np.ones((3, 3), np.uint8)
target = cv.dilate(thresh, kernel)  # 膨胀操作
# closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
# cv2.imshow('closeImage', target)
# cv2.waitKey(0)

# 轮廓提取->contoursImage
contours, hierarchy = cv2.findContours(target, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# for i in range(0,len(contours)):
#
#     x, y, w, h = cv2.boundingRect(contours[i])
#     cv2.rectangle(img, (x,y), (x + w, y + h), (0,0,255), 2)

areas = list()
for i in range(len(contours)):
    area = cv.contourArea(contours[i], False)
    areas.append(area)
    print("轮廓%d的面积:%d" % (i, area))
area_avg = np.average(areas)
print("轮廓平均面积:", area_avg)

for i in contours:
    # 1.矩形边界框检测
    # (1)计算出一个简单的边框
    # x, y, w, h = cv2.boundingRect(i)
    #
    # # (2)将轮廓转换为(x,y)坐标，加上矩形的高度和宽度，绘制矩形
    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # # 2.最小矩形区域检测
    # # (1)计算出包围目标的最小区域
    # rect = cv2.minAreaRect(c)
    #
    # # (2)计算最小面积矩形的坐标
    # box = cv2.boxPoints(rect)
    #
    # # (3)坐标归一化为整型
    # box = np.int0(box)
    #
    # # (4)绘制轮廓
    # cv2.drawContours(img, [box], 0, (0, 255, 0), 3)

    # 3.最小闭圆检测
    # (1)计算最小闭圆的中心和半径
    [x, y], radius = cv2.minEnclosingCircle(i)

    # (2)坐标归一化为整型
    center = [int(x), int(y)]
    radius = int(radius)

    # (3)绘制圆
    img = cv2.circle(img, center, radius, (255, 0, 0), 2)

    # centers = list()
    # centers.extend(center)
    # print(centers)

# cv2.drawContours(img, contours, -1, (255, 0, 0), 2)  # 绘制边沿轮廓
# cv2.imshow("contours", img)
#
# cv2.waitKey()
# cv2.destroyAllWindows()

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('B'), plt.xticks([]), plt.yticks([])
plt.show()
# cv2.imshow('contoursImage', img)
# cv2.waitKey(0)