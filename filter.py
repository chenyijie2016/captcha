#!/usr/bin/env python
# -*- coding: utf-8 -*-     
# Copyright (c) 2017 cyj <chenyijiethu@gmail.com>
# Date: 17-7-9
# LICENSE: MIT

from skimage import io, measure, color, morphology
import matplotlib.pyplot as plt
import numpy as np


class Filter(object):
    def __init__(self, image_file):
        self.img = self.image = io.imread(image_file)
        self.image_name = image_file.split('/')[-1]
        self.labels = None
        self.dst = None

    def binarize(self):
        for x in np.nditer(self.image, op_flags=['readwrite']):
            if x > 100:
                x[...] = 255
            else:
                x[...] = 0

    def remove_small(self):
        self.dst = morphology.remove_small_objects(self.labels, min_size=200, connectivity=2)
        for x in np.nditer(self.dst, op_flags=['readwrite']):
            if x == 0:
                x[...] = 255
            else:
                x[...] = 0

    def label(self):
        self.labels = measure.label(self.image, connectivity=2, background=255)

    def show(self):

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        ax1.imshow(self.img, plt.cm.gray, interpolation='nearest')
        ax2.imshow(self.dst, plt.cm.gray, interpolation='nearest')
        fig.tight_layout()
        plt.show()

    def save(self, filename):
        io.imsave(filename, self.dst)

    def auto_process(self, filename):
        self.binarize()
        self.label()
        self.remove_small()
        self.save(filename)
