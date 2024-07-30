#-*- codeing = utf-8 -*-
#@Time : 2021-12-29 11:09
#@Author : Jasmine
#@File : absDiff.py
#@Software : PyCharm




import cv2

import numpy as np
from matplotlib import pyplot as plt
import argparse


imgA = cv2.imread('../img/12.jpg')
imgB = cv2.imread('../img/11.jpg')
result = cv2.absdiff(imgA, imgB)

print(result)
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB)), plt.title('A'), plt.xticks([]), plt.yticks([])
plt.show()