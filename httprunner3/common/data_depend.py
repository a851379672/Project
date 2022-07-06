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

    def extract_(self, key, value, response):
        """
        :param key: extract_key
        :param value: extract_value
        :param response: response
        :return: output log
        """
        replace_data = self.replace_(value)
        if replace_data:
            value = replace_data
        values = {key: jsonpath.jsonpath(response.json(), value)[0]}.get(key) if value.startswith('$.') else ''
        self.dicts.update({key: values.__str__()}) if values else self.dicts.update({key: value.__str__()})
        logging.info(f'提取变量：{key}: {value}')

    def replace_(self, replace_data):
        """
        :param replace_data: replace_data
        :return: eval(build_data)
        """
        replace_copy = copy.copy(replace_data.__str__())
        keys1 = set(re.findall(self.expr1, replace_copy))
        if keys1:
            replace_copy = self.get_replace(keys1, replace_copy)
        keys2 = set(re.findall(self.expr2, replace_copy))
        if keys2:
            replace_copy = self.get_replace(keys2, replace_copy)
        keys3 = set(re.findall(self.expr3, replace_copy))
        if keys3:
            for key in keys3:
                replace_copy = self.get_replace([key[0], key[1]], replace_copy)
        keys4 = set(re.findall(self.expr4, replace_copy))
        if keys4:
            replace_copy = self.get_replace(keys4, replace_copy)
        if replace_copy is not replace_data:
            return replace_copy

    def get_replace(self, keys, replace_data):
        """
        :param keys: keys
        :param replace_data: replace_data
        :return: replace_data
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

    @staticmethod
    def in_getattr(func):
        """
        :param func: 函数
        :return: objects
        """
        if func in dir(date_time.DateTime):
            return date_time.DateTime
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
        :return: value
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
        return self.getattr_(self.in_getattr(func), func, func_params.__str__()) \
            if self.in_getattr(func) else self.getattr_(self.in_getattr(func), key)

    def definition(self, keys, key, replace_data):
        """
        自定义方法
        :param keys: processing_keys
        :param key: processing_method
        :param replace_data: replace_data
        :return: replace_data
        """
        method = keys[-1]
        objects = self.in_getattr(key)
        if file_depend.FileDepend().file_dispose(method) and key in dir(lib_):
            #   图片加密转换
            keys[1] = file_depend.FileDepend().file_dispose(keys[1])
        if len(keys) > 1:
            eval_replace_data = eval(replace_data).get('params') or eval(replace_data).get('data')
            #   文件加密上传
            return file_depend.file_encryption(method, replace_data, key) \
                if eval_replace_data and eval_replace_data.get('fileKey') and len(eval_replace_data) == 1 \
                else replace_data.replace('$' + key + '{' + method + '}',
                                          self.getattr_(objects, key, keys[1]).__str__())
        else:
            value = self.getattr_(objects, key)
            return replace_data.replace('$' + key + '{}', value.__str__())


if __name__ == '__main__':
    import pprint
    data_depend = DataDepend()
    data_depend.dicts.update({'admin_token': '123', 'data_id': 'abc'})
    pprint.pprint(data_depend.replace_("{'url': 'api/v1/system/file/simple-upload-auth/${admin_token}',"
                                       " 'method': 'POST/${data_id}',"
                                       " 'headers': {'Authorization': 'Bearer__${admin_token}',"
                                       " 'uri': 'exam/exam-game/${data_id}'},"
                                       " 'data': {'picSize': '${admin_token}', 'access_token': '${data_id}', 'file':"
                                       " '$file_content{exam/练习图标.jpg}'}}"))
