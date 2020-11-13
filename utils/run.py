#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/12/2020 3:58 PM
# @File    : run.py
# @Software: PyCharm

from utils import parse_arguments, track


def just_do_it():
    options = parse_arguments.parse_arguments()

    track.track(options.video_path, options.show_result)

    print("End of game, have a nice day!")
