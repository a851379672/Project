#!/user/bin/env python
# coding=utf-8
"""
pytest用例执行文件
"""

if __name__ == '__main__':
    import pytest
    import os
    pytest.main(['--cache-clear', '--alluredir', 'allure-report/result/case_result'])
    os.system('allure generate allure-report/result --clean allure-report/result/case_result -o allure-report/html')
