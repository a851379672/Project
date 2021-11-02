# -*- coding: utf-8 -*-
import copy
import jsonpath
import re
import logging
import datetime_
import lib_

from settings import *


class DataDepend(object):

    def __init__(self):
        self.dicts = {}
        self.image_file = lambda x: any(x.endswith(extension)
                                        for extension in ['.png ', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG'])
        self.expr1 = r'\$\{(.*?)\}'
        self.expr2 = r'\$[a-z]+[+\-*/_-]+[a-z]+{\$.*?}'
        self.expr3 = r'\$(.*?){}'
        self.expr4 = r'\$(.*?){(.*?)}'
        self.datetime_ = datetime_.DateTime

    def extract_(self, key, value, response, deal_with):
        """
        :param key: extract_key
        :param value: extract_value
        :param response: response数据
        :param deal_with: deal_with
        :return: log info
        """
        replace_data = deal_with.replace_(value)
        if replace_data:
            value = replace_data
        if value.startswith('$.'):
            try:
                values = {key: jsonpath.jsonpath(response.json(), value)[0]}.get(key)
                if values:
                    self.dicts[key] = str(values)
                    logging.info('提取变量：{}: {}'.format(key, values))
            except TypeError as error:
                logging.info(f'请检查响应和jsonpath: {error}')

    def replace_(self, replace_data):
        """
        :param replace_data: replace_data
        :return: eval(build_data)
        """
        replace_copy = copy.copy(str(replace_data))
        keys1 = re.findall(self.expr1, replace_copy)
        if keys1:
            replace_copy = self.get_replace(keys1, replace_copy)
        keys2 = re.findall(self.expr2, replace_copy)
        if keys2:
            replace_copy = self.get_replace(keys2, replace_copy)
        keys3 = re.findall(self.expr3, replace_copy)
        if keys3:
            replace_copy = self.get_replace(keys3, replace_copy)
        keys4 = re.findall(self.expr4, replace_copy)
        if keys4:
            for key in keys4:
                replace_copy = self.get_replace(key, replace_copy)
        if replace_copy is not replace_data:
            return replace_copy

    def get_replace(self, keys, replace_data):
        """
        :param keys: keys
        :param replace_data: replace_data
        :return:
        """
        for key in keys:
            if self.image_file(keys[-1]):
                #   图片加密转换
                replace_data = self.image_depend(keys[1], key, replace_data)
                break
            if key.startswith('$'):
                #   获取方法集合、倒序排序
                func_gather = re.findall(r'\$(.*?){', key)[::-1]
                func = func_gather[1]
                if len(func_gather) > 1:
                    #   方法抽取及参数处理
                    func_replace = re.findall('{(.*?)}', re.findall('{(.*?)}', key)[0] + '}')[0]
                    objects = self.in_getattr_(func)
                    func_params = self.getattr_(objects, func_gather[0], func_replace)
                else:
                    func_params = None
                if self.in_getattr_(func):
                    objects = self.in_getattr_(func)
                    value = self.getattr_(objects, func, func_params)
                else:
                    objects = self.in_getattr_(func)
                    value = self.getattr_(objects, key)
                replace_data = replace_data.replace(replace_data, value.__str__())
            elif self.in_getattr_(key):
                objects = self.in_getattr_(key)
                if len(keys) > 1:
                    value = self.getattr_(objects, key, keys[1])
                    replace_data = replace_data.replace('$' + key + '{' + keys[1] + '}', value.__str__())
                else:
                    value = self.getattr_(objects, key)
                    replace_data = replace_data.replace('$' + key + '{}', value.__str__())
                break
            else:
                value = self.dicts.get(key)
                replace_data = replace_data.replace('${' + key + '}', value)
        return replace_data

    def in_getattr_(self, func):
        """
        :param func: 函数
        :return: objects
        """
        if func in dir(self.datetime_):
            return self.datetime_
        elif func in dir(lib_):
            return lib_
        else:
            return False

    def getattr_(self, objects, func, func_params=None):
        """
        :param objects
        :param func: 函数
        :param func_params: 参数
        :return:
        """
        if func_params:
            try:
                value = getattr(objects, func)(func_params)
            except TypeError:
                value = getattr(objects, func)(objects(), func_params)
        else:
            value = getattr(objects, func)(self)
        return value

    def image_depend(self, keys, key, replace_data):
        file_path = os.path.join(FILE_PATH, keys)
        objects = self.in_getattr_(key)
        value = self.getattr_(objects, key, open(file_path, 'rb'))
        return replace_data.replace(r'$' + key + '{' + keys[1] + '}', value.__str__())


if __name__ == '__main__':
    datadepend_ = DataDepend()
    datadepend_.image_depend('考试封面.jpg', 'base_64', "{'url': '/api/v1/system/file/cropper-upload', 'method': 'POST', 'headers': {'Authorization': 'Bearer__cb4fbe83f03b19163f0b8d39fe347e2f', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'uri': 'exam/exam'}, 'data': {'image': 'data:image/png;base64,$base_64{考试封面.jpg}'}}")
    datadepend_.dicts['access_token'] = '123'
    print(datadepend_.replace_("{'name': '【普通考试】-人脸识别规则', 'request': {'method': 'GET', 'headers': {'Authorizati"
                               "on': 'Bearer__${access_token}', 'uri': None}, 'params': {'key': '$diy_time{2021, 09, +0"
                               "2, +03, -40, 30}', 'value': '$diy_time{2021, 09, +02, +03, -40, 30}'}}, 'sql_statement'"
                               ": None, 'extract': None, 'validate': [{'eq': ['$.status', '1']}]}"))
