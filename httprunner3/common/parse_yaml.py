# -*- coding: utf-8 -*-
import copy
import yaml
from settings import *


class ReadData(object):

    def __init__(self):
        """
        self.folder: 模块文件夹
        self.file_name: yaml文件名
        """
        self.folder = [os.path.join(paths, filename) for paths, files, name in os.walk(TESTCASE_PATH) for filename in
                       files]
        self.file_name = [name for folder in self.folder for path, file, name in os.walk(folder) if name]

    def load_data(self):
        """
        遍历模块文件夹中的yaml测试文件
        :return: list_data
        """
        list_data = []
        num = 0
        for file_path in self.folder:
            file_list = self.file_name[num]
            for file_name in file_list:
                with open(os.path.join(file_path, file_name), 'r', encoding='UTF-8') as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)  # 读取文件内容
                    list_data.append(data)
            num += 1
        return list_data

    def data_separation(self, separation_data):
        """
        遍历测试数据，参数化allure报告
        :param separation_data: load_data
        :return: test_data
        """
        allure_data = [data.get('allure') for data in separation_data if data]
        test_data = [data.get('test') for data in separation_data if data]
        list_data = []
        num = 0
        for allure in allure_data:
            for test in test_data[num]:
                allure['allure_descrption'] = test['name']
                test['allure'] = copy.deepcopy(allure)
                list_data.append(test)
            num += 1
        return list_data

    def return_data(self):
        """
        测试数据调用方法
        :return: test_data
        """
        load_data = self.load_data()
        test_data = self.data_separation(load_data)
        return test_data


if __name__ == '__main__':
    print(ReadData().return_data())
