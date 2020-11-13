#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 1:54 PM
# @File    : rgb2gray.py
# @Software: PyCharm

import pylab
from matplotlib import pyplot as plt
import os
import matplotlib.image as mpimg


def rgb2gray(rgb_image):
    """
    从 RGB 图像加权求和得到灰度图像，参考 http://stackoverflow.com/questions/12201577
     [0.299, 0.587, 0.114] 分别对应 R, G, B 三通道的加权系数
    :param rgb_image: 彩色 RGB 图像
    :return: 灰度图像
    """

    return pylab.dot(rgb_image, [0.299, 0.587, 0.114])


if __name__ == '__main__':
    img_path = '../data/surfer/imgs'
    rgb_list = os.listdir(img_path)
    # print(rgb_list)
    rgb = os.path.join(img_path, rgb_list[0])
    # print(rgb)

    img = mpimg.imread(rgb)

    imgplot = plt.imshow(img)
    plt.show()

    gray = rgb2gray(rgb_image=img)

    img_gray_plot = plt.imshow(gray)
    plt.show()
