#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# &author: 漂移过弯  time: 2022/5/19 6:02 下午

import base64
import pandas as pd
import time
import utils
import numpy as np

pd.set_option('display.max_columns', 100000)
pd.set_option('display.width', 100000)
pd.set_option('display.max_colwidth', 100000)


# 账单状态判定
# w.款项标准, u.款项优惠, x.支付优惠, y.款项实收 / 付, z.款项呆账
def bill_status(w, u, x, y, z):
    if w - u - x == y:
        return '已完成'
    if w - u - x > y and z == 0:
        return '待处理'
    if w - u - x > y and z != 0:
        return '已关闭'


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

    def __init__(self, stu_info_dire):
        self.stu_info_dire = stu_info_dire
        # self.tenant_id = tenant_id

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

        # print(stu_info_dire_new, file_name1, file_name2, dire0)

        stu_final.to_excel(stu_info_dire_new, index=False, header=True)

        if stu_final.shape[0] > 0:
            res = '学员档案转换完成'
        else:
            res = '转换未完成，请确认数据'

        print(res)
        return res

    # @staticmethod
    # def stu_exam_format(stu_info_dire):
    #     print(stu_info_dire)
    #     return stu_info_dire

    @staticmethod
    def stu_finance_format_multi_bill(stu_info_dire, tenant_id):
        stu_finance = pd.DataFrame(pd.read_excel(stu_info_dire, sheet_name='学员财务_多账单', dtype=str))

        if stu_finance.shape[0] > 0:

            stu_finance.loc[:, ('款项标准', '支付优惠', '款项实收/付')] = \
                stu_finance.loc[:, ('款项标准', '支付优惠', '款项实收/付')].astype(float)
            stu_finance.loc[:, '学员编号'] = stu_finance.loc[:, '证件号码'] + stu_finance.loc[:, '报名日期']

            stu_finance_bill = stu_finance.loc[:,
                               ('收支类型', '账单类型', '证件号码', '报名日期', '账单款项', '款项标准',
                                '支付优惠', '款项实收/付', '账单备注', '创建人', '创建时间', '支付方式', '支付日期', '经办人',
                                '缴费点', '备注', '对账状态', '对账人', '对账时间', '手写票号')]

            stu_finance_bill = stu_finance_bill[
                (stu_finance_bill['证件号码'].notna()) & (stu_finance_bill['报名日期'].notna()) & (
                    stu_finance_bill['支付日期'].notna())]

            stu_finance_bill.rename(
                columns={'款项实收/付': '款项实收', '款项待收/付': '款项待收'}, inplace=True)

            stu_finance_bill.loc[:, '学员编号'] = stu_finance_bill.loc[:, '证件号码'] + stu_finance_bill.loc[:, '报名日期'].str[
                                                                                0: 10]

            stu_finance_bill.loc[:, '款项呆账'] = 0
            stu_finance_bill.loc[:, '款项优惠'] = 0
            stu_finance_bill.loc[:, '账单来源'] = '批量新增'
            stu_finance_bill.loc[:, '审核状态'] = '审核通过'
            stu_finance_bill.loc[:, '序号'] = range(1, len(stu_finance_bill) + 1)

            stu_finance_bill.loc[:, '账单单据编号'] = str(tenant_id) + '_' + stu_finance_bill.loc[:,
                                                                       '证件号码'] + '_' + stu_finance_bill.loc[:,
                                                                                       '支付日期'].str[0:10] + '_' + \
                                                stu_finance_bill.loc[:, '账单款项'].apply(
                                                    lambda x: base64.b64encode(x.encode('utf-8'))).astype(str)

            stu_finance_bill.loc[:, '款项待收'] = stu_finance_bill.loc[:, '款项标准'].astype(float) - \
                                              stu_finance_bill.loc[:, '支付优惠'].astype(float) - \
                                              stu_finance_bill.loc[:, '款项实收'].astype(float) - stu_finance_bill.loc[:,
                                                                                              '款项优惠'].astype(float)

            stu_finance_bill.loc[:, '账单状态'] = stu_finance_bill.apply(
                lambda x: bill_status(x.款项标准, x.款项优惠, x.支付优惠, x.款项实收, x.款项呆账), axis=1)

            # 生成财务流水
            stu_finance_flow = stu_finance_bill.loc[:,
                               ('账单单据编号', '支付方式', '账单款项', '支付优惠', '款项实收', '支付日期', '经办人',
                                '缴费点', '备注', '对账状态', '对账人', '对账时间', '手写票号')]

            stu_finance_bill.rename(
                columns={'款项实收': '款项实收/付', '款项待收': '款项待收/付', '账单单据编号': '单据编号'}, inplace=True)

            stu_bill_tar = utils.student_income_bill()
            columns = stu_finance_bill.columns.tolist()

            # 固定处理规则
            dff_1 = list(set(columns).difference(set(stu_bill_tar)))
            stu_finance_bill.drop(dff_1, axis=1, inplace=True)

            # 取出空缺的列，并添加
            dff_2 = list(set(stu_bill_tar).difference(set(columns)))
            stu_finance_bill[dff_2] = np.nan

            stu_finance_bill = stu_finance_bill[stu_bill_tar]

            stu_info_dire_new, file_name1, file_name2, dire0 = cleaned_filename(stu_info_dire, '后台导入财务多账单')

            stu_finance_bill.to_excel(stu_info_dire_new, index=False, header=True)

            if stu_finance_bill.shape[0] > 0:
                res = '财务账单转换完成'
            else:
                res = '财务账单转换未完成，请确认数据'

            # 处理流水
            stu_finance_flow.loc[:, '单据编号'] = stu_finance_flow.loc[:, '账单单据编号']

            stu_finance_flow.rename(
                columns={'账单单据编号': '账单编号', '款项实收': '实际金额', '账单款项': '款项'}, inplace=True)

            stu_finance_flow.loc[:, '序号'] = range(1, len(stu_finance_flow) + 1)

            stu_flow_tar = utils.student_income_flow()
            columns1 = stu_finance_flow.columns.tolist()

            # 固定处理规则
            dff_3 = list(set(columns1).difference(set(stu_flow_tar)))
            stu_finance_flow.drop(dff_3, axis=1, inplace=True)

            # 取出空缺的列，并添加
            dff_4 = list(set(stu_flow_tar).difference(set(columns1)))
            stu_finance_flow[dff_4] = np.nan

            stu_finance_flow = stu_finance_flow[stu_flow_tar]

            stu_info_dire_new1, file_flow_name1, file_flow_name2, dire0 = cleaned_filename(stu_info_dire, '后台导入财务多流水')

            stu_finance_flow.to_excel(stu_info_dire_new1, index=False, header=True)

            if stu_finance_flow.shape[0] > 0:
                res1 = '财务流水转换完成'
            else:
                res1 = '财务流水转换未完成，请确认数据'

            # print(res, res1)
            return res, res1

        else:
            pass

    @staticmethod
    def stu_finance_format_single_bill(stu_info_dire, tenant_id):
        stu_finance = pd.DataFrame(pd.read_excel(stu_info_dire, sheet_name='学员财务_单账单', dtype=str))

        if stu_finance.shape[0] > 0:

            stu_finance.loc[:, ('款项标准', '支付优惠', '款项实收/付')] = \
                stu_finance.loc[:, ('款项标准', '支付优惠', '款项实收/付')].astype(float)
            stu_finance.loc[:, '学员编号'] = stu_finance.loc[:, '证件号码'] + stu_finance.loc[:, '报名日期']

            stu_finance_bill2 = stu_finance.loc[:,
                               ('收支类型', '账单类型', '证件号码', '报名日期', '账单款项', '款项标准',
                                '支付优惠', '款项实收/付', '账单备注', '创建人', '创建时间', '支付方式', '支付日期', '经办人',
                                '缴费点', '备注', '对账状态', '对账人', '对账时间', '手写票号')]

            stu_finance_bill2 = stu_finance_bill2[
                (stu_finance_bill2['证件号码'].notna()) & (stu_finance_bill2['报名日期'].notna()) & (
                    stu_finance_bill2['支付日期'].notna())]

            stu_finance_bill2.rename(
                columns={'款项实收/付': '款项实收', '款项待收/付': '款项待收'}, inplace=True)

            stu_finance_bill2.loc[:, '学员编号'] = stu_finance_bill2.loc[:, '证件号码'] + stu_finance_bill2.loc[:, '报名日期'].str[
                                                                                0: 10]

            stu_finance_bill2.loc[:, '款项呆账'] = 0
            stu_finance_bill2.loc[:, '款项优惠'] = 0
            stu_finance_bill2.loc[:, '账单来源'] = '批量新增'
            stu_finance_bill2.loc[:, '审核状态'] = '审核通过'


            stu_finance_bill2.loc[:, '流水单据编号'] = str(tenant_id) + '_' + stu_finance_bill2.loc[:, '证件号码'] \
                                                + '_' + stu_finance_bill2.loc[:, '支付日期'].str[0:10] + '_' + \
                                                stu_finance_bill2.loc[:, '账单款项'].apply(
                                                    lambda x: base64.b64encode(x.encode('utf-8'))).astype(str)

            stu_finance_bill2.loc[:, '账单单据编号'] = str(tenant_id) + '_' + stu_finance_bill2.loc[:, '证件号码'] \
                                                + '_' + stu_finance_bill2.loc[:, '账单款项'].apply(
                                                    lambda x: base64.b64encode(x.encode('utf-8'))).astype(str)

            stu_finance_bill = stu_finance_bill2.groupby(['账单单据编号'], as_index=False).agg(
                {'款项标准': 'max', '支付优惠': 'sum', '款项实收': 'sum', '账单备注': 'min', '款项呆账': 'max', '款项优惠': 'min', '账单来源': 'min',
                 '审核状态': 'min', '收支类型': 'min'})

            stu_finance_bill.loc[:, '款项待收'] = stu_finance_bill.loc[:, '款项标准'].astype(float) - \
                                              stu_finance_bill.loc[:, '支付优惠'].astype(float) - \
                                              stu_finance_bill.loc[:, '款项实收'].astype(float) - stu_finance_bill.loc[:,
                                                                                              '款项优惠'].astype(float)


            stu_finance_bill.loc[:, '序号'] = range(1, len(stu_finance_bill) + 1)

            stu_finance_bill.loc[:, '账单状态'] = stu_finance_bill.apply(
                lambda x: bill_status(x.款项标准, x.款项优惠, x.支付优惠, x.款项实收, x.款项呆账), axis=1)

            stu_finance_bill.loc[:, '款项待收'] = stu_finance_bill.loc[:, '款项标准'].astype(float) - \
                                              stu_finance_bill.loc[:, '支付优惠'].astype(float) - \
                                              stu_finance_bill.loc[:, '款项实收'].astype(float) - stu_finance_bill.loc[:,
                                                                                              '款项优惠'].astype(float)

            # 生成财务流水
            stu_finance_flow = stu_finance_bill2.loc[:,
                               ('流水单据编号', '账单单据编号', '支付方式', '账单款项', '支付优惠', '款项实收', '支付日期', '经办人',
                                '缴费点', '备注', '对账状态', '对账人', '对账时间', '手写票号')]
            # 账单重命名
            stu_finance_bill.rename(
                columns={'款项实收': '款项实收/付', '款项待收': '款项待收/付', '账单单据编号': '单据编号'}, inplace=True)

            stu_bill_tar = utils.student_income_bill()
            columns = stu_finance_bill.columns.tolist()

            # 固定处理规则
            dff_1 = list(set(columns).difference(set(stu_bill_tar)))
            stu_finance_bill.drop(dff_1, axis=1, inplace=True)

            # 取出空缺的列，并添加
            dff_2 = list(set(stu_bill_tar).difference(set(columns)))
            stu_finance_bill[dff_2] = np.nan

            stu_finance_bill = stu_finance_bill[stu_bill_tar]

            stu_info_dire_new, file_name1, file_name2, dire0 = cleaned_filename(stu_info_dire, '后台导入财务单账单')

            stu_finance_bill.to_excel(stu_info_dire_new, index=False, header=True)

            if stu_finance_bill.shape[0] > 0:
                res = '财务账单转换完成'
            else:
                res = '财务账单转换未完成，请确认数据'

            # 处理流水
            stu_finance_flow.loc[:, '单据编号'] = stu_finance_flow.loc[:, '流水单据编号']

            stu_finance_flow.rename(
                columns={'账单单据编号': '账单编号', '款项实收': '实际金额', '账单款项': '款项'}, inplace=True)

            stu_finance_flow.loc[:, '序号'] = range(1, len(stu_finance_flow) + 1)

            stu_flow_tar = utils.student_income_flow()
            columns1 = stu_finance_flow.columns.tolist()

            # 固定处理规则
            dff_3 = list(set(columns1).difference(set(stu_flow_tar)))
            stu_finance_flow.drop(dff_3, axis=1, inplace=True)

            # 取出空缺的列，并添加
            dff_4 = list(set(stu_flow_tar).difference(set(columns1)))
            stu_finance_flow[dff_4] = np.nan

            stu_finance_flow = stu_finance_flow[stu_flow_tar]

            stu_info_dire_new1, file_flow_name1, file_flow_name2, dire0 = cleaned_filename(stu_info_dire, '后台导入财务单流水')

            stu_finance_flow.to_excel(stu_info_dire_new1, index=False, header=True)

            if stu_finance_flow.shape[0] > 0:
                res1 = '财务单流水转换完成'
            else:
                res1 = '财务流水转换未完成，请确认数据'

            print(res, res1)
            return res, res1

        else:
            pass


if __name__ == '__main__':
    start = time.time()
    DataFormat.stu_finance_format_single_bill('/Users/hechun/Downloads/测试相关文件夹/数据导入模板.xlsx', '999')
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
