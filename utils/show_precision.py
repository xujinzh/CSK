#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 3:21 PM
# @File    : show_precision.py
# @Software: PyCharm

import pylab
from utils import load_video_info


def show_precision(positions, ground_truth, title):
    """
    Calculates precision for a series of distance thresholds (percentage of
    frames where the distance to the ground truth is within the threshold).
    The results are shown in a new figure.

    Accepts positions and ground truth as Nx2 matrices (for N frames), and
    a title string.
    """

    print("Evaluating tracking results.")

    pylab.ioff()  # interactive mode off

    max_threshold = 50  # used for graphs in the paper

    if positions.shape[0] != ground_truth.shape[0]:
        raise Exception(
            "Could not plot precisions, because the number of ground"
            "truth frames does not match the number of tracked frames.")

    # calculate distances to ground truth over all frames
    delta = positions - ground_truth
    distances = pylab.sqrt((delta[:, 0] ** 2) + (delta[:, 1] ** 2))
    # distances[pylab.isnan(distances)] = []

    # compute precisions
    precisions = pylab.zeros((max_threshold, 1), dtype=float)
    for p in range(max_threshold):
        precisions[p] = pylab.sum(distances <= p, dtype=float) / len(distances)

    if False:
        pylab.figure()
        pylab.plot(distances)
        pylab.title("Distances")
        pylab.xlabel("Frame number")
        pylab.ylabel("Distance")

    # plot the precisions
    pylab.figure()  # 'Number', 'off', 'Name',
    pylab.title("Precisions - " + title)
    pylab.plot(precisions, "k-", linewidth=2)
    pylab.xlabel("Threshold")
    pylab.ylabel("Precision")

    pylab.show()
    return


if __name__ == '__main__':
    v_path = '..\\data\\surfer'
    result = load_video_info.load_video_info(video_path=v_path)
    gt = result[4]
    pos = gt
    tt = 'surfer'
    show_precision(positions=pos, ground_truth=gt, title=tt)
