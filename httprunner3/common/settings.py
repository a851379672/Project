#  -*- coding: utf-8 -*-
import os

#  项目绝对路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#  测试用例路径
TESTCASE_PATH = os.path.join(BASE_PATH, 'test_data')

# 义测试报告路径
REPORT_PATH = os.path.join(BASE_PATH, 'allure-report')

#  测试文件路径
FILE_PATH = os.path.join(BASE_PATH, 'test_file')

#  日志文件路径
LOG_PATH = os.path.join(BASE_PATH, 'log/log.txt')

#  配置文件路径
CONFIG_PATH = os.path.join(BASE_PATH, 'config')

#  json文件路径
TARGET_PATH = os.path.join(BASE_PATH, 'target/config.json')
