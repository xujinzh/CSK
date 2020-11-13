#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/9/2020 5:39 PM
# @File    : load_video_info.py
# @Software: PyCharm

import os
import os.path
import glob
import pylab


def load_video_info(video_path):
    """
    加载给定视频路径下的视频相关的所有信息，包括：待检测的每帧图片名列表，首帧目标矩形框中心点位置 (1x2)，首帧目标矩形框的
    一半 (1x2)，是否将视频调整为一半（布尔型变量）缩放分辨率，计算精确度的 ground truth 信息 (Nx2, N 表示帧数)，
    视频路径。坐标顺序采用 [y, x]，对于的矩形框为高、宽。
    :param video_path: 视频或图像序列路径
    :return: 目标检测算法需要的相关信息，具体如上面描述
    """

    # 加载 ground truth 文件路径，MIL Track's 格式，以 _gt.txt 结尾。文件中包含目标中心点坐标和矩形框宽高值
    # text_files 是列表，其中第一个元素为 ground truth 文件的完整路径
    text_files = glob.glob(os.path.join(video_path, "*_gt.txt"))
    # 如果不存在该文件，则返回错误提示信息
    assert text_files, "No initial position and ground truth (*_gt.txt) to load."
    # 读取 ground truth 完整路径
    first_file_path = text_files[0]
    # 读取以逗号分隔的 ground truth 文件数值
    # 每行对应一帧，并包含 “x, y, width, height”; 请注意，此信息仅适用于每5帧中的1帧，其余信息用0填充
    # x, y 表示目标矩形框左下角坐标，width, height 表示目标矩形框宽度和高度
    ground_truth = pylab.loadtxt(first_file_path, delimiter=",")
    # 把第一帧的位置信息读出来作为首帧目标初始化
    first_ground_truth = ground_truth[0, :]
    # 获取首帧目标矩形框的高度和宽度
    target_sz = pylab.array([first_ground_truth[3], first_ground_truth[2]])
    # 获取首帧目标矩形框的中心坐标 [y_center, x_center]
    pos = [first_ground_truth[1], first_ground_truth[0]] + pylab.floor(target_sz / 2)
    # 如果 ground truth 非空，则进行插值其他帧的位置坐标值，并转化为目标中心坐标值
    if ground_truth is not None:
        # 分别依次插值 x, y, width, height 列，而不是一行一行插值
        for i in range(4):
            # xp 表示那些有非零值的 ground truth 行
            xp = range(0, ground_truth.shape[0], 5)
            # fp 表示非零值的 ground truth 每列的值
            fp = ground_truth[xp, i]
            # x 表示所有帧的个数组成的列表
            x = range(ground_truth.shape[0])
            # 调用 numpy 的一维线性插值为 ground truth 中为零的插值
            ground_truth[:, i] = pylab.interp(x, xp, fp)
        # 根据矩形框左下角坐标和高宽值计算得到目标中心点坐标
        ground_truth = ground_truth[:, [1, 0]] + ground_truth[:, [3, 2]] / 2
    # 如果不存在 ground truth 文件，则提示，并赋值为空
    else:
        print("Failed to gather ground truth data")
        ground_truth = []
    # 列举所有帧信息。首先从文件 "*_frames.txt" 中读取开始帧和结束帧数值，如果不存在，则读取 "imgs" 文件夹中的所有图片
    # 读取文件 "*_frames.txt" 的路径，结果是包含 "_frames.txt" 为结尾的所有文件的列表
    text_files = glob.glob(os.path.join(video_path, "*_frames.txt"))
    # 如果存在待检测帧开始帧和结束帧值文件
    if text_files:
        # 默认只有一个 "_frames.txt" 文件，所以第一个就是该文件，记录开始帧和结束帧
        first_file_path = text_files[0]
        # 读取开始帧和结束帧数值
        frames = pylab.loadtxt(first_file_path, delimiter=",", dtype=int)
        # 测试首帧图片是否存在与图片文件夹 "imgs" 中
        # %05i 表示替换值为整数，输出格式是5位，不足5位前面添加0
        test1_path_to_img = os.path.join(video_path, "imgs/img%05i.png" % frames[0])
        test2_path_to_img = os.path.join(video_path, "img%05i.png" % frames[0])
        # 如果图片在 "imgs" 文件夹下
        if os.path.exists(test1_path_to_img):
            video_path = os.path.join(video_path, "imgs/")
        # 如果图片在 video_path 文件夹下
        elif os.path.exists(test2_path_to_img):
            video_path = video_path
        # 如果图片既不在 "imgs" 文件夹下，也不在 video_path 文件夹下，则提示错误
        else:
            raise Exception("Failed to find the png images")
        # 把所有图片组成一个列表
        img_files = ["img%05i.png" % i for i in range(frames[0], frames[1] + 1)]
    # 如果不存在 "_frames.txt" 文件，则直接从 video_path 读取图片
    else:
        # 把 video_path 下面的 "png" 文件组成列表
        img_files = glob.glob(os.path.join(video_path, "*.png"))
        # 如果没有 "png" 文件，则读取 "jpg" 文件
        if len(img_files) == 0:
            img_files = glob.glob(os.path.join(video_path, "*.jpg"))
        # 如果两种类型的图片都不存在，则提示错误
        assert len(img_files), "Failed to find png or jpg images"
        # 对图片列表进行按照字符串字典排列
        img_files.sort()
    # 如果初始目标矩形框太大，如超过100个像素，则缩放为原来一半，即使用低分辨率
    if pylab.sqrt(pylab.prod(target_sz)) >= 100:
        pos = pylab.floor(pos / 2)
        target_sz = pylab.floor(target_sz / 2)
        resize_image = True
    # 如果不是，则不用缩放
    else:
        resize_image = False
    # 返回视频（所有帧图像）的信息，包括每帧图像列表，首帧目标矩形框中心点坐标[y_center, x_center]，首帧目标矩形框的
    # 高、宽的一半，是否对图片进行缩放，检测帧的 ground_truth，视频路径
    return [img_files, pos, target_sz, resize_image, ground_truth, video_path]


if __name__ == '__main__':
    v_path = '../data/surfer'
    res = load_video_info(video_path=v_path)
    print(res[2])
    print(type(res[2]))
