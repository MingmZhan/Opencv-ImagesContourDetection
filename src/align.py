# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# @author：lin
# data：2021-12-28


"""
    此程序用于后续的靶纸照片与标准放置的靶纸照片进行比对
    1. 为了防止实际对比时的冗余，我们规定在源程序中将附带一张标准靶纸图像
    2. 在系统运行时后续的靶纸都将跟这张标准靶纸首先进行对其操作
    3. 该操作主要是为了防止在射击过程中子弹摩擦导致的靶纸偏移，导致最后的评分结果出错
    目前当前文件夹下并无标准靶纸文件
                                                                    """


from __future__ import print_function
import cv2
import numpy as np

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15


def alignImages(im1, im2):
    #   图像灰度化处理
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    #   检测ORB特征并计算特征描述符
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)

    #   匹配特征
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    #   按分数对匹配项进行排序
    matches.sort(key=lambda x: x.distance, reverse=False)

    #   删除效果不好的匹配项
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    #   绘制匹配项
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)

    #   提取匹配位置
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    #   求单应性
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    #   使用单应性
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg, h


#   以下案例为参考案例
if __name__ == '__main__':
    #   读取参考图像
    refFilename = "img/1.jpg"
    print("Reading reference image : ", refFilename)
    imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)

    #   读取要对齐的图像
    imFilename = "img/2.jpg"
    print("Reading image to align : ", imFilename)
    im = cv2.imread(imFilename, cv2.IMREAD_COLOR)

    print("Aligning images ...")
    imReg, h = alignImages(im, imReference)

    #   保存对齐后的图像
    outFilename = "aligned.jpg"
    print("Saving aligned image : ", outFilename)
    cv2.imwrite(outFilename, imReg)

    print("Estimated homography : \n", h)

