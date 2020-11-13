#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 3:56 PM
# @File    : parse_arguments.py
# @Software: PyCharm

import os
from optparse import OptionParser


def parse_arguments():
    parser = OptionParser()
    parser.description = \
        "This program will track objects " \
        "on videos in the MILTrack paper format. " \
        "See http://goo.gl/pSTo9r"

    parser.add_option("-i", "--input", dest="video_path",
                      metavar="PATH", type="string", default=None,
                      help="path to a folder o a MILTrack video")
    parser.add_option("-s", "--show", dest="show_result", type="string", default="yes",
                      help="show tracking result or not")

    (options, args) = parser.parse_args()
    # print (options, args)

    if not options.video_path:
        parser.error("'input' option is required to run this program")
    if not os.path.exists(options.video_path):
        parser.error("Could not find the input file %s"
                     % options.video_path)

    return options
