# -*- coding: utf-8 -*-
import requests
import logging
import json

from settings import *
from httprunner.client import get_req_resp_record


def get_admin_token(config: dict):
    """
    :return: admin_token
    """
    res = requests.post(
        url=config['login_url'],
        data={
            'key': config['admin_login_key'],
            'organization_id': config['organization_id'],
            'login_method': config['login_method'],
            'username': config['admin_username'],
            'pword': config['admin_password']
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    get_req_resp_record(res)
    admin_token = res.json().get('access_token')
    if admin_token:
        logging.info('企业管理员登录成功')
        config.update({'admin_token': admin_token})
        with open(TARGET_PATH, 'w') as f:
            f.write(json.dumps(config))
        return res
    else:
        logging.info('企业管理员登录失败')


def get_student_token(config: dict):
    """
    :return: student_token
    """
    res = requests.post(
        url=config['login_url'],
        data={
            'key': config['student_login_key'],
            'organization_id': config['organization_id'],
            'login_method': config['login_method'],
            'username': config['student_username'],
            'pword': config['student_password']
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    get_req_resp_record(res)
    student_token = res.json().get('access_token')
    if student_token:
        logging.info('企业学员登录成功')
        config.update({'student_token': student_token})
        with open(TARGET_PATH, 'w') as f:
            f.write(json.dumps(config))
        return res
    else:
        logging.info('企业学员登录失败')
