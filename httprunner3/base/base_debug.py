# -*- coding: utf-8 -*-
import requests
import pytest
import jsonpath
from httprunner.client import get_req_resp_record


def base_debug(config):
    """
    DEBUG
    """
    access_token = jsonpath.jsonpath(config.json(), '$.access_token')[0]
    res = requests.post(
        url='https://zxy9.zhixueyun.com/api/v1/exam/manual/fix-exam-task-status',
        data={
            'examId': '699c7722-917a-46d3-bcd9-7162b80ce527',
            'memberIds': 'ec9be59e-34d1-4dcd-9a90-299b263f91e0,6afbd95c-ce44-4b88-9704-e8ed8eb1eeef'
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'authorization': f'Bearer__{access_token}'
        })
    get_req_resp_record(res)
    print('123')


if __name__ == '__main__':
    pytest.main(['-s', '-q'])
