#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# &author: 漂移过弯  time: 2022/5/19 6:02 下午

import stu_info
import stu_finance


class DataFormat:

    def __init__(self, stu_directory, stu_finance_directory, stu_exam_directory):
        self.stu_directory = stu_directory
        self.stu_finance_directory = stu_finance_directory
        self.stu_exam_directory = stu_exam_directory

    @staticmethod
    def stu_format(stu_directory):
        print(stu_directory)
        return stu_directory
