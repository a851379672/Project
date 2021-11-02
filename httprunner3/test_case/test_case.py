# -*- coding: utf-8 -*-
import pytest
import requests

from conftest import get_config_token
from common.parse_yaml import ReadData
from common.data_depend import DataDepend
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

    def test_config_token(self, get_config):
        """
        :return: extract_data
        """
        get_config_token(get_config, self.deal_with)

    @pytest.mark.parametrize('api_data', ReadData().join_url(ReadData().return_data()))
    def test_run(self, api_data):
        """
        :param api_data
        :return: report_content
        """

        """数据处理"""
        request_data = eval(self.deal_with.replace_(api_data['request']))
        if request_data['headers'].get('content-type') and 'urlencoded' in request_data['headers']:
            request_data['data'] = urlencode(request_data['data'])
        if request_data.get('files'):
            file_name = request_data['files']['file']
            file_path = os.path.join(FILE_PATH, file_name)
            if len(request_data['files']) == 1:
                request_data['files'] = {'file': open(file_path, 'rb')}
            else:
                file_params = {key: (None, value) for key, value in request_data['files'].items() if key != 'file'}
                file_params.update({'file': (file_name, open(file_path, 'rb'))})
                request_data['files'] = file_params
        allure_(api_data)

        """日志输出"""
        response = requests.session().request(**request_data)
        get_req_resp_record(response)

        """sql执行"""
        sql_statement = api_data.get('sql_statement')
        if sql_statement:
            [MysqlOperate(value[0]).execute_sql(value[1], self.deal_with) for sql in sql_statement
             for value in sql.values()]

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
    pytest.main(['-s', '-v'])
