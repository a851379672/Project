import base64
import hashlib
import allure
from settings import *


def allure_(allure_data, ent_url):
    """
    allure数据参数化
    :param allure_data: allure_data
    :param ent_url: ent_url
    """
    allure.dynamic.suite(allure_data['allure']['allure_descrption'])
    allure.dynamic.link(f"{ent_url}{allure_data['request']['url']}")
    allure.dynamic.sub_suite(allure_data['allure']['allure_sub_suite'])
    allure.dynamic.feature(allure_data['allure']['allure_feature'])
    allure.dynamic.story(allure_data['allure']['allure_story'])
    allure.dynamic.title(allure_data['allure']['allure_descrption'])


def base_64(encrypt_data):
    """
    :param encrypt_data: encrypt_data
    :return: base64(data)
    """
    try:
        base64data = base64.b64encode(encrypt_data.encode(encoding='utf-8'))
    except AttributeError:
        base64data = str(base64.b64encode(encrypt_data.read()), encoding='utf-8')
    return base64data


def md_5(encrypt_data):
    """
    :param encrypt_data: encrypt_data
    :return: md5(data)
    """
    try:
        md5data = hashlib.md5(encrypt_data.encode(encoding='utf-8')).hexdigest()
    except AttributeError:
        md5data = str(base64.b64encode(encrypt_data.read()), encoding='utf-8')
    return md5data


if __name__ == '__main__':
    with open(rf'{BASE_PATH}\test_file\exam\考试封面_1195.jpg', 'rb') as f:
        md5_file = md_5(f)
        print(md5_file)
    with open(rf'{BASE_PATH}\test_file\exam\考试封面_1195.jpg', 'rb') as f:
        base_64_file = base_64(f)
        print(base_64_file)
