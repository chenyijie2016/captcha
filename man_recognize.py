#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-7-6
# LICENSE: MIT

from PIL import Image
import os

images = [x for x in os.listdir('./Codes/')]

for img in images:

    pic = Image.open('./Codes/' + img)
    pic.show()
    code = input()
    # pic.save('./man_recognize/' + code + '_' + img)
    os.system('cp ./Codes/'+img+' ./man_recognize/'+ code + '_' + img)
    os.system('rm ./Codes/'+img)

