# -*- coding: utf-8 -*-
import pytest
import requests
import json

from common.parse_yaml import ReadData
from common.data_depend import DataDepend
from common.file_depend import *
from common.validate import Validate
from common.mysql_operate import MysqlOperate
from common.lib_ import *
from settings import *
from urllib.parse import urlencode
from httprunner.client import get_req_resp_record


class TestClass:

    def setup_class(self):
        self.deal_with = DataDepend()
        self.validate = Validate()
        with open(TARGET_PATH, 'r') as file:
            self.file = json.load(file)

    def test_config(self):
        """
        :return: extract_data
        """
        [self.deal_with.extract_(key, value.__str__(), None, self.deal_with) for key, value in self.file.items()]

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    @pytest.mark.parametrize('api_data', ReadData().return_data())
    def test_run(self, api_data):
        """
        :param api_data
        :return: report_content
        """

        """数据处理"""
        request_data = eval(self.deal_with.replace_(api_data['request']))
        request_data['url'] = f"{self.file['ent_url']}{request_data['url']}"
        if request_data.get('files'):
            request_data['files'] = FileDepend().file_dispose(request_data['files'])
        if request_data['headers'].get('content-type') and 'urlencoded' in request_data['headers'].get('content-type'):
            request_data['data'] = urlencode(request_data['data'])
        allure_(api_data, self.file['ent_url'])

        """日志输出"""
        response = requests.session().request(**request_data, timeout=10)
        get_req_resp_record(response)

        """sql执行"""
        sql_statement = api_data.get('sql_statement')
        if sql_statement:
            [MysqlOperate(key, value[0]).execute_sql(value[1], self.deal_with) for sql in sql_statement
             for key, value in sql.items()]

        """参数提取"""
        extract = api_data.get('extract')
        if extract:
            [self.deal_with.extract_(key, value, response, self.deal_with) for key, value in extract.items()]

        """响应断言"""
        validate = api_data.get('validate')
        if validate:
            [self.validate.validate_(value[0], value[1], response, self.deal_with) for validate_dict in validate
             for key, value in validate_dict.items()]


if __name__ == '__main__':
    pytest.main(['-vs'])
