# -*- coding: utf-8 -*-
import copy
import jsonpath
import re
import logging
import date_time
import lib_
import file_depend


class DataDepend:

    def __init__(self):
        self.dicts = {}
        self.expr1 = r'\$\{(.*?)\}'
        self.expr2 = r'\$[a-z]+[+\-*/_-]+[a-z]+{\$.*?}'
        self.expr3 = r'\$(.*?){(.*?)}'
        self.expr4 = r'\$(.*?){}'
        self.datetime_ = date_time.DateTime

    def extract_(self, key, value, response, deal_with):
        """
        :param key: extract_key
        :param value: extract_value
        :param response: response
        :param deal_with: deal_with
        :return: log info
        """
        replace_data = deal_with.replace_(value)
        if replace_data:
            value = replace_data
        if value.startswith('$.'):
            values = {key: jsonpath.jsonpath(response.json(), value)[0]}.get(key)
            if values:
                self.dicts.update({key: values.__str__()})
                logging.info(f'提取变量：{key}: {values}')
                return values
        else:
            self.dicts.update({key: value.__str__()})
            logging.info(f'提取变量：{key}: {value}')

    def replace_(self, replace_data):
        """
        :param replace_data: replace_data
        :return: eval(build_data)
        """
        replace_copy = copy.copy(replace_data.__str__())
        keys1 = re.findall(self.expr1, replace_copy)
        if keys1:
            replace_copy = self.get_replace(keys1, replace_copy)
        keys2 = re.findall(self.expr2, replace_copy)
        if keys2:
            replace_copy = self.get_replace(keys2, replace_copy)
        keys3 = re.findall(self.expr3, replace_copy)
        if keys3:
            for key in keys3:
                replace_copy = self.get_replace([key[0], key[1]], replace_copy)
        keys4 = re.findall(self.expr4, replace_copy)
        if keys4:
            replace_copy = self.get_replace(keys4, replace_copy)
        if replace_copy is not replace_data:
            return replace_copy

    def get_replace(self, keys, replace_data):
        """
        :param keys: keys
        :param replace_data: replace_data
        :return:
        """
        for key in keys:
            if key.startswith('$'):
                value = self.repeatedly(key)
                replace_data = replace_data.replace(key + '}', value.__str__())
            elif self.in_getattr(key):
                #   自定义方法
                replace_data = self.definition(keys, key, replace_data)
                break
            else:
                #   替换变量
                value = self.dicts.get(key)
                replace_data = replace_data.replace('${' + key + '}', value)
        return replace_data

    def in_getattr(self, func):
        """
        :param func: 函数
        :return: objects
        """
        if func in dir(self.datetime_):
            return self.datetime_
        elif func in dir(lib_):
            return lib_
        elif func in dir(file_depend.FileDepend()):
            return file_depend.FileDepend()
        else:
            return False

    def getattr_(self, objects, func, func_params=None):
        """
        :param objects: 对象
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

    def repeatedly(self, key):
        """
        数据多次处理
        :param key: processing_key
        :return:
        """
        #   获取方法集合、倒序排序
        func_gather = re.findall(r'\$(.*?){', key)[::-1]
        func = func_gather[1]
        if len(func_gather) > 1:
            #   方法抽取、参数处理
            func_replace = re.findall('{(.*?)}', re.findall('{(.*?)}', key)[0] + '}')[0]
            objects = self.in_getattr(func)
            func_params = self.getattr_(objects, func_gather[0], func_replace)
        else:
            func_params = None
        if self.in_getattr(func):
            objects = self.in_getattr(func)
            return self.getattr_(objects, func, func_params.__str__())
        else:
            objects = self.in_getattr(func)
            return self.getattr_(objects, key)

    def definition(self, keys, key, replace_data):
        """
        自定义方法
        :param keys: processing_keys
        :param key: processing_method
        :param replace_data: replace_data
        :return:
        """
        method = keys[-1]
        objects = self.in_getattr(key)
        if file_depend.FileDepend().file_dispose(method) and key in dir(lib_):
            #   图片加密转换
            keys[1] = file_depend.FileDepend().file_dispose(keys[1])
        if len(keys) > 1:
            eval_replace_data = eval(replace_data).get('params') or eval(replace_data).get('data')
            if eval_replace_data and eval_replace_data.get('fileKey') and len(eval_replace_data) == 1:
                #   文件加密上传
                return file_depend.file_encryption(method, replace_data, key)
            else:
                value = self.getattr_(objects, key, keys[1])
                return replace_data.replace('$' + key + '{' + method + '}', value.__str__())
        else:
            value = self.getattr_(objects, key)
            return replace_data.replace('$' + key + '{}', value.__str__())


if __name__ == '__main__':
    data_depend = DataDepend()
    data_depend.dicts['admin_token'] = '123'
    print(data_depend.replace_("{'url': 'api/v1/system/file/simple-upload-auth', 'method': 'POST', 'headers': {'Author"
                               "ization': 'Bearer__${admin_token}', 'uri': 'exam/exam-game'}, 'data': {'picSize': 51200"
                               "0, 'access_token': '${admin_token}', 'file': '$file_content{exam/练习图标.jpg}'}}"))
