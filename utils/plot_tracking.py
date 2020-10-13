#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 3:30 PM
# @File    : plot_tracking.py
# @Software: PyCharm

import pylab
from matplotlib import cm

debug = False


def plot_tracking(frame, pos, target_sz, im, ground_truth):
    global tracking_figure, tracking_figure_title, tracking_figure_axes, tracking_rectangle, gt_point,\
        z_figure_axes, response_figure_axes, z, response

    timeout = 1e-6
    # timeout = 0.05  # uncomment to run slower
    if frame == 0:
        # pylab.ion()  # interactive mode on
        tracking_figure = pylab.figure()
        gs = pylab.GridSpec(1, 3, width_ratios=[3, 1, 1])

        tracking_figure_axes = tracking_figure.add_subplot(gs[0])
        tracking_figure_axes.set_title("Tracked object (and ground truth)")

        z_figure_axes = tracking_figure.add_subplot(gs[1])
        z_figure_axes.set_title("Template")

        response_figure_axes = tracking_figure.add_subplot(gs[2])
        response_figure_axes.set_title("Response")

        tracking_rectangle = pylab.Rectangle((0, 0), 0, 0)
        tracking_rectangle.set_color((1, 0, 0, 0.5))
        tracking_figure_axes.add_patch(tracking_rectangle)

        gt_point = pylab.Circle((0, 0), radius=5)
        gt_point.set_color((0, 0, 1, 0.5))
        tracking_figure_axes.add_patch(gt_point)

        tracking_figure_title = tracking_figure.suptitle("")

        pylab.show(block=False)

    elif tracking_figure is None:
        return  # we simply go faster by skipping the drawing
    elif not pylab.fignum_exists(tracking_figure.number):
        # print("Drawing window closed, end of game. "
        #      "Have a nice day !")
        # sys.exit()
        print("From now on drawing will be omitted, "
              "so that computation goes faster")
        tracking_figure = None
        return

    tracking_figure_axes.imshow(im, cmap=pylab.cm.gray)

    rect_y, rect_x = tuple(pos - target_sz / 2.0)
    rect_height, rect_width = target_sz
    tracking_rectangle.set_xy((rect_x, rect_y))
    tracking_rectangle.set_width(rect_width)
    tracking_rectangle.set_height(rect_height)

    if len(ground_truth) > 0:
        gt = ground_truth[frame]
        gt_y, gt_x = gt
        gt_point.center = (gt_x, gt_y)

    if z is not None:
        z_figure_axes.imshow(z, cmap=pylab.cm.hot)

    if response is not None:
        response_figure_axes.imshow(response, cmap=pylab.cm.hot)

    tracking_figure_title.set_text("Frame %i (out of %i)"
                                   % (frame + 1, len(ground_truth)))

    if debug and False and (frame % 1) == 0:
        print("Tracked pos ==", pos)

    # tracking_figure.canvas.draw()  # update
    pylab.draw()
    pylab.waitforbuttonpress(timeout=timeout)

    return
