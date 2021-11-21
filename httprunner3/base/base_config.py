# -*- coding: utf-8 -*-
import logging


def get_config_json(config_data, deal_with):
    """
    :param config_data: config_data
    :param deal_with: deal_with
    :return:
    """
    for key, value in config_data.items():
        deal_with.dicts.update({key: str(value)})
        logging.info(f'提取变量：{key}: {value}')
