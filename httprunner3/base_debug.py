# -*- coding: utf-8 -*-
import requests
import pytest
import jsonpath
from httprunner.client import get_req_resp_record
from common.file_depend import file_encryption


def base_debug(config):
    """
    DEBUG
    """
    cookie = 'JSESSIONID=2706FEC50B918DF592A7713538969179'
    num = 1
    contentId = 362
    res = requests.post(
        url='http://api2.game2.top:88/cdk70/pay.php?sdk=ODUxMzc5NjcyOzE2ODY=',
        json={
            'type': 1,
            'uid': '奶妈'
        },
        headers={
            'Referer': 'http://api2.game2.top:88/cdk70/?sdk=ODUxMzc5NjcyOzE2ODY=',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
    )
    print(res.json())


if __name__ == '__main__':
    pytest.main(['-s', '-q'])
