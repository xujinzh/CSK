#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/9/2020 5:39 PM
# @File    : load_video_info.py
# @Software: PyCharm

# from __future__ import print_function
import os
import os.path
import glob
import pylab


def load_video_info(video_path):
    """
    Loads all the relevant information for the video in the given path:
    the list of image files (cell array of strings), initial position
    (1x2), target size (1x2), whether to resize the video to half
    (boolean), and the ground truth information for precision calculations
    (Nx2, for N frames). The ordering of coordinates is always [y, x].

    The path to the video is returned, since it may change if the images
    are located in a sub-folder (as is the default for MILTrack's videos).
    """

    # load ground truth from text file (MILTrack's format)
    text_files = glob.glob(os.path.join(video_path, "*_gt.txt"))
    assert text_files, \
        "No initial position and ground truth (*_gt.txt) to load."
    # print("text files:", text_files)

    # first_file_path = os.path.join(video_path, text_files[0])
    first_file_path = text_files[0]
    # print("first file path:", first_file_path)
    # f = open(first_file_path, "r")
    # ground_truth = textscan(f, '%f,%f,%f,%f') # [x, y, width, height]
    # ground_truth = cat(2, ground_truth{:})
    ground_truth = pylab.loadtxt(first_file_path, delimiter=",")
    # print("ground_truth:", ground_truth)
    # f.close()

    # set initial position and size
    first_ground_truth = ground_truth[0, :]
    # print("first ground truth:", first_ground_truth)
    # target_sz contains height, width
    target_sz = pylab.array([first_ground_truth[3], first_ground_truth[2]])
    # print("target size:", target_sz)
    # pos contains y, x center
    pos = [first_ground_truth[1], first_ground_truth[0]] + pylab.floor(target_sz / 2)
    # print("pos:", pos)
    # print("ground truth shape:", ground_truth.shape)
    # try:
    if ground_truth is not None:
        # interpolate missing annotations
        # 4 out of each 5 frames is filled with zeros
        for i in range(4):  # x, y, width, height
            # xp 表示那些有真实值的 ground truth
            xp = range(0, ground_truth.shape[0], 5)
            # print("xp:", xp)
            # fp 表示真实值的 ground truth 每列的值
            fp = ground_truth[xp, i]
            # print("fp:", fp)
            # x 表示所有帧长度
            x = range(ground_truth.shape[0])
            # 插值，调用 numpy 的一维线性插值
            ground_truth[:, i] = pylab.interp(x, xp, fp)
        # store positions instead of boxes
        # 得到的是二维的坐标，指向边界框的右上角位置
        ground_truth = ground_truth[:, [1, 0]] + ground_truth[:, [3, 2]] / 2
        # print("ground truth after interpolation:", ground_truth)
        # print("ground truth shape after interp:", ground_truth.shape)
    # except Exception as e:
    else:
        print("Failed to gather ground truth data")
        # print("Error", e)
        # ok, wrong format or we just don't have ground truth data.
        ground_truth = []

    # list all frames. first, try MILTrack's format, where the initial and
    # final frame numbers are stored in a text file. if it doesn't work,
    # try to load all png/jpg files in the folder.

    text_files = glob.glob(os.path.join(video_path, "*_frames.txt"))
    # print("text files:", text_files)
    if text_files:
        # first_file_path = os.path.join(video_path, text_files[0])
        first_file_path = text_files[0]
        # print("first file path:", first_file_path)
        # f = open(first_file_path, "r")
        # frames = textscan(f, '%f,%f')
        frames = pylab.loadtxt(first_file_path, delimiter=",", dtype=int)
        # print("frames:", frames)
        # f.close()

        # see if they are in the 'imgs' subfolder or not
        # print("imgs/img%05i.png" % frames[0])
        test1_path_to_img = os.path.join(video_path, "imgs/img%05i.png" % frames[0])
        test2_path_to_img = os.path.join(video_path, "img%05i.png" % frames[0])
        if os.path.exists(test1_path_to_img):
            video_path = os.path.join(video_path, "imgs/")
        elif os.path.exists(test2_path_to_img):
            video_path = video_path  # no need for change
        else:
            raise Exception("Failed to find the png images")

        # list the files
        img_files = ["img%05i.png" % i
                     for i in range(frames[0], frames[1] + 1)]
        # print("img files:", img_files)
        # img_files = num2str((frames{1} : frames{2})', 'img%05i.png')
        # img_files = cellstr(img_files);
    else:
        # no text file, just list all images
        img_files = glob.glob(os.path.join(video_path, "*.png"))
        if len(img_files) == 0:
            img_files = glob.glob(os.path.join(video_path, "*.jpg"))

        assert len(img_files), "Failed to find png or jpg images"

        img_files.sort()

    # if the target is too large, use a lower resolution
    # no need for so much detail
    if pylab.sqrt(pylab.prod(target_sz)) >= 100:
        pos = pylab.floor(pos / 2)
        target_sz = pylab.floor(target_sz / 2)
        resize_image = True
    else:
        resize_image = False

    ret = [img_files, pos, target_sz, resize_image, ground_truth, video_path]
    return ret


if __name__ == '__main__':
    v_path = '..\\data\\surfer'
    result = load_video_info(video_path=v_path)
    print(result)
