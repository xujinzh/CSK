#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 3:04 PM
# @File    : dense_gauss_kernel.py
# @Software: PyCharm

import pylab
import os
from utils import rgb2gray
from matplotlib import image as mpimg


def dense_gauss_kernel(sigma, x, y=None):
    """
    通过高斯核计算余弦子窗口图像块的响应图
    利用带宽是 sigma 的高斯核估计两个图像块 X (MxN) 和 Y (MxN) 的关系。X, Y 是循环的、经余弦窗处理的。输出结果是
    响应图矩阵 MxN. 如果 X = Y, 则函数调用时取消 y，则加快计算。
    该函数对应原文中的公式 (16)，以及算法1中的 function k = dgk(x1, x2, sigma)
    :param sigma: 高斯核带宽
    :param x: 余弦子窗口图像块
    :param y: 空或者模板图像块
    :return: 响应图
    """
    # 计算图像块 x 的傅里叶变换
    xf = pylab.fft2(x)  # x in Fourier domain
    # 把图像块 x 拉平
    x_flat = x.flatten()
    # 计算 x 的2范数平方
    xx = pylab.dot(x_flat.transpose(), x_flat)  # squared norm of x

    if y is not None:
        # 一半情况， x 和 y 是不同的，计算 y 的傅里叶变化和2范数平方
        yf = pylab.fft2(y)
        y_flat = y.flatten()
        yy = pylab.dot(y_flat.transpose(), y_flat)
    else:
        # x 的自相关，避免重复计算
        yf = xf
        yy = xx

    # 傅里叶域的互相关计算，逐元素相乘
    xyf = pylab.multiply(xf, pylab.conj(yf))

    # 转化为频率域
    xyf_ifft = pylab.ifft2(xyf)
    # 对频率域里的矩阵块进行滚动平移，分别沿 row 和 col 轴
    row_shift, col_shift = pylab.floor(pylab.array(x.shape) / 2).astype(int)
    xy_complex = pylab.roll(xyf_ifft, row_shift, axis=0)
    xy_complex = pylab.roll(xy_complex, col_shift, axis=1)
    xy = pylab.real(xy_complex)

    # 计算高斯核响应图
    scaling = -1 / (sigma ** 2)
    xx_yy = xx + yy
    xx_yy_2xy = xx_yy - 2 * xy

    return pylab.exp(scaling * pylab.maximum(0, xx_yy_2xy / x.size))


if __name__ == '__main__':
    image_path = r'..\data\surfer\imgs'
    image_list = os.listdir(image_path)
    image = os.path.join(image_path, image_list[0])
    img = mpimg.imread(image)
    gray = rgb2gray.rgb2gray(img)
    sgm = 0.2
    kernel = dense_gauss_kernel(sigma=sgm, x=gray)
    print(kernel)
