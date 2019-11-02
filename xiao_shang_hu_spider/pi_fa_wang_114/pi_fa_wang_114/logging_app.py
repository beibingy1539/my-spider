#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import datetime
import os
from logging.handlers import RotatingFileHandler

# 线上日志文件目录
file_name = datetime.datetime.now().strftime('%Y-%m-%d')
file_path = '/store/logs/goods-ext-checkuser-py/' + file_name
if not os.path.exists(file_path):
    os.makedirs(file_path)

LOG_FILENAME = '/store/logs/goods-ext-checkuser-py/{}/goods-ext-checkuser-py.{}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d'), datetime.datetime.now().strftime('%Y-%m-%d'))
logger = logging.getLogger("AppName")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(LOG_FILENAME, encoding='UTF-8', maxBytes=1024 * 1024 * 100, backupCount=999)
handler.setLevel(logging.DEBUG)

logging_format = logging.Formatter(
    '%(asctime)s  - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

handler.setFormatter(logging_format)
logger.addHandler(handler)