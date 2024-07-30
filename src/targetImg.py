# -*- codeing = utf-8 -*-
# @Time : 2021-12-29 17:12
# @Author : Jasmine
# @File : targetImg.py
# @Software : PyCharm
import cv2 as cv
import numpy as np
import cv2
from matplotlib import pyplot as plt
from originImg import *
import ast


def newHole(origin_file, newfile):
    origin_coordinate = originHoles(origin_file)
    print("---------------- 以下为新弹孔检测-----------------")

    # 读取image
    img = cv2.imread(newfile)

    # image灰度化->GrayImage
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 进行阈值分割,将弹孔与背景分割
    thresh = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 15)

    # 闭运算 先膨胀后腐蚀->closing
    kernel = np.ones((5, 5), np.uint8)
    target = cv.dilate(thresh, kernel)  # 膨胀操作
    im_floodfill = target.copy()

    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = target.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)

    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)

    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)

    # Combine the two images to get the foreground.
    im_out = target | im_floodfill_inv
    cv2.imshow('openImage', im_out)
    cv2.waitKey(0)
    # 轮廓提取->contoursImage
    contours, hierarchy = cv2.findContours(im_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

    temp_coordinate = []
    for i in contours:
        # 3.最小闭圆检测
        # (1)计算最小闭圆的中心和半径
        (x, y), radius = cv2.minEnclosingCircle(i)

        # (2)坐标归一化为整型
        center1 = (int(x), int(y))
        radius = int(radius)
        print(center1)

        # (3)绘制圆
        img = cv2.circle(img, center1, radius, (255, 0, 0), 2)
        temp_coordinate.append(center1)

    # 输出新弹孔位置的坐标
    print(temp_coordinate)
    print("----------------------------------------------------------")


    target_coordinate = []
    # for j in temp_coordinate:
    #     center2 = j
    #     img = cv2.circle(img, center2, 20, (255, 0, 0), 2)

    for x in range(len(contours)):
        if x not in deny_area:
            target_coordinate.append(temp_coordinate[x])
            print(temp_coordinate[x])
    print("--------------以下为新弹孔图片准确位置的坐标列表---------------")
    print(target_coordinate)
    # print(temp_coordinate + origin_coordinate)
    # new_coordinate = [x for x in (temp_coordinate + origin_coordinate) if x not in origin_coordinate]
    # print("new_coordinate =", new_coordinate)

    origin_location = []
    for i in range(len(origin_coordinate)):
        for j in range(len(origin_coordinate[i])):
            print(origin_coordinate[i][j])
            origin_location.append(origin_coordinate[i][j])
    print(origin_location)

    target_location = []
    for i in range(len(target_coordinate)):
        for j in range(len(target_coordinate[i])):
            print(target_coordinate[i][j])
            target_location.append(target_coordinate[i][j])
    print(target_location)

    new_coordinate = []
    if len(origin_location) != len(target_location):
        for i in range(len(origin_location)):
            if abs(target_location[i] - origin_location[i]) <= 3:
                new_coordinate = []
            elif abs(target_location[i] - origin_location[i]) > 3:
                new_coordinate.append(target_location[i])
        if new_coordinate == []:
            new_coordinate.append(target_location[len(origin_location):len(target_location)])
    elif len(origin_location) == len(target_location):
        new_coordinate = []
        print("前后图片相似，无新增弹孔坐标")

    print("------------！！以下为新增弹孔准确位置的坐标！！---------------")
    print(new_coordinate)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('B'), plt.xticks([]), plt.yticks([])
    plt.show()
    # return new_coordinate

if __name__ == "__main__":
    newHole('../images/darkTest1.jpg', '../images/darkTest2.jpg')