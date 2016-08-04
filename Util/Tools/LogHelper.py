#  -*- coding: utf-8 -*-
#!/usr/bin/python

#LogHelper.py
import logging, sys, inspect, os, codecs
from Util.Tools import DateHelp

def makeConsoleAndFileLogger(file_name):

    log_name = os.path.basename(file_name)
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    # 定义一个Handler打印INFO及以上级别的日志到sys.stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    # 定义一个FileHandler
    this_file = inspect.getfile(inspect.currentframe())
    dirpath = os.path.abspath(os.path.dirname(this_file))

    if (not os.path.exists(os.path.dirname(file_name))):
        os.makedirs(os.path.dirname(file_name))
    file_handler = logging.FileHandler(file_name)

    # 设置日志打印格式
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 将定义好的console日志handler添加到root logger
    logger.handlers = []
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def makeFileLogger(file_name):

    log_name = os.path.basename(file_name)
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.INFO)

    # 定义一个FileHandler
    this_file = inspect.getfile(inspect.currentframe())
    dirpath = os.path.abspath(os.path.dirname(this_file))

    if (not os.path.exists(os.path.dirname(file_name))):
        os.makedirs(os.path.dirname(file_name))
    file_handler = logging.FileHandler(file_name)

    # 设置日志打印格式
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    file_handler.setFormatter(formatter)

    # 将定义好的console日志handler添加到root logger
    logger.handlers = []
    logger.addHandler(file_handler)

    return logger

def printFile(file_name, mode, content):
    if (not os.path.exists(os.path.dirname(file_name))):
        os.makedirs(os.path.dirname(file_name))

    dest_file = codecs.open(file_name, mode, encoding='utf-8', errors='ignore')
    dest_file.write(content)
    dest_file.close()
