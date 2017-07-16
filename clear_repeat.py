#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-7-6
# LICENSE: MIT
import os, hashlib
recognized_img = os.listdir('./man_recognize/')
img = os.listdir('./Codes/')

print(recognized_img)

print(img)

hashlist = []

for image in recognized_img:
    f = open('./man_recognize/'+image,'rb')
    md5 = hashlib.md5()
    md5.update(f.read())
    hashlist.append(md5.hexdigest())
    f.close()

for image in img:
    f = open('./Codes/' + image, 'rb')
    md5 = hashlib.md5()
    md5.update(f.read())
    f.close()
    if md5.hexdigest() in hashlist:
        os.system('rm ./Codes/'+image)
        print('rm ', image)
