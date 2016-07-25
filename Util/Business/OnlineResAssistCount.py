#  -*- coding: utf-8 -*-
#!/usr/bin/python
#主要分析 算法在在线情况下的 辅助分析
#OnlineResCount.py
import os
from Util.Tools import MathHelper
from Util.Tools import LogHelper
logger = None

Total = 0
TotalOfflineAssistCount = 0
#没有使用准报站算法gps点数
TotalOfflineAssistCountNotInUse = 0
#准报站算法提供的意见准确率
TotalOfflineAssistCanCmp = 0
TotalOfflineAssistCorrect = 0

def initLogger(log_dir):
    global logger
    logger = LogHelper.makeConsoleAndFileLogger(os.path.join(log_dir,'在线辅助效果分析.log'))

def GetKernalReport():
    msg = '\n实时辅助概况总览:\n\n' + \
        '总共行数:%s\n'%Total + \
        '总共辅助:%s\n'%TotalOfflineAssistCount + \
        '没有使用的辅助:%s\n'%TotalOfflineAssistCountNotInUse + \
        '准确数:%s\n'%TotalOfflineAssistCorrect + \
        '可以比较的数:%s\n'%TotalOfflineAssistCanCmp + \
        '准确率:%s\n'%MathHelper.percentToString(TotalOfflineAssistCorrect, TotalOfflineAssistCanCmp)

    return msg

def Report(log_dir = 'log'):
    global logger
    initLogger(log_dir)
    if logger != None:
        logger.info('\n' + GetKernalReport())

def Count(bus_point, off_bus_point):
    global Total
    global TotalOfflineAssistCount
    global TotalOfflineAssistCountNotInUse
    global TotalOfflineAssistCanCmp
    global TotalOfflineAssistCorrect

    Total += 1

    #统计辅助使用率和准确率
    if bus_point.assist_line_id != '-':
        TotalOfflineAssistCount += 1
        if not bus_point.is_rec:
            TotalOfflineAssistCountNotInUse += 1

    if bus_point.assist_line_id != '-' and bus_point.is_rec:
        TotalOfflineAssistCanCmp += 1
        if bus_point.assist_line_id == off_bus_point.line_id:
            TotalOfflineAssistCorrect += 1

def Clear():
    global logger
    global Total
    global TotalOfflineAssistCount
    global TotalOfflineAssistCountNotInUse
    global TotalOfflineAssistCanCmp
    global TotalOfflineAssistCorrect

    logger = None

    Total = 0
    TotalOfflineAssistCount = 0
    #没有使用准报站算法gps点数
    TotalOfflineAssistCountNotInUse = 0
    #准报站算法提供的意见准确率
    TotalOfflineAssistCanCmp = 0
    TotalOfflineAssistCorrect = 0

    print('OnlineResAssistCount Clear')
