#-*- codeing = utf-8 -*-
#@Time : 2021-12-10 16:14
#@Author : Jasmine
#@File : OpeningCaculate.py
#@Software : PyCharm

import cv2 as cv
import numpy as np
import cv2
from matplotlib import pyplot as plt


def originHoles(file):

    # 读取image
    img = cv2.imread(file)

    # image灰度化->GrayImage
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
    # cv2.imshow('thresh', thresh)
    # cv2.waitKey(0)

    # 开运算 先腐蚀后膨胀->opening
    kernel = np.ones((5, 5), np.uint8)
    origin = cv.dilate(thresh, kernel)

    # origin = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # cv2.imshow('openImage', origin)
    # cv2.waitKey(0)

    im_floodfill = origin.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = origin.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    # Invert floodfilled image 取反操作
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground 位或操作
    im_out = origin | im_floodfill_inv
    cv2.imshow('openImage', im_out)
    cv2.waitKey(0)

    # 轮廓提取->contoursImage
    contours, hierarchy = cv2.findContours(im_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 获取轮廓面积
    areas = list()
    deny_area = list()
    for i in range(len(contours)):
        area = cv.contourArea(contours[i], False)
        if 50 < area < 1000:
            areas.append(area)
            print("轮廓%d的面积:%d" % (i, area))
        elif area < 50 or area > 1000:
            print("弹孔识别在轮廓%d存在误差的面积为:%d" % (i, area))
            deny_area.append(i)
    print("需要去除的轮廓下标为：", deny_area)
    # area_avg = np.average(areas)
    # print("轮廓平均面积:", area_avg)

    # 最小闭圆检测
    coordinate = []
    for i in contours:
        # (1)计算最小闭圆的中心和半径

        (x, y), radius = cv2.minEnclosingCircle(i)

        # (2)坐标归一化为整型
        center1 = (int(x), int(y))
        radius = int(radius)

        # (3)绘制圆

        img = cv2.circle(img, center1, radius, (255, 0, 0), 2)

        print(center1)
        coordinate.append(center1)
    print(coordinate)

    print("--------------------------------------------------------")

    original_coordinate = []
    for x in range(len(contours)):
        if x not in deny_area:
            original_coordinate.append(coordinate[x])
            print(coordinate[x])
    print("--------------以下为原始弹孔图片准确位置的坐标---------------")
    print(original_coordinate)
    #
    # for j in original_coordinate:
    #     center = j
    #     img = cv2.circle(img, center, 40, (255, 0, 0), 2)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('OriginBullet'), plt.xticks([]), plt.yticks([])
    plt.show()
    return original_coordinate


if __name__ == "__main__":
    originHoles('../images/darkTest1.jpg')