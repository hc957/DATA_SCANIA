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
from data_format import *


# from scrapy_list import scrapy_total
# from cleans_list import clean_total


class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.master = root
        self.pack()
        self.askdirectory = tk.StringVar()
        self.askdirectory2 = tk.StringVar()
        root.geometry('650x345')
        root.minsize(345, 250)
        root.maxsize(1024, 768)
        root.title('斯堪尼亚数据助手')
        # root.iconbitmap()

        self.intWind()

    def buttonActive(self):
        dire = self.askdirectory.get()

        if len(dire) == 0:
            messagebox.showinfo('提示:', '没有选择文件')
            return

        df = DataFormat()
        df.stu_format()

        messagebox.showinfo('提示:', '数据转换完成')

    def delete(self):
        self.saascookieid.delete(0, 'end')
        self.tenantIds.delete(0, 'end')
        self.askdirectory.delete(0, 'end')

    def selectpath(self):
        path_ = askdirectory()
        askdirectory.set(path_)
        return path_

    def select_settings_path(self):
        path2_ = askdirectory2()
        askdirectory2.set(path2_)
        return path2_

    def intWind(self):
        frame3 = Frame(self)
        Label(frame3, text='请输入学员档案路径:').grid(row=2, column=0)
        Entry(frame3, textvariable=self.askdirectory).grid(row=2, column=1)
        Button(frame3, text='学员档案路径', command=self.selectstuinfopath).grid(row=2, column=2)

        frame5 = Frame(self)
        Label(frame5, text='请输入交管考试记录路径:').grid(row=3, column=0)
        Entry(frame5, textvariable=self.askdirectory).grid(row=3, column=1)
        Button(frame5, text='交管考试记录路径', command=self.selectstuexampath).grid(row=3, column=2)

        frame4 = Frame(self)
        Label(frame4, text='请输入学员财务路径:').grid(row=4, column=0)
        Entry(frame4, textvariable=self.askdirectory2).grid(row=4, column=1)
        Button(frame4, text='学员财务路径', command=self.selectstufinancepath).grid(row=4, column=2)

        frame3.grid(pady=3)
        frame4.grid(pady=3)
        frame5.grid(pady=3)

        Button(self, text='开始转换', width=5, command=self.buttonActive).grid()
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
