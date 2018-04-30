#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/13 18:48
# @Author  : cyj
# @Site    : 
# @File    : captcha.py
# @Software: PyCharm
from pytesseract import *
from PIL import Image


class captcha:
    """验证码识别"""

    def __init__(self, image):
        self.imgname = image
        self.img = Image.open(image)
        self.size = self.img.size
        self.w, self.h = self.size
        maxn = self.size[0] * self.size[1]
        self.dotMap = []
        self.root = [i for i in range(maxn)]
        self.count = [1 for i in range(maxn)]
        self.dx = [1, -1, 0, 0, 1, -1, 1, -1]
        self.dy = [0, 0, 1, -1, 1, -1, -1, 1]
        self.vis = [False for i in range(maxn)]
        self.tmp = []

    def find(self, x):
        """ 查找某个点的root """
        if self.root[x] != x:
            self.root[x] = self.find(self.root[x])
            return self.root[x]
        else:
            return self.root[x]

    def merge(self, x, y):
        """合并root相同的区域"""
        x = self.find(x)
        y = self.find(y)
        if (x == y):
            return
        else:
            self.root[x] = y
            self.count[y] += self.count[x]

    def scanPixel(self):
        """ 扫描点 """
        for x in range(self.w):
            for y in range(self.h):
                if self.img.getpixel((x, y)) == 0:
                    self.dotMap.append((x, y))
                    for i in range(8):
                        sx = self.dx[i] + x
                        sy = self.dy[i] + y
                        if sx < 0 or sy < 0 or sx >= self.w or sy >= self.h:
                            continue
                        if self.img.getpixel((sx, sy)) == 0:
                            self.merge(x * self.h + y, sx * self.h + sy)

    def closeImg(self):
        self.img.close()

    def saveImg(self, name):
        self.img.save(name + "-" + self.imgname)

    def threshold(self):
        """ 二值化 - 采用阈值分割法，threshold为分割点 """
        threshold = 100
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        self.img = self.img.point(table, '1')

    def gray(self):
        """ convert the image to gray """
        self.img = self.img.convert('L')

    def calarea(self, x, y):
        self.vis[self.find(x * self.h + y)] = True
        return self.count[self.find(x * self.h + y)]

    def clear(self):
        for dot in self.dotMap:
            if self.calarea(dot[0], dot[1]) < 15:
                self.img.putpixel(dot, 1)

    def text2String(self):
        """ 识别转换 """
        rep = {'O': '0', 'A': '8',
               'I': '1', 'L': '1',
               'Z': '2', 'S': '8',
               'E': '6', 'G': '9',
               'B': '6', ' ': ''
               }
        self.text = image_to_string(self.img, config="-l eng")
        self.text = self.text.upper()
        print(self.text)
        # for r in rep:
        #   self.text = self.text.replace(r, rep[r])

        if not self.text.isalnum():
            self.text = image_to_string(self.img, config="-l eng")

        # for r in rep:
        #    self.text = self.text.replace(r, rep[r])

    def captcha(self):
        self.gray()
        self.saveImg('1')
        self.threshold()
        self.saveImg('2')
        self.scanPixel()
        self.saveImg('3')
        self.clear()
        self.text2String()
