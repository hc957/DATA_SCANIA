#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# &author: 漂移过弯  time: 2022/5/19 6:02 下午


import pandas as pd
import time
import utils


class DataFormat:

    def __init__(self, stu_info_dire, stu_exam_dire, stu_finance_dire):
        self.stu_info_dire = stu_info_dire
        self.stu_finance_dire = stu_finance_dire
        self.stu_exam_dire = stu_exam_dire

    @staticmethod
    def stu_info_format(stu_info_dire):
        # execfile_xls = '' % stu_info_dire
        # execfile = '%s.xls' % stu_info_dire
        stu_info = pd.DataFrame(pd.read_excel(stu_info_dire, sheet_name='专业模式', dtype=str))
        stu_info.rename(
            columns={'证件号': '证件号码', '报名时间': '报名日期', '招生经办人': '招生人'},
            inplace=True)

        stu_info.loc[:, '原学员编号'] = stu_info.loc[:, '证件号码'] + stu_info.loc[:, '报名日期']
        status_list = utils.status_list()

        stu_info['vc'] = ""
        vc = stu_info['证件号码'].value_counts()
        stu_info['vc'] = stu_info['证件号码'].map(vc)

        stu_info.sort_values(by=['vc'], ascending=[True], inplace=True)

        stu_info.loc[:, '学员状态'] = stu_info.loc[:, '学员状态'].astype('category')
        stu_info.loc[:, '学员状态'].cat.set_categories(status_list, inplace=True)

        # data_f.loc[:, 'sort_time'] = data_f.loc[:, '报名日期'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

        stu_info1 = stu_info[stu_info['vc'] == 1].sort_values(by=['报名日期'], ascending=[True])
        stu_info2 = stu_info[stu_info['vc'] != 1].sort_values(by=['学员状态', '报名日期'], ascending=[True, True])

        stu_final = pd.concat([stu_info1, stu_info2], axis=0)
        stu_final.drop(['vc'], axis=1, inplace=True)
        stu_final = stu_final[dit_tar]

        print(stu_info)

        return stu_info_dire

    @staticmethod
    def stu_exam_format(stu_exam_dire):
        print(stu_exam_dire)
        return stu_exam_dire

    @staticmethod
    def stu_finance_format(stu_finance_dire):
        print(stu_finance_dire)
        return stu_finance_dire


if __name__ == '__main__':
    start = time.time()
    DataFormat.stu_info_format('/Users/hechun/Downloads/测试相关文件夹/学员导入_专业模式.xlsx')
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
