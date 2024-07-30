# -*- coding = utf-8 -*-
# @Time : 2022-01-17 23:09
# @Author : Jasmine
# @File : capture.py
# @Software : PyCharm


import cv2
import time
from test2 import *


def get_frame_from_camera():
    cap = cv2.VideoCapture(0)  # 定义摄像头对象
    # 计数count
    count = 1
    while True:
        """
        ret：True或者False，代表是否读取到图片
        frame：表示截取到一帧的图片
        
        """
        # count 为1的情况表明：从摄像头开始拍摄的第一帧开始识别
        if count == 1:
            # 按帧读取视频，其中ret是bool值
            # frame是每一帧的图像，是个三维矩阵，颜色空间是ＢＧＲ
            ret, frame = cap.read()

            # 以下将frame转为file图片路径进行存储
            # cv2.imwrite(folder_path + str(i) + ".jpeg", frame)
            # frame_bullet_img = test(folder_path + str(i) + ".jpeg", i)

            # 两行测试代码:前后帧图片是否读对
            # folder_path = "G:/PythonWorkStation/study/bullet/BulletRec/images3/"
            # cv2.imwrite(folder_path + str(count) + ".jpeg", frame)

            # 以下将实时frame直接传参，不通过存储图片形式进行弹孔检测
            # 此时的frame为第一帧图片，得到frame_bullet_img为进行图像处理识别后的弹孔图片，origin_coordinate为第一帧的弹孔坐标
            frame_bullet_img, origin_coordinate = test(frame, count)

            # 将origin_coordinate元组数据转为列表数据存储，便于后续新增坐标的比对
            origin_location = []
            for i in range(len(origin_coordinate)):
                for j in range(len(origin_coordinate[i])):
                    # print(origin_coordinate[i][j])
                    origin_location.append(origin_coordinate[i][j])
            print(origin_location)

            # frame_bullet_img为进行图像处理识别后的弹孔图片画框，实时展示在摄像框
            cv2.imshow('capture', frame_bullet_img)

            count = count + 1

            # 开始读取第二帧，获得target_frame
            ret, target_frame = cap.read()
            next_frame_bullet_img, target_coordinate = test(target_frame, count)
            cv2.imshow('capture', next_frame_bullet_img)

            # 得到下一帧的坐标数据
            target_location = []
            for i in range(len(target_coordinate)):
                for j in range(len(target_coordinate[i])):
                    # print(target_coordinate[i][j])
                    target_location.append(target_coordinate[i][j])
            print(target_location)

            # 进行前后帧的新增坐标筛选
            new_coordinate = []
            if len(origin_location) != len(target_location):
                if(len(origin_location) < len(target_location)):
                    for i in range(len(origin_location)):
                        if abs(target_location[i] - origin_location[i]) <= 3:
                            new_coordinate = []
                        elif abs(target_location[i] - origin_location[i]) > 3:
                            new_coordinate.append(target_location[i])
                    if new_coordinate == []:
                        new_coordinate.append(target_location[len(origin_location):len(target_location)])
                # 以下if条件为使得测试环境成功（实际中不需要）
                elif(len(origin_location) > len(target_location)):
                    new_coordinate = []
                    print("前后图片相反，前一帧弹孔多于后一帧，无新增弹孔坐标")
            elif len(origin_location) == len(target_location):
                new_coordinate = []
                print("前后图片弹孔个数相同，图片相似，无新增弹孔坐标")
            print("------------！！以下为新增弹孔准确位置的坐标！！---------------")
            print(new_coordinate)

        # count不为1 开始，直接拿上一帧当做当前帧，再进行frame读取，作为下一帧
        elif count != 1:

            # 以下将frame直接传参，不存储图片
            # target_frame为从count=2后的每一帧，作为上一帧
            frame_bullet_img, origin_coordinate = test(target_frame, count)

            origin_location = []
            for i in range(len(origin_coordinate)):
                for j in range(len(origin_coordinate[i])):
                    # print(origin_coordinate[i][j])
                    origin_location.append(origin_coordinate[i][j])
            print(origin_location)

            # 测试前后帧图片是否读对
            # folder_path = "G:/PythonWorkStation/study/bullet/BulletRec/images3/"
            # cv2.imwrite(folder_path + str(count) + ".jpeg", target_frame)

            cv2.imshow('capture', frame_bullet_img)

            count = count + 1

            # 重新读取视频帧，更新target_frame，作为当前帧（下一帧）
            ret, target_frame = cap.read()

            next_frame_bullet_img, target_coordinate = test(target_frame, count)
            cv2.imshow('capture', next_frame_bullet_img)

            target_location = []
            for i in range(len(target_coordinate)):
                for j in range(len(target_coordinate[i])):
                    # print(target_coordinate[i][j])
                    target_location.append(target_coordinate[i][j])
            print(target_location)

            new_coordinate = []
            if len(origin_location) != len(target_location):
                if (len(origin_location) < len(target_location)):
                    for i in range(len(origin_location)):
                        if abs(target_location[i] - origin_location[i]) <= 3:
                            new_coordinate = []
                        elif abs(target_location[i] - origin_location[i]) > 3:
                            new_coordinate.append(target_location[i])
                    if new_coordinate == []:
                        new_coordinate.append(target_location[len(origin_location):len(target_location)])
                # 以下if条件为使得测试环境成功（实际中不需要）
                elif (len(origin_location) > len(target_location)):
                    new_coordinate = []
                    print("前后图片相反，前一帧弹孔多于后一帧，无新增弹孔坐标")
            elif len(origin_location) == len(target_location):
                new_coordinate = []
                print("前后图片弹孔个数相同，图片相似，无新增弹孔坐标")

            print("------------！！以下为新增弹孔准确位置的坐标！！---------------")
            print(new_coordinate)

        """
           cv2.waitKey(1)：waitKey()函数功能是不断刷新图像，返回值为当前键盘的值
           OxFF：是一个位掩码，一旦使用了掩码，就可以检查它是否是相应的值
           ord('q')：返回q对应的unicode码对应的值(113)
        """
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if ret is False:
            print("断开连接，自主重连")
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # folder_path = "G:/PythonWorkStation/study/bullet/BulletRec/images3/"  # 存储视频每帧的本地路径
    # get_frame_from_camera(folder_path)
    get_frame_from_camera()


#
#
# import cv2
# import time
# from test2 import *
#
#
# def get_img_from_camera(folder_path):
#     cap = cv2.VideoCapture(0)  # 定义摄像头对象
#     # 按帧读取视频，其中ret是bool值
#     # frame是每一帧的图像，是个三维矩阵，颜色空间是ＢＧＲ
#     ret, frame = cap.read()
#     if ret is True:
#         i = 0
#         j = 0
#         time_fps = 30
#         # 每隔30帧提取一次图片，本dell笔记本摄像头每秒内会有30帧，所以要实现每秒截一张图片，则每30帧保存一帧图片
#         while True:
#             i = i + 1
#             if (i % time_fps == 0):
#                 j = j + 1
#                 cv2.imwrite(folder_path + str(j) + ".jpeg", frame)  # 存储为图像，图像以j从1.jpeg递增命名
#                 #cv2.imshow('capture', frame)
#                 test(folder_path + str(j) + ".jpeg", j)
#
#             ret, frame = cap.read()
#             if ret is False:
#                 print("断开连接，自主重连")
#                 cap = cv2.VideoCapture(0)
#                 ret, frame = cap.read()
#             if cv2.waitKey(0) & 0xFF == ord('q'):
#                 exit(-1)
#
#         cap.release()
#         cv2.destroyAllWindows()
#     else:
#         cap = cv2.VideoCapture(0)
#         ret, frame = cap.read()
#         print("断开连接，重连")
#
#
# if __name__ == "__main__":
#     folder_path = "G:/PythonWorkStation/study/bullet/BulletRec/images3/"  # 存储视频每帧的本地路径
#     get_img_from_camera(folder_path)


# import cv2
# # 打开笔记本的内置摄像头
# cap = cv2.VideoCapture(0)
# i = 0
#
# while True:
#     """
#     ret：True或者False，代表有没有读取到图片
#     frame：表示截取到一帧的图片
#     """
#     ret, frame = cap.read()
#     # 展示图片
#     #cv2.imshow('capture', frame)

#     # 保存图片
#     cv2.imwrite(r"G:\PythonWorkStation\study\bullet\BulletRec\images3\\" + str(i) + ".jpg", frame)
#     i = i + 1
#     """
#        cv2.waitKey(1)：waitKey()函数功能是不断刷新图像，返回值为当前键盘的值
#        OxFF：是一个位掩码，一旦使用了掩码，就可以检查它是否是相应的值
#        ord('q')：返回q对应的unicode码对应的值(113)
#     """
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
#     # k = cv2.waitKey(1)
#     #     if k == ord('k'):
#     #         cv2.imwrite(r"G:\PythonWorkStation\study\bullet\BulletRec\images3\\" + str(i) + ".jpg", frame)  # 存储路径
#     #         i = i + 1
#     #     # time.sleep(5)
#     #     if k == ord('q'):
#     #         break
# # 释放对象和销毁窗口
# cap.release()
# cv2.destroyAllWindows()