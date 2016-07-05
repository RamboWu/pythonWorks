#  -*- coding: utf-8 -*-
#!/usr/bin/python

#OnlineResCount.py
from Util.Tools import MathHelper
from Util.Tools import LogHelper
logger = 0

class OnlineResCountBus:
    '''
    classdocs
    '''
    def __init__(self,bus_id):

        self.bus_id = bus_id
        self.total = 0
        self.miss = 0
        self.wrong = 0

    def report(self):
        global logger
        if logger != 0:
            logger.info(\
                'Bus_id: %s Total: %s Miss: %s Wrong: %s 丢失率: %s', \
                self.bus_id, self.total, self.miss, self.wrong, MathHelper.percentToString(self.miss,self.total))

Total = 0
TotalCorrect = 0
TotalCorrectCanCmp = 0
TotalCorrectRight = 0
TotalCorrectMis = 0
BusMap = dict()

def initLogger():
    global logger
    logger = LogHelper.makeConsoleAndFileLogger('在线算法评测')

def Report():
    global logger
    initLogger()
    if logger != 0:
        logger.info("\n实时算法概况总览: ")
        logger.info('总共%s行', Total)
        logger.info('识别总数:%s', TotalCorrect)
        logger.info('可以比较的总数:%s', TotalCorrectCanCmp)
        logger.info('准确数:%s', TotalCorrectRight)
        logger.info('miss数:%s', TotalCorrectMis)
        logger.info('准确率:%s', MathHelper.percentToString(TotalCorrectRight, TotalCorrectCanCmp))
        logger.info('占所有点准确率:%s', MathHelper.percentToString(TotalCorrectRight, Total))

    for key in BusMap.keys():
        BusMap[key].report()

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

    if bus_point.is_rec:
        TotalCorrect += 1
        if off_bus_point.is_rec:
            TotalCorrectCanCmp += 1
            if bus_point.bus_id == off_bus_point.bus_id:
                TotalCorrectRight += 1
            else:
                BusMap[bus_point.bus_id].wrong += 1

    if not bus_point.is_rec and off_bus_point.is_rec:
        TotalCorrectMis += 1
        BusMap[bus_point.bus_id].miss += 1
