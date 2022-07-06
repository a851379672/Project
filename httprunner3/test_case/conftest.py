# -*- coding: utf-8 -*-
import json
import pytest
import yaml
import logging
from common.settings import *
from base import base_token
from base import base_file


def pytest_addoption(parser):
    """
    添加命令行参数
    """
    parser.addoption(
        "--config", action="store", default="test_config.yaml", help="配置文件"
    )


@pytest.fixture(scope="session", autouse=True)
def get_config(request):
    """环境预处理"""
    config = request.config.getoption("config")
    config_path = os.path.join(CONFIG_PATH, f'{config}')
    with open(config_path, "r", encoding="utf-8") as f:
        config_dict = yaml.safe_load(f)
    if config_dict:
        with open(TARGET_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(config_dict))
    base_token.get_admin_token(config_dict)
    base_token.get_student_token(config_dict)
    # base_debug.base_debug(base_token.get_admin_token(config_dict))


@pytest.fixture(scope="session", autouse=True)
def file_fixture():
    """文件预处理"""
    base_file.base_testfile()


@pytest.fixture(scope="session", autouse=True)
def fsetup_tear_down(request):
    """全局前后置处理器"""
    yield

    # 全局后置处理，添加报告中的环境变量 environment.properties
    config = request.config.getoption("config")
    config_path = os.path.join(BASE_PATH, 'config', f'{config}')
    with open(config_path, "r", encoding="utf-8") as f:
        config_contents = yaml.safe_load(f)
    config_contents["environment"] = os.path.splitext(f'{config}')[0]
    environment_content = ''
    for key, value in config_contents.items():
        environment_content += f"{key}={value}\n"
    with open(ENV_PRO, "w", encoding="utf-8") as f:
        f.write(environment_content)
    logging.info("后置处理完成.")


if __name__ == '__main__':
    pytest.main(['-s', '-q'])
