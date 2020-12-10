#-*-coding: UTF-8 -*-
'''
Created on 2020年6月1日

@author: qguan
'''
import os

# 当前项目路径
basepath = os.path.abspath(os.path.dirname(__file__))

# 练习数据目录
data_path = os.path.join(basepath + "\\datas\\")

# 日志存放路径
log_path = os.path.join(basepath + "\\logs\\")

# 配置文件目录
prop_path = os.path.join(basepath + "\\properties\\")

# 生层报告目录
reports_path = os.path.join(basepath + "\\reports\\")

account_excel = os.path.join(data_path + "testcases.xlsx")

jsonData_path = os.path.join(basepath + "/jsonData/")

if __name__ == '__main__':
    pass
