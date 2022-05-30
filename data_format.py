#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# &author: 漂移过弯  time: 2022/5/19 6:02 下午


import pandas as pd
import time
import utils
import numpy as np


def cleaned_filename(ori_dire, name):
    file_name1 = ori_dire.split('/')[-1]
    file_name2 = ori_dire.split('\\')[-1]

    dire0 = ori_dire.replace(file_name1, '').replace(file_name2, '')

    # 如果是mac系统
    if ori_dire == file_name2:
        dire = dire0 + name + file_name1
    # 如果是windows系统
    if ori_dire == file_name1:
        dire = dire0 + name + file_name2
    return dire, file_name1, file_name2, dire0


class DataFormat:

    def __init__(self, stu_info_dire, tenant_id):
        self.stu_info_dire = stu_info_dire
        self.tenant_id = tenant_id

    @staticmethod
    def stu_info_format(stu_info_dire):
        stu_info = pd.DataFrame(pd.read_excel(stu_info_dire, sheet_name='学员档案', dtype=str))
        stu_info.rename(
            columns={'姓名': '学员姓名', '证件号': '证件号码', '报名时间': '报名日期', '招生经办人': '招生人', '电子邮箱': '邮箱'}, inplace=True)

        stu_info.loc[:, '原学员编号'] = stu_info.loc[:, '证件号码'] + stu_info.loc[:, '报名日期']
        status_list = utils.status_list()

        stu_info['vc'] = ""
        vc = stu_info['证件号码'].value_counts()
        stu_info['vc'] = stu_info['证件号码'].map(vc)

        stu_info.sort_values(by=['vc'], ascending=[True], inplace=True)

        stu_info.loc[:, '学员状态'] = stu_info.loc[:, '学员状态'].astype('category')
        stu_info.loc[:, '学员状态'].cat.set_categories(status_list, inplace=True)

        stu_info1 = stu_info[stu_info['vc'] == 1].sort_values(by=['报名日期'], ascending=[True])
        stu_info2 = stu_info[stu_info['vc'] != 1].sort_values(by=['学员状态', '报名日期'], ascending=[True, True])

        stu_final = pd.concat([stu_info1, stu_info2], axis=0)
        stu_final.drop(['vc'], axis=1, inplace=True)

        stu_info_tar = utils.student_info()
        columns = stu_final.columns.tolist()

        # 固定处理规则
        dff_1 = list(set(columns).difference(set(stu_info_tar)))
        stu_final.drop(dff_1, axis=1, inplace=True)

        # 取出空缺的列，并添加
        dff_2 = list(set(stu_info_tar).difference(set(columns)))
        stu_final[dff_2] = np.nan

        stu_final = stu_final[stu_info_tar]

        stu_info_dire_new, file_name1, file_name2, dire0 = cleaned_filename(stu_info_dire, '后台导入学员')

        print(stu_info_dire_new, file_name1, file_name2, dire0)

        stu_final.to_excel(stu_info_dire_new, index=False, header=True)

        if stu_final.shape[0] > 0:
            res = '学员档案转换完成'
        else:
            res = '转换未完成，请确认数据'

        print(res)
        return res

    @staticmethod
    def stu_exam_format(stu_exam_dire):
        print(stu_exam_dire)
        return stu_exam_dire

    @staticmethod
    def stu_finance_format(stu_finance_dire, tenant_id):
        stu_finance = pd.DataFrame(pd.read_excel(stu_info_dire, sheet_name='学员财务', dtype=str))
        stu_finance.loc[:, '学员编号'] = stu_finance.loc[:, '证件号码'] + stu_finance.loc[:, '报名日期']
        
        sut_finance_bill = stu_finance.loc[:, (
                           '收支类型',
                           '账单类型',
                           '证件号码',
                           '报名日期',
                           '账单来源',
                           '账单状态',
                           '审核状态',
                           '账单款项',
                           '款项标准',
                           '款项优惠',
                           '支付优惠',
                           '款项实收/付',
                           '款项待收/付',
                           '款项呆账',
                           '账单备注',
                           '创建人',
                           '创建时间')]
        print(stu_finance_dire)
        return stu_finance_dire


if __name__ == '__main__':
    start = time.time()
    DataFormat.stu_info_format('/Users/hechun/Downloads/测试相关文件夹/学员导入_专业模式.xlsx', 999)
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
