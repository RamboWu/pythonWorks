#  -*- coding: utf-8 -*-
#!/usr/bin/python

#OnlineResCount.py

logger = 0


Total = 0
TotalCorrect = 0
TotalCorrectCanCmp = 0
TotalCorrectRight = 0
TotalCorrectMis = 0

def percent(a, b):
    if (b == 0):
        b = 1
    return "%.2f%%"%(float(a)/float(b))

def Report():
    global logger
    if logger != 0:
        logger.info("实时算法概况总览: ")
        logger.info('总共%s行', Total)
        logger.info('识别总数:%s', TotalCorrect)
        logger.info('可以比较的总数:%s', TotalCorrectCanCmp)
        logger.info('准确数:%s', TotalCorrectRight)
        logger.info('miss数:%s', TotalCorrectMis)
        logger.info('准确率:%s', percent(TotalCorrectRight, TotalCorrectCanCmp))
        logger.info('占所有点准确率:%s', percent(TotalCorrectRight, Total))


def Count(bus_point, off_bus_point):
    global Total
    global TotalCorrect
    global TotalCorrectCanCmp
    global TotalCorrectRight
    global TotalCorrectMis
    global BusMap

    if bus_point.bus_id in BusMap.keys():
        bus_stat = BusMap.get(bus_point.bus_id)
    else:
        bus_stat = OnlineResCountBus(bus_point.bus_id)
        BusMap[bus_point.bus_id] = bus_stat

    Total += 1
    BusMap[bus_point.bus_id].total += 1

    #统计辅助使用率和准确率
    if bus_point.assist_line_id != '-':
        self.total_offline_assist_count += 1
        if not bus_point.is_rec:
            self.total_offline_assist_count_not_in_use += 1

    if bus_point.assist_line_id != '-' and bus_point.is_rec:
        self.total_offline_assist_can_cmp += 1
        if bus_point.assist_line_id == off_bus_point.line_id:
            self.total_offline_assist_correct += 1
