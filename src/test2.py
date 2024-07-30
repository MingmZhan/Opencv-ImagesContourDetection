# -*- coding = utf-8 -*-
# @Time : 2022-01-06 16:27
# @Author : Jasmine
# @File : test2.py
# @Software : PyCharm

import os
import numpy as np
import cv2
from matplotlib import pyplot as plt


# 第一种画轮廓的方式
def draw_contours(img, cnts):  # conts = contours
    img = np.copy(img)
    img = cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
    cv2.imshow("draw_contours", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img


def draw_approx_hull_polygon(img, cnts):
    img = np.zeros(img.shape, dtype=np.uint8)

    cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)  # blue

    min_side_len = img.shape[0] / 32  # 多边形边长的最小值 the minimum side length of polygon
    min_poly_len = img.shape[0] / 16  # 多边形周长的最小值 the minimum round length of polygon
    min_side_num = 3  # 多边形边数的最小值
    approxs = [cv2.approxPolyDP(cnt, min_side_len, True) for cnt in cnts]  # 以最小边长为限制画出多边形
    approxs = [approx for approx in approxs if cv2.arcLength(approx, True) > min_poly_len]  # 筛选出周长大于 min_poly_len 的多边形
    approxs = [approx for approx in approxs if len(approx) > min_side_num]  # 筛选出边长数大于 min_side_num 的多边形
    cv2.polylines(img, approxs, True, (0, 255, 0), 2)  # green
    hulls = [cv2.convexHull(cnt) for cnt in cnts]
    cv2.polylines(img, hulls, True, (0, 0, 255), 2)  # red
    # cv2.imshow("draw_approx_hull_polygon", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img


# 第二种画轮廓的方式
def draw_min_rect_circle(img, cnts, count):  # conts = contours
    img = np.copy(img)

    original_coordinate = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue
        # print(x, y, x + w, y + h)
        # 此处定义内切圆的圆心以及半径
        temp_w = w / 2
        temp_h = h / 2
        temp_x = x + temp_w
        temp_y = y + temp_h
        radius = min(w, h) / 2

        min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
        min_rect = np.int0(cv2.boxPoints(min_rect))
        # cv2.drawContours(img, [min_rect], 0, (0, 255, 0), 2)  # green

        # 内切圆
        # (x, y), radius = cv2.minEnclosingCircle(cnt)
        center, radius = (int(temp_x), int(temp_y)), int(radius)
        original_coordinate.append(center)
        img = cv2.circle(img, center, radius, (0, 0, 255), 2)

        # 外切圆
        # (x, y), radius = cv2.minEnclosingCircle(cnt)
        # center, radius = (int(x), int(y)), int(radius)  # center and radius of minimum enclosing circle
        # img = cv2.circle(img, center, radius, (0, 0, 255), 2)  # red

    # cv2.imshow("draw_min_rect_circle", img)
    # cv2.waitKey(0)

    print("--------------以下为第 %d 张原始弹孔图片准确位置的坐标---------------" % count)
    # print(original_coordinate)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), plt.title('OriginBullet'), plt.xticks([]), plt.yticks([])
    plt.show()
    plt.show(block=False)
    plt.pause(0.5)
    plt.close()

    return img, original_coordinate

    #cv2.imwrite(str(count) + ".jpg", img)
    #return img


# 传入参数file改为了（capture里的frame）img直接传参,直接读取，不转为图片路径
def test(file, count):
    # 读取图像
    img = cv2.imread(file)

    # 灰度化
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv2.namedWindow('gray', 0)
    # cv2.resizeWindow('gray', 600, 600)
    #cv2.imshow('gray', grayImage)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # 图像平滑处理
    blur = cv2.GaussianBlur(grayImage, (9, 9), 0)
    # cv2.namedWindow('Blur', 0)
    # cv2.resizeWindow('Blur', 600, 600)
    # cv2.imshow('Blur', blur)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 边缘检测
    thresh = cv2.Canny(blur, cv2.ADAPTIVE_THRESH_MEAN_C, 256)
    # cv2.namedWindow('Thresh', 0)
    # cv2.resizeWindow('Thresh', 600, 600)
    # cv2.imshow('Thresh', thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 使用连接组件进行图像平滑处理来消除图像中的噪声
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, None, None, None, 8, cv2.CV_32S)
    areas = stats[1:, cv2.CC_STAT_AREA]
    result = np.zeros((labels.shape), np.uint8)
    for i in range(0, nlabels - 1):
        # 此处的阈值还要根据弹孔的实际大小来定
        if areas[i] >= 20:
            result[labels == i + 1] = 255

    # cv2.namedWindow('result', 0)
    # cv2.resizeWindow('result', 600, 600)
    # cv2.imshow("result", result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 进行闭运算
    kernel = np.ones((9, 9), np.uint8)
    closed = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel, iterations=3)
    # cv2.namedWindow('closed', 0)
    # cv2.resizeWindow('closed', 600, 600)
    # cv2.imshow("closed", closed)
    # # cv2.waitKey(0)
    # # # cv2.destroyAllWindows()

    # 消除轮廓中的干扰区域
    im_floodfill = closed.copy()
    h, w = closed.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)  # 定义mask掩模，要求长度加2
    # 使用floodFill函数，得到只标记孔洞的像素矩阵（孔洞值为0，非孔洞值为指定值）
    # 得到im_floodfill图像， 255填充非孔洞值
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    # 取反操作
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # im_in、im_floodfill_inv 两幅图像结合
    im_out = closed | im_floodfill_inv
    # cv2.namedWindow('openImage', 0)
    # cv2.resizeWindow('openImage', 600, 600)
    # cv2.imshow('openImage', im_out)
    # cv2.waitKey(0)

    # 得到目标边缘
    contours, hierarchy = cv2.findContours(im_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 这里测试三种画轮廓的方式
    # draw_contours(img, contours)
    return draw_min_rect_circle(img, contours, count)


    # 绘制近似船体多边形
    # draw_approx_hull_polygon(img, contours)


if __name__ == "__main__":
    file_list = os.listdir("../images2")

    # for i in range(1, len(file_list) + 1):
    #     test('../images2/' + str(i) + ".jpeg", i)
    test("../images2/16.jpeg", 1)
    # test("../img/10.jpg", 1)