#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# &author: 漂移过弯  time:2022/1/7 2:20 下午

import os
import time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter import ttk
from data_format import DataFormat


# from scrapy_list import scrapy_total
# from cleans_list import clean_total


class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        self.askdirectory = tk.StringVar()
        self.tenant_id = tk.StringVar()
        root.geometry('650x345')
        root.minsize(345, 250)
        root.maxsize(1024, 768)
        root.title('斯堪尼亚数据助手')
        # root.iconbitmap()

        self.intwind()

    def buttonactive(self):
        stu_info_dire = self.askdirectory.get()
        tenant_id = self.tenantIds.get()

        # if len(dire) == 0:
        #     messagebox.showinfo('提示:', '没有选择文件')
        #     return

        df = DataFormat(stu_info_dire, tenant_id)
        df.stu_info_format(stu_info_dire)
        df.stu_exam_format(stu_exam_dire, tenant_id)
        df.stu_finance_format(stu_finance_dire, tenant_id)

        messagebox.showinfo('提示:', '数据转换完成')

    def delete(self):
        self.saascookieid.delete(0, 'end')
        self.tenantIds.delete(0, 'end')
        self.askdirectory.delete(0, 'end')

    @staticmethod
    def select_stu_info_path(self):
        stu_info_path_ = askdirectory()
        askdirectory.set(stu_info_path_)
        return stu_info_path_

    @staticmethod
    def tenant_id(self):
        tenant_id = self.tenant_id()
        self.tenant_id.set(tenant_id)
        return tenant_id

    def intwind(self):
        frame1 = Frame(self)
        Label(frame1, text='请输入文件路径:', fg='red').grid(row=2, column=0)
        Entry(frame1, textvariable='').grid(row=2, column=1)
        Button(frame1, text='文件路径', command=self.select_stu_info_path).grid(row=2, column=2)

        frame2 = Frame(self)
        Label(frame2, text='   请输入驾校ID:', fg='red').grid(row=3, column=0, sticky=E)
        Entry(frame2, textvariable=self.tenant_id).grid(row=3, column=1)

        frame1.grid(pady=3, sticky=W)
        frame2.grid(pady=3, sticky=W)

        Button(self, text='开始转换', width=5, command=self.buttonactive).grid()
        Button(self, text='退出', width=5, command=self.quit).grid()

    # def create_page(self):
    #     # self.about_frame = Frame(self)
    #
    #     # frame1 = Frame(self)
    #     # Label(frame1, Text='关于作品：本工具只限制公司测试使用').pack()
    #
    #     menubar = Menu(self)
    #     menubar.add_command(label='设置')
    #     # menubar.add_command(label='关于', command=self.show_about())
    #     # self.root['menu'] = menubar
    #
    # # def show_about(self):
    # #     self.frame1.pack()


if __name__ == '__main__':
    root = tk.Tk()
    application = Application(root=root)
    application.mainloop()
