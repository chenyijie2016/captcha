#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-7-8
# LICENSE: MIT

'''
This file is used to enhance the captcha and split single letter.
'''

from PIL import Image, ImageEnhance, ImageFilter
from pytesseract import *


class ImageProcess(object):
    def __init__(self, image_file):
        self.image_file_name = image_file.split('/')[-1]  # Get file name

        self.image = Image.open(image_file)

        self.image = self.image.convert('L')

        print(self.image_file_name)

    def binarize(self, value=140):
        x, y = self.image.size
        for i in range(x):
            for j in range(y):
                if self.image.getpixel((i, j)) > value:
                    self.image.putpixel((i, j), 255)
                else:
                    self.image.putpixel((i, j), 0)

    def show(self):
        self.image.show()

    def save(self, filename):
        self.image.save(filename)

    def enhance(self):
        img = self.image
        # 去噪
        img = img.filter(ImageFilter.MedianFilter())
        # 亮度加强
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        # im = im.convert('1')
        # im.show()
        self.image = img

    def filter(self):
        x, y = self.image.size
        # clear the interference line in x
        for i in range(y):
            begin = 0
            end = 0
            for j in range(x):
                if self.image.getpixel((j, i)) == 255:
                    if 1 <= end - begin <= 4:
                        for k in range(begin - 1, end + 1):
                            self.image.putpixel((k, i), 255)

                        begin = j
                        end = j
                    if self.image.getpixel((j, i)) == 0:
                        end = j

        # clear the interference line in y
        for i in range(x):
            begin = 0
            end = 0
            for j in range(y):
                if self.image.getpixel((i, j)) == 255:
                    if 1 <= end - begin <= 3:
                        for k in range(begin-1, end + 1):
                            self.image.putpixel((i, k), 255)
                    begin = j
                    end = j
                if self.image.getpixel((i, j)) == 0:
                    end = j

    def cut(self):
        x, y = self.image.size
        for i in range(x):
            for j in range(y):
                if i <= 35 or i >= 165 or j <= 5 or j >= y - 5:
                    self.image.putpixel((i, j), 255)

    def get_text(self):
        self.text = image_to_string(self.image, config='-l eng')
        try:
            if self.text[0] in r"`'“”‘’;./\:；~":
                self.text = self.text[1:-1]
        except BaseException as e:
            pass

        return self.text

    def auto_process(self):
        self.enhance()
        self.binarize()
        self.cut()
        self.filter()
        self.filter()
        # self.get_text()
        # print(self.text)
