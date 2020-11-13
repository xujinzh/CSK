#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 2:23 PM
# @File    : get_subwindow.py
# @Software: PyCharm

import pylab
import os
from matplotlib import image as mpimg
import numpy as np
from utils import rgb2gray
from matplotlib import pyplot as plt


def get_subwindow(im, pos, sz, cos_window):
    """
    使用 replication padding 从图像中获得子窗口。子窗口以 [y, x] 为坐标中心，大小为 [height, width].
    如果子窗口超过图像边界，则复制图像的边界像素值。获得的子窗口将使用余弦窗口标准化到 [-0.5, 0.5]
    :param im: 输入图像
    :param pos: 子窗口中心点坐标 [y, x]
    :param sz: 子窗口大小 [height, width]
    :param cos_window: 余弦子窗口矩阵
    :return: 返回经过余弦子窗口截取的图像矩形框部分
    """
    # 如果不是高、宽组成的数组，而是一个一维数值，则转化为一个数组
    # 目标是子窗矩形化
    if pylab.isscalar(sz):  # square sub-window
        sz = [sz, sz]
    # 以 pos 为中心，以 sz 为窗口大小建立子窗
    ys = pylab.floor(pos[0]) + pylab.arange(sz[0], dtype=int) - pylab.floor(sz[0] / 2)
    xs = pylab.floor(pos[1]) + pylab.arange(sz[1], dtype=int) - pylab.floor(sz[1] / 2)
    ys = ys.astype(int)
    xs = xs.astype(int)
    # 如果子窗超过坐标，则设置为边界值
    ys[ys < 0] = 0
    ys[ys >= im.shape[0]] = im.shape[0] - 1
    xs[xs < 0] = 0
    xs[xs >= im.shape[1]] = im.shape[1] - 1
    # 提取子窗剪切的图像块
    out = im[pylab.ix_(ys, xs)]
    # 将图像像素值从 [0, 1] 平移到 [-0.5, 0.5]
    out = out.astype(pylab.float64) - 0.5
    # 余弦窗口化，论文公式 (18)

    return pylab.multiply(cos_window, out)


if __name__ == '__main__':
    image_path = r'..\data\surfer\imgs'
    image_list = os.listdir(image_path)
    image = os.path.join(image_path, image_list[0])
    img = mpimg.imread(image)
    gray = rgb2gray.rgb2gray(rgb_image=img)
    position = np.array([152., 286.])
    size = np.array([35., 32.])
    cos_window = pylab.outer(pylab.hanning(size[0]), pylab.hanning(size[1]))
    result = get_subwindow(im=gray, pos=position, sz=size, cos_window=cos_window)
    print(pylab.hanning(size[0]))
    print(cos_window)
    plt.imshow(result)
    plt.show()
