import allure
import base64
import hashlib


def allure_(allure_data):
    """
    :param allure_data:
    :return:
    """
    allure.dynamic.suite(allure_data['allure']['allure_descrption'])
    allure.dynamic.link(allure_data['request']['url'])
    allure.dynamic.sub_suite(allure_data['allure']['allure_sub_suite'])
    allure.dynamic.feature(allure_data['allure']['allure_feature'])
    allure.dynamic.story(allure_data['allure']['allure_story'])
    allure.dynamic.title(allure_data['allure']['allure_descrption'])


def base_64(encrypt_data):
    """
    :param encrypt_data: encrypt_data
    :return: str(base64data, encoding="utf-8")
    """
    try:
        base64data = base64.b64encode(encrypt_data.encode(encoding='utf-8'))
    except AttributeError:
        base64data = str(base64.b64encode(encrypt_data.read()), encoding='utf-8')
    return base64data


def md_5(encrypt_data):
    """
    :param encrypt_data: encrypt_data
    :return:
    """
    try:
        md5data = hashlib.md5(encrypt_data.encode(encoding='utf-8')).hexdigest()
    except AttributeError:
        md5data = str(base64.b64encode(encrypt_data.read()), encoding='utf-8')
    return md5data


if __name__ == '__main__':
    with open(r'D:\PyCharm\project\httprunner3\test_file\考试封面.jpg', 'rb') as f:
        s = md_5(f)
        print(s)
