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

debug = False


def get_subwindow(im, pos, sz, cos_window):
    """
    Obtain sub-window from image, with replication-padding.
    Returns sub-window of image IM centered at POS ([y, x] coordinates),
    with size SZ ([height, width]). If any pixels are outside of the image,
    they will replicate the values at the borders.

    The sub-window is also normalized to range -0.5 .. 0.5, and the given
    cosine window COS_WINDOW is applied
    (though this part could be omitted to make the function more general).
    """

    if pylab.isscalar(sz):  # square sub-window
        sz = [sz, sz]

    ys = pylab.floor(pos[0]) + pylab.arange(sz[0], dtype=int) - pylab.floor(sz[0] / 2)
    xs = pylab.floor(pos[1]) + pylab.arange(sz[1], dtype=int) - pylab.floor(sz[1] / 2)

    ys = ys.astype(int)
    xs = xs.astype(int)

    # check for out-of-bounds coordinates,
    # and set them to the values at the borders
    ys[ys < 0] = 0
    ys[ys >= im.shape[0]] = im.shape[0] - 1

    xs[xs < 0] = 0
    xs[xs >= im.shape[1]] = im.shape[1] - 1
    # zs = range(im.shape[2])

    # extract image
    # out = im[pylab.ix_(ys, xs, zs)]
    out = im[pylab.ix_(ys, xs)]

    if debug:
        print("Out max/min value==", out.max(), "/", out.min())
        pylab.figure()
        pylab.imshow(out, cmap=pylab.cm.gray)
        pylab.title("cropped subwindow")

    # pre-process window --
    # normalize to range -0.5 .. 0.5
    # pixels are already in range 0 to 1
    out = out.astype(pylab.float64) - 0.5

    # apply cosine window
    out = pylab.multiply(cos_window, out)

    return out


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
    print(result)
    plt.imshow(result)
    plt.show()
