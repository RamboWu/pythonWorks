#  -*- coding: utf-8 -*-
#!/usr/bin/python

#LogHelper.py
import logging, sys, inspect, os
from Util.Tools import DateHelp

def makeConsoleAndFileLogger(log_name):

    logger = logging.getLogger('BusStat')
    logger.setLevel(logging.INFO)

    # 定义一个Handler打印INFO及以上级别的日志到sys.stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    # 定义一个FileHandler
    this_file = inspect.getfile(inspect.currentframe())
    dirpath = os.path.abspath(os.path.dirname(this_file))

    if (not os.path.exists('log')):
        os.makedirs('log')
    log_file = 'log/' + log_name + DateHelp.getTime() + '.log'
    file_handler = logging.FileHandler(log_file)

    # 设置日志打印格式
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 将定义好的console日志handler添加到root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
