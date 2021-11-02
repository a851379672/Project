# -*- coding: utf-8 -*-
import json
import pytest
import requests
import logging
import yaml

from httprunner.client import get_req_resp_record
from settings import *


def pytest_addoption(parser):
    """
    添加命令行参数
    """
    parser.addoption(
        "--config", action="store", default="pre_config.yaml", help="配置文件"
    )


@pytest.fixture(scope="session", autouse=True)
def get_config(request):
    config = request.config.getoption("config")
    config_path = os.path.join(CONFIG_PATH, f'{config}')
    with open(config_path, "r", encoding="utf-8") as f:
        config_json = yaml.safe_load(f)
    if config_json:
        with open(TARGET_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(config_json))
    return get_access_token(config_json), get_enterprise_config(config_json)


def get_access_token(config: dict):
    """
    :return: access_token
    """
    res = requests.post(
        url=config['login_url'],
        data={
            'key': config['login_key'],
            'organization_id': config['organization_id'],
            'login_method': config['login_method'],
            'username': config['username'],
            'pword': config['password']
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
    get_req_resp_record(res)
    access_token = res.json().get('access_token')
    if access_token:
        logging.info('企业管理员登录成功')
        config.update({'access_token': access_token})
        with open(TARGET_PATH, 'w') as f:
            f.write(json.dumps(config))
        return res
    else:
        logging.info('企业管理员登录失败')


def get_enterprise_config(config: dict):
    """
    :return: enterprise_config
    """
    res = requests.get(
        url=config['config_url'],
        headers={
            'Authorization': f'Bearer__{config["access_token"]}'
        })
    get_req_resp_record(res)
    if res.json()['redirectUri'] in config['ent_url']:
        logging.info('获取企业配置信息成功')
        return res
    else:
        logging.info('获取企业配置信息失败')


def get_config_token(*args):
    """
    :param args: args
    :return:
    """
    access_token = args[0][0]
    enterprise_config = args[0][1]
    deal_with = args[1]
    deal_with.extract_('access_token', '$.access_token', access_token, deal_with)
    enterprise_json = [
        {'organizationId': '$.currentUser.organization.id'},
        {'organizationName': '$.currentUser.organization.name'},
        {'organizationPath': '$.currentUser.organization.path'},
        {'ent_url': '$.redirectUri'},
        {'ent_name': '$.websiteTitle'}
    ]
    [deal_with.extract_(key, value, enterprise_config, deal_with) for ent in enterprise_json
     for key, value in ent.items()]


if __name__ == '__main__':
    pytest.main(['-s', '-q'])
