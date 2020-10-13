#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Jinzhong Xu
# @Contact : jinzhongxu@csu.ac.cn
# @Time    : 10/9/2020 5:34 PM
# @File    : CirculantMatrixTracker.py
# @Software: PyCharm

from __future__ import print_function

import os
import os.path
import sys
import glob
import time
from optparse import OptionParser
import scipy.misc
import pylab

debug = False


class CirculantMatrixTracker:

    def __init__(self, object_example):
        """
        object_example is an image showing the object to track
        """

        return

    def find(self, image):
        """
        Will return the x/y coordinates where the object was found,
        and the score
        """

        return

    def update_template(self, new_example, forget_factor=1):
        """
        Update the tracking template,
        new_example is expected to match the size of
        the example provided to the constructor
        """

        return
