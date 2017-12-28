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
from Xclipboard import paste
from matplotlib import pyplot as PLT
from os import getcwd, path
from time import sleep

H,V = X.size()
print("Screen size is", H, V)

def printscreen():
    X.hotkey("Fn", "PrintScreen")
    image = ImageGrab.grabclipboard()
    image.save("tmp.jpg")

def matching(t, show=False):
    image = cv.imread("tmp.jpg")
    print(image.shape) # TODO: OpenCV的颜色通道BGR、像素矩阵做了转置

    picture = image.copy()
    template = cv.imread(path.join('dingtalk',t))
    width, height, channel = template.shape

    resource = cv.matchTemplate(picture,template,cv.TM_CCOEFF_NORMED)
    minv, maxv, minp, maxp = cv.minMaxLoc(resource)

    top, left = maxp
    bottom, right = top+width, left+height
    if show:
        mark(picture,resource,left,right,top,bottom)
    return left, right, top, bottom

def circle():
    image = cv.imread("tmp.jpg")
    image = cv.medianBlur(image, 5)
    cimage = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    circles = cv.HoughCircles(cimage, cv.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=15, maxRadius=20)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        xyr = []
        for i in circles[0, :]:
            x, y, r = i
            xyr.append((x,y,r))
            # draw the outer circle
            cv.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)

        cv.imshow('circles', image)
        cv.waitKey(0)
        cv.destroyAllWindows()
        print(xyr)
        return xyr

def cursor(left,right,top,bottom):
    X.moveTo((top+bottom)/2,(left+right)/2,duration=3) # TODO: 像素矩阵做了转置

def _cursor(x,y):
    X.moveTo(x,y,duration=3)

def active():
    X.click()
    sleep(3)

def context():
    X.rightClick()
    sleep(3)

procedure = [
    {
        "step":0,
        "template":"contact-button.png",
        "action":"active",
        "next":[1]
    },
    {
        "step":1,
        "template":"contact-structure.png",
        "action":"active",
        "next":[2]
    },
    {
        "step":2,
        "template":"contact-subordinate.png",
        "action":"active",
        "next":[2,3,7]
    },
    {
        "step":3,
        "template":None,
        "action":"circle",
        "next":[4,7]
    },
    {
        "step":4,
        "template":None,
        "action":"active",
        "next":[5,1]
    },
    {
        "step":5,
        "template":["contact-name.png", "contact-phonenumber.png"],
        "action":"context",
        "next":[6]
    },
    {
        "step":6,
        "template":"contact-copy.png",
        "action":"active",
        "next":[-1] # TODO: 最简陋版本（阅完领导就闪）
    },
    {
        "step":7,
        "template":None,
        "action":"scroll",
        "next":{True:"last",False:"last.last"}
    },
    {
        "step":-1,
        "template":None,
        "action":"over",
        "next":[]
    }
]

class GLOBALBITCH:
    LIMIT = 13
    kickoff = 0

def do(step):
    while True:
        GLOBALBITCH.kickoff += 1
        if GLOBALBITCH.kickoff > GLOBALBITCH.LIMIT:
            break
        printscreen()
        process = procedure[step]
        t = process.get("template")
        if isinstance(t, str):
            t = [t]
        for tt in t:
            left, right, top, bottom = matching(tt)
            cursor(left, right, top, bottom)
            method = eval(process.get("action", "passby"))
            r = method()
            if r is not None:
                for m,n,r in r:
                    _cursor(m, n)
                    active()
                    do(4) # TODO: 点击每个圆形头像
            then = process.get("next")
            for x in then:
                do(x) # TODO: 破除递归

def stupido():
    printscreen()
    left, right, top, bottom = matching("contact-button.png", True)
    cursor(left, right, top, bottom)
    active()
    X.moveRel(100, 75, duration=2)
    active()
    X.moveRel(256, -72, duration=2)
    active()
    printscreen()
    for x,y,r in circle():
        if y < 48:
            continue
        _cursor(x,y)
        active()
        printscreen()
        left, right, top, bottom = matching("contact-card.png")
        cursor(left, right, top, bottom)
        X.moveRel(64, 48, duration=2)
        context()
        # printscreen()
        # left, right, top, bottom = matching("contact-copy.png")
        # cursor(left, right, top, bottom)
        X.moveRel(32, 24, duration=1)
        active()
        left, right, top, bottom = matching("nppp.png")
        cursor(left, right, top, bottom)
        active()
        X.hotkey("ctrl", "v")
        break

def passby(*args, **kwargs):
    print("=====PASSBY=====")
    pprint(args)
    pprint(kwargs)

def imageinfo(image):
    if isinstance(image, Image.Image):
        print(image.format, image.size, image.mode)
        h, v = image.size
        print(h, v)
        pixels = image.load()
        print(pixels)
        for x in range(h):
            for y in range(v):
                print(pixels[x, y])

def mark(picture,resource,left,right,top,bottom):
    cv.rectangle(picture,(top,left), (bottom,right), 255, 2)

    PLT.ion()
    figure = PLT.figure('TITLE @ SOURCE @ TEMPLATE @ COST')
    PLT.subplot(121),PLT.imshow(resource,cmap = 'gray')
    PLT.title('Matching Map'),PLT.xticks([]),PLT.yticks([])
    PLT.subplot(122),PLT.imshow(picture,cmap = 'gray')
    PLT.title('Detected Point'),PLT.xticks([]),PLT.yticks([])
    PLT.suptitle("TM-CCOEFF-NORMED")

    PLT.pause(5)
    # PLT.show(block=True)
    PLT.close()
    # figure.savefig(path.join(getcwd(),"TEMPLATE-SOURCE-ALGORITHM.png")) # TODO: _tkinter.TclError: can't invoke "wm" command: application has been destroyed

def test():
    image = cv.imread("tmp.jpg", 0)  # 直接读为灰度图像
    _, a = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
    _, b = cv.threshold(image, 127, 255, cv.THRESH_BINARY_INV)
    _, c = cv.threshold(image, 127, 255, cv.THRESH_TRUNC)
    _, d = cv.threshold(image, 127, 255, cv.THRESH_TOZERO)
    _, e = cv.threshold(image, 127, 255, cv.THRESH_TOZERO_INV)
    titles = ['GRAY', 'BINARY', 'BINARY-INV', 'TRUNC', 'TOZERO', 'TOZERO-INV']
    images = [image, a, b, c, d, e]
    figure = PLT.figure('test')
    for i in range(len(images)):
        PLT.subplot(2,3,i+1)
        PLT.imshow(images[i],"gray")
        PLT.title(titles[i])
        PLT.xticks([]), PLT.yticks([])
    PLT.show()

if __name__ == "__main__":
    # printscreen()
    # circle()
    # print(matching("contact-copy.png"))
    # print(matching("contact-name.png"))
    # print(matching("contact-phonenumber.png"))
    # print(matching("contact-structure.png"))
    # print(matching("contact-subordinate-double.png"))
    # print(matching("contact-button.png"))
    # test()
    stupido()
