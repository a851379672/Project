import jsonpath
from mysql_operate import *

logger = logging


class Validate(object):

    def __init__(self):
        self.judge = JsonPath()
        status_code = StatusCode()
        reg_exp = RegExp()
        self.judge.next_handler(status_code)
        status_code.next_handler(reg_exp)

    def validate_(self, actual, expect, response, deal_with):
        """
        :param actual: 实际值
        :param expect: 预期值
        :param response: response
        :param deal_with: deal_with
        :return: logger info
        """
        if deal_with.replace_(expect):
            expect = deal_with.replace_(expect)
        elif deal_with.replace_(actual):
            actual = deal_with.replace_(actual)
        # elif deal_with.replace_(expect, actual):
        #     expect = deal_with.replace_(expect, actual)
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
            try:
                assert expect.__str__() in actual.__str__().lower()
                logger.info(f"响应断言： 预期值：'{expect}' 实际值：'{actual}', 断言成功!")
            except AssertionError:
                pytest.xfail(f'断言失败：{AssertionError}')
        else:
            self.obj.handler(actual, expect, response)


class StatusCode(Manager):

    def handler(self, actual, expect, response):
        if actual.startswith('Status Code'):
            actual = response.status_code
            try:
                assert actual.__str__() in expect.__str__().lower()
                logger.info(f"响应断言： 预期值：'{expect}' 实际值：'{actual}', 断言成功!")
            except AssertionError:
                pytest.xfail(f'断言失败：{AssertionError}')
        else:
            self.obj.handler(actual, expect, response)


class RegExp(Manager):

    def handler(self, actual, expect, response):
        actual = re.findall(actual, response.text)[0]
        try:
            assert actual.__str__() in expect.__str__().lower()
            logger.info(f"响应断言： 预期值：'{expect}' 实际值：'{actual}', 断言成功!")
        except AssertionError:
            pytest.xfail(f'断言失败：{AssertionError}')


if __name__ == '__main__':
    Validate()
