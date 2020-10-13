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
    Gaussian Kernel with dense sampling.
    Evaluates a gaussian kernel with bandwidth SIGMA for all displacements
    between input images X and Y, which must both be MxN. They must also
    be periodic (ie., pre-processed with a cosine window). The result is
    an MxN map of responses.

    If X and Y are the same, omit the third parameter to re-use some
    values, which is faster.
    """

    xf = pylab.fft2(x)  # x in Fourier domain
    x_flat = x.flatten()
    xx = pylab.dot(x_flat.transpose(), x_flat)  # squared norm of x

    if y is not None:
        # general case, x and y are different
        yf = pylab.fft2(y)
        y_flat = y.flatten()
        yy = pylab.dot(y_flat.transpose(), y_flat)
    else:
        # auto-correlation of x, avoid repeating a few operations
        yf = xf
        yy = xx

    # cross-correlation term in Fourier domain
    xyf = pylab.multiply(xf, pylab.conj(yf))

    # to spatial domain
    xyf_ifft = pylab.ifft2(xyf)
    # xy_complex = circshift(xyf_ifft, floor(x.shape/2))
    row_shift, col_shift = pylab.floor(pylab.array(x.shape) / 2).astype(int)
    xy_complex = pylab.roll(xyf_ifft, row_shift, axis=0)
    xy_complex = pylab.roll(xy_complex, col_shift, axis=1)
    xy = pylab.real(xy_complex)

    # calculate gaussian response for all positions
    scaling = -1 / (sigma ** 2)
    xx_yy = xx + yy
    xx_yy_2xy = xx_yy - 2 * xy
    k = pylab.exp(scaling * pylab.maximum(0, xx_yy_2xy / x.size))

    # print("dense_gauss_kernel x.shape ==", x.shape)
    # print("dense_gauss_kernel k.shape ==", k.shape)

    return k


if __name__ == '__main__':
    image_path = r'..\data\surfer\imgs'
    image_list = os.listdir(image_path)
    image = os.path.join(image_path, image_list[0])
    img = mpimg.imread(image)
    gray = rgb2gray.rgb2gray(img)
    sgm = 2
    kernel = dense_gauss_kernel(sigma=sgm, x=gray)
    print(kernel)
