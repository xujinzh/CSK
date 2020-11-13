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
import time
import numpy as np
from PIL import Image

debug = False


def track(input_video_path, show_tracking):
    """
    注意：以 f 结尾的变量表示频率域
    """

    # 目标周围的额外区域
    padding = 1.0
    # 空间带宽，与目标成比例
    output_sigma_factor = 1 / float(16)
    # 高斯核带宽
    sigma = 0.2
    # 正则化系数
    lambda_value = 1e-2
    # 线性插值因子
    interpolation_factor = 0.075
    # 加载视频信息，包括待测试的每帧图片列表，首帧目标矩形框中心点坐标[y,x]，矩形框高、宽一半的大小，是否进行图片缩放一半
    # 每帧图片的 ground truth 信息，视频路径
    info = load_video_info.load_video_info(input_video_path)
    img_files, pos, target_sz, should_resize_image, ground_truth, video_path = info

    # 把填充考虑进去，定义为窗口大小。
    sz = pylab.floor(target_sz * (1 + padding))

    # 计算想要的高斯形状的输出，其中带宽正比于目标矩形框大小
    output_sigma = pylab.sqrt(pylab.prod(target_sz)) * output_sigma_factor
    # 平移目标矩形框的高度，以中心点为圆点，得到高度坐标列表
    # 平移目标矩形框的宽度，以中心点为圆点，得到宽度坐标列表
    grid_y = pylab.arange(sz[0]) - pylab.floor(sz[0] / 2)
    grid_x = pylab.arange(sz[1]) - pylab.floor(sz[1] / 2)
    # 把坐标列表边长坐标矩阵，即对二维平面范围内的区域进行网格划分
    rs, cs = pylab.meshgrid(grid_x, grid_y)
    # 论文中公式 (19)，计算得到 [0, 1] 值，越靠近中心点值越大，反之越小
    y = pylab.exp((-0.5 / output_sigma ** 2) * (rs ** 2 + cs ** 2))
    # 计算二维离散傅里叶变换
    yf = pylab.fft2(y)

    # 首先计算矩形框高（某一个整数值）的 Hanning 窗（加权的余弦窗），其次计算矩形框宽的 Hanning 窗
    # 最后计算两个向量的外积得到矩形框的余弦窗
    cos_window = pylab.outer(pylab.hanning(sz[0]), pylab.hanning(sz[1]))
    # 计算 FPS
    total_time = 0  # to calculate FPS
    # 计算精度值
    positions = pylab.zeros((len(img_files), 2))  # to calculate precision

    # global z, response
    plot_tracking.z = None
    alphaf = None
    plot_tracking.response = None
    # 依次访问图像从图像名列表中
    for frame, image_filename in enumerate(img_files):
        if (frame % 10) == 0:
            print("Processing frame", frame)
        # 读取图像
        image_path = os.path.join(video_path, image_filename)
        im = pylab.imread(image_path)
        # 如果图像是彩色图像，则转化为灰度图像
        if len(im.shape) == 3 and im.shape[2] > 1:
            im = rgb2gray.rgb2gray(im)
        # 如果需要进行图像缩放，则缩放为原来一半
        if should_resize_image:
            im = np.array(Image.fromarray(im).resize((int(im.shape[0] / 2), int(im.shape[1] / 2))))

        # 开始计时
        start_time = time.time()

        # 提取并预处理子窗口，采用余弦子窗口
        x = get_subwindow.get_subwindow(im, pos, sz, cos_window)

        is_first_frame = (frame == 0)
        # 不过不是第一帧，则计算分类器的响应
        if not is_first_frame:
            # 计算分类器在所有位置上的相应
            k = dense_gauss_kernel.dense_gauss_kernel(sigma, x, plot_tracking.z)
            kf = pylab.fft2(k)
            alphaf_kf = pylab.multiply(alphaf, kf)
            plot_tracking.response = pylab.real(pylab.ifft2(alphaf_kf))  # Eq. 9

            # 最大响应就是目标位置
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

        # 获取目标位置的余弦窗口，用于训练分类器
        x = get_subwindow.get_subwindow(im, pos, sz, cos_window)

        # kernel 最小方差正则化，在傅里叶域计算参数 ALPHA
        k = dense_gauss_kernel.dense_gauss_kernel(sigma, x)
        new_alphaf = pylab.divide(yf, (pylab.fft2(k) + lambda_value))  # Eq. 7
        new_z = x

        if is_first_frame:
            # 对于第一帧，训练单张图片
            alphaf = new_alphaf
            plot_tracking.z = x
        else:
            # 对于后续帧，进行模型参数插值
            f = interpolation_factor
            alphaf = (1 - f) * alphaf + f * new_alphaf
            plot_tracking.z = (1 - f) * plot_tracking.z + f * new_z

        # 保持当前位置，并计算 FPS
        positions[frame, :] = pos
        total_time += time.time() - start_time

        # 可视化显示跟踪的结果
        if show_tracking == "yes":
            plot_tracking.plot_tracking(frame, pos, target_sz, im, ground_truth)

    if should_resize_image:
        positions = positions * 2

    print("Frames-per-second:", len(img_files) / total_time)

    title = os.path.basename(os.path.normpath(input_video_path))

    if len(ground_truth) > 0:
        # 画出精确率图像
        show_precision.show_precision(positions, ground_truth, title)


if __name__ == '__main__':
    v_path = '..\\data\\surfer'
    track(input_video_path=v_path)
