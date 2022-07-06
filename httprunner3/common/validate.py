import jsonpath
from mysql_operate import *


class Validate:

    def __init__(self):
        self.judge, status_code, reg_exp = JsonPath(), StatusCode(), RegExp()
        self.judge.next_handler(status_code)
        status_code.next_handler(reg_exp)

    def validate_(self, actual, expect, response, deal_with):
        """
        :param actual: 实际值
        :param expect: 预期值
        :param response: response
        :param deal_with: deal_with
        :return: output log
        """
        if deal_with.replace_(expect):
            expect = deal_with.replace_(expect)
        elif deal_with.replace_(actual):
            actual = deal_with.replace_(actual)
        self.judge.handler(actual, expect, response)


class Manager:

    def __init__(self):
        self.obj = None

    def handler(self, actual, expect, response):
        pass

    def next_handler(self, obj):
        self.obj = obj


class JsonPath(Manager):

    def handler(self, actual, expect, response):
        if actual.startswith('$'):
            if re.findall(r'\$[a-zA-Z](.*?){', actual):
                actual = re.findall('{(.*?)}', actual)[0]
                actual = str(jsonpath.jsonpath(response.json(), actual)[0])[:-3]
            else:
                actual = jsonpath.jsonpath(response.json(), actual)[0]
            assert_(actual.__str__().lower(), expect.__str__().lower())
        else:
            self.obj.handler(actual, expect, response)


class StatusCode(Manager):

    def handler(self, actual, expect, response):
        if actual.lower().startswith('status code'):
            actual = response.status_code
            assert_(actual.__str__().lower(), expect.__str__().lower())
        else:
            self.obj.handler(actual, expect, response)


class RegExp(Manager):

    def handler(self, actual, expect, response):
        actual = re.findall(actual, response.text)[0]
        assert_(actual.__str__().lower(), expect.__str__().lower())


def assert_(actual, expect):
    """
    响应断言
    :param actual: 实际值
    :param expect: 预期值
    :return: output log
    """
    if expect in actual:
        logging.info(f"响应断言:  预期值: '{expect}' 实际值: '{actual}', 断言成功!")
    else:
        logging.info(f"响应断言:  预期值: '{expect}' 实际值: '{actual}', 断言失败!")
        assert expect.__str__().lower() in actual.__str__().lower()


if __name__ == '__main__':
    Validate()
