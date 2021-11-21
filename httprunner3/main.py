#!/user/bin/env python
# coding=utf-8
import pytest
import os
"""
pytest用例执行文件
"""

if __name__ == '__main__':
    pytest.main(['--cache-clear', '--alluredir', 'allure-report/result/case_result'])
    os.system('allure generate allure-report/result --clean allure-report/result/case_result -o allure-report/html')
