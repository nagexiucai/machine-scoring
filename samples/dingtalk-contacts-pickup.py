#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Time    : 2017/12/28 10:55
# @Author  : Bob
# @Website : www.nagexiucai.com
# @E-Mail  : me@nagexiucai.com
# @Summary : 基于opencv-python、pil和pyautogui的钉钉联系人信息拾取。

from sys import path as INCLUDE
INCLUDE.append("..") # TODO: CWD MUST BE THE SAME WITH THE SCRIPT
from core import *
from PIL import Image, ImageGrab
import pyautogui as X
from matplotlib import pyplot as PLT
from os import getcwd, path
from time import sleep

H,V = X.size()
print("Screen size is", H, V)
X.hotkey("Fn", "PrintScreen")
image = ImageGrab.grabclipboard()
image.save("tmp.jpg")

# if isinstance(image, Image.Image):
#     print(image.format, image.size, image.mode)
#     h, v = image.size
#     print(h, v)
#     pixels = image.load()
#     print(pixels)
#     for x in range(h):
#         for y in range(v):
#             print(pixels[x, y])

image = cv.imread("tmp.jpg")
print(image.shape) # TODO: OpenCV的颜色通道BGR、像素矩阵做了转置


picture = image.copy()
template = cv.imread('dingtalk/contact-button.png')
width, height, channel = template.shape

resource = cv.matchTemplate(picture,template,cv.TM_CCOEFF_NORMED)
minv, maxv, minp, maxp = cv.minMaxLoc(resource)

top, left = maxp

bottom, right = top+width, left+height

X.moveTo((top+bottom)/2,(left+right)/2,duration=3) # TODO: 像素矩阵做了转置
X.click()

# cv.rectangle(picture,(top,left), (bottom,right), 255, 2)

# figure = PLT.figure('TITLE @ SOURCE @ TEMPLATE @ COST')
# PLT.subplot(121),PLT.imshow(resource,cmap = 'gray')
# PLT.title('Matching Map'),PLT.xticks([]),PLT.yticks([])
# PLT.subplot(122),PLT.imshow(picture,cmap = 'gray')
# PLT.title('Detected Point'),PLT.xticks([]),PLT.yticks([])
# PLT.suptitle("TM-CCOEFF-NORMED")

# PLT.show(block=False)
# sleep(3)
# PLT.close()
# figure.savefig(path.join(getcwd(),"TEMPLATE-SOURCE-ALGORITHM.png")) # TODO: _tkinter.TclError: can't invoke "wm" command: application has been destroyed
