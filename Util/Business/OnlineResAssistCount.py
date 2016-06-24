#  -*- coding: utf-8 -*-
#!/usr/bin/python

#OnlineResCount.py

from Util.Tools import MathHelper
logger = None

Total = 0
TotalOfflineAssistCount = 0
#没有使用准报站算法gps点数
TotalOfflineAssistCountNotInUse = 0
#准报站算法提供的意见准确率
TotalOfflineAssistCanCmp = 0
TotalOfflineAssistCorrect = 0

def Report():
    global logger
    if logger != None:
        logger.info("\n实时辅助概况总览: ")
        logger.info('总共%s行', Total)
        logger.info('总共辅助:%s', TotalOfflineAssistCount)
        logger.info('没有使用的辅助:%s', TotalOfflineAssistCountNotInUse)
        logger.info('准确数:%s', TotalOfflineAssistCorrect)
        logger.info('可以比较的数:%s', TotalOfflineAssistCanCmp)
        logger.info('准确率:%s', MathHelper.percentToString(TotalOfflineAssistCorrect, TotalOfflineAssistCanCmp))


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
