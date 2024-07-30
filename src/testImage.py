#-*- codeing = utf-8 -*-
#@Time : 2021-12-31 12:57
#@Author : Jasmine
#@File : testImage.py
#@Software : PyCharm

import os
from PIL import Image

path = os.path.join(os.getcwd(), "../images/lighterTest1.jpg")
img = Image.open(path)
print(img.size)

path2 = os.path.join(os.getcwd(), "../images/lighterTest2.jpg")
img2 = Image.open(path2)
print(img2.size)