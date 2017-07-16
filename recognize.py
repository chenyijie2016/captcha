#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-7-9
# LICENSE: MIT

'''
自动图片处理
'''

from image_process import ImageProcess

from filter import Filter

import os

ORANGIN = './ORANGIN/'
TEMP = './TMP/'
TARGET = './TARGET/'

images = os.listdir(ORANGIN)
for img in images:
    a = ImageProcess(ORANGIN + img)
    a.auto_process()
    # a.show()
    a.save(TEMP + img)

images = os.listdir(TEMP)

for img in images:
    a = Filter(TEMP + img)
    a.auto_process(TARGET + img)
