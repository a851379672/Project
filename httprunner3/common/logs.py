# -*- coding: utf-8 -*-
import logging
from logging import handlers
from settings import LOG_PATH


def logging_():
    # 初始化
    logger = logging.getLogger()
    # 日志等级
    logger.setLevel(logging.INFO)
    # 控制处理器
    sh = logging.StreamHandler()
    # 文件处理器
    th = handlers.TimedRotatingFileHandler(filename=LOG_PATH, when='D', interval=1, backupCount=7, encoding='utf-8')
    format_ = "%(asctime)s | %(pathname)s[line:%(lineno)d] | %(levelname)s: %(message)s"
    formatter_ = logging.Formatter(format_)
    sh.setFormatter(formatter_)
    th.setFormatter(formatter_)
    logger.addHandler(sh)
    logger.addHandler(th)


if __name__ == '__main__':
    logging_()
    logging.info('————————哎唷不错哦————————')
