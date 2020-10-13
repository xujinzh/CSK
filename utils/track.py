#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 3:37 PM
# @File    : track.py
# @Software: PyCharm

import pylab
import os
from utils import load_video_info, rgb2gray, get_subwindow, dense_gauss_kernel, plot_tracking, \
    show_precision
import scipy
import time

debug = False


def track(input_video_path):
    """
    notation: variables ending with f are in the frequency domain.
    """

    # parameters according to the paper --
    padding = 1.0  # extra area surrounding the target
    # spatial bandwidth (proportional to target)
    output_sigma_factor = 1 / float(16)
    sigma = 0.2  # gaussian kernel bandwidth
    lambda_value = 1e-2  # regularization
    # linear interpolation factor for adaptation
    interpolation_factor = 0.075

    info = load_video_info.load_video_info(input_video_path)
    img_files, pos, target_sz, should_resize_image, ground_truth, video_path = info

    # window size, taking padding into account
    sz = pylab.floor(target_sz * (1 + padding))

    # desired output (gaussian shaped), bandwidth proportional to target size
    output_sigma = pylab.sqrt(pylab.prod(target_sz)) * output_sigma_factor

    grid_y = pylab.arange(sz[0]) - pylab.floor(sz[0] / 2)
    grid_x = pylab.arange(sz[1]) - pylab.floor(sz[1] / 2)
    # [rs, cs] = ndgrid(grid_x, grid_y)
    rs, cs = pylab.meshgrid(grid_x, grid_y)
    y = pylab.exp(-0.5 / output_sigma ** 2 * (rs ** 2 + cs ** 2))
    yf = pylab.fft2(y)
    # print("yf.shape ==", yf.shape)
    # print("y.shape ==", y.shape)

    # store pre-computed cosine window
    cos_window = pylab.outer(pylab.hanning(sz[0]),
                             pylab.hanning(sz[1]))

    total_time = 0  # to calculate FPS
    positions = pylab.zeros((len(img_files), 2))  # to calculate precision

    # global z, response
    plot_tracking.z = None
    alphaf = None
    plot_tracking.response = None

    for frame, image_filename in enumerate(img_files):

        if True and ((frame % 10) == 0):
            print("Processing frame", frame)

        # load image
        image_path = os.path.join(video_path, image_filename)
        im = pylab.imread(image_path)
        if len(im.shape) == 3 and im.shape[2] > 1:
            im = rgb2gray.rgb2gray(im)

        # print("Image max/min value==", im.max(), "/", im.min())

        if should_resize_image:
            im = scipy.misc.imresize(im, 0.5)

        start_time = time.time()

        # extract and pre-process subwindow
        x = get_subwindow.get_subwindow(im, pos, sz, cos_window)

        is_first_frame = (frame == 0)

        if not is_first_frame:
            # calculate response of the classifier at all locations
            k = dense_gauss_kernel.dense_gauss_kernel(sigma, x, plot_tracking.z)
            kf = pylab.fft2(k)
            alphaf_kf = pylab.multiply(alphaf, kf)
            plot_tracking.response = pylab.real(pylab.ifft2(alphaf_kf))  # Eq. 9

            # target location is at the maximum response
            r = plot_tracking.response
            row, col = pylab.unravel_index(r.argmax(), r.shape)
            pos = pos - pylab.floor(sz / 2) + [row, col]

            if debug:
                print("Frame ==", frame)
                print("Max response", r.max(), "at", [row, col])
                pylab.figure()
                pylab.imshow(cos_window)
                pylab.title("cos_window")

                pylab.figure()
                pylab.imshow(x)
                pylab.title("x")

                pylab.figure()
                pylab.imshow(plot_tracking.response)
                pylab.title("response")
                pylab.show(block=True)

        # end "if not first frame"

        # get subwindow at current estimated target position,
        # to train classifer
        x = get_subwindow.get_subwindow(im, pos, sz, cos_window)

        # Kernel Regularized Least-Squares,
        # calculate alphas (in Fourier domain)
        k = dense_gauss_kernel.dense_gauss_kernel(sigma, x)
        new_alphaf = pylab.divide(yf, (pylab.fft2(k) + lambda_value))  # Eq. 7
        new_z = x

        if is_first_frame:
            # first frame, train with a single image
            alphaf = new_alphaf
            plot_tracking.z = x
        else:
            # subsequent frames, interpolate model
            f = interpolation_factor
            alphaf = (1 - f) * alphaf + f * new_alphaf
            plot_tracking.z = (1 - f) * plot_tracking.z + f * new_z
        # end "first frame or not"

        # save position and calculate FPS
        positions[frame, :] = pos
        total_time += time.time() - start_time

        # visualization
        plot_tracking.plot_tracking(frame, pos, target_sz, im, ground_truth)
    # end of "for each image in video"

    if should_resize_image:
        positions = positions * 2

    print("Frames-per-second:", len(img_files) / total_time)

    title = os.path.basename(os.path.normpath(input_video_path))

    if len(ground_truth) > 0:
        # show the precisions plot
        show_precision.show_precision(positions, ground_truth, title)


if __name__ == '__main__':
    v_path = '..\\data\\surfer'
    track(input_video_path=v_path)
