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
        self.is_detected_by_zhunbaozhan = False
        self.miss_before_detected_by_zhunbaozhan = 0

    def addMiss(self):
        self.miss += 1
        if not self.is_detected_by_zhunbaozhan:
            self.miss_before_detected_by_zhunbaozhan += 1

    def report(self):
        global logger

        tmp = ''
        if self.is_detected_by_zhunbaozhan:
            tmp = str(self.miss_before_detected_by_zhunbaozhan)
        else:
            tmp = 'NotDetect'

        if logger != 0:
            logger.info(\
                'Bus_id: %s Total: %s Miss: %s MissBefore:%s Wrong: %s 丢失率: %s', \
                self.bus_id, self.total, self.miss, \
                tmp, \
                self.wrong, MathHelper.percentToString(self.miss,self.total))
            if self.wrong > 50 or self.miss > 50:
                logger.info('Found it!')

Total = 0
UselessTotal = 0
TotalCorrect = 0
TotalCorrectCanCmp = 0
TotalCorrectRight = 0
TotalCorrectMis = 0
BusMap = dict()

MissTimePeriod = dict()

def initLogger():
    global logger
    logger = LogHelper.makeConsoleAndFileLogger('在线算法评测')

def Report():
    global logger
    initLogger()

    miss_before = 0
    miss_after = 0
    miss_not_detect = 0
    for key in BusMap.keys():
        if BusMap[key].is_detected_by_zhunbaozhan:
            miss_before += BusMap[key].miss_before_detected_by_zhunbaozhan
            miss_after += BusMap[key].miss - BusMap[key].miss_before_detected_by_zhunbaozhan
        else:
            miss_not_detect += BusMap[key].miss

    if logger != 0:
        logger.info("\n实时算法概况总览: ")
        logger.info('总共%s行', Total)
        logger.info('无效数据%s行', UselessTotal)
        logger.info('识别总数:%s', TotalCorrect)
        logger.info('可以比较的总数:%s', TotalCorrectCanCmp)
        logger.info('准确数:%s', TotalCorrectRight)
        logger.info('miss数:%s', TotalCorrectMis)
        logger.info('准确率:%s', MathHelper.percentToString(TotalCorrectRight, TotalCorrectCanCmp))
        logger.info('占所有点准确率:%s', MathHelper.percentToString(TotalCorrectRight, Total))
        logger.info('在识别前miss:%s 在识别后miss:%s 未识别miss:%s', miss_before, miss_after, miss_not_detect)

    items = sorted(MissTimePeriod.items(), key=lambda d:d[0], reverse = False)
    for item in items:
        logger.info('Miss Num At Hour[%s] is %s.', item[0], item[1])

    for key in BusMap.keys():
        BusMap[key].report()

def Count(bus_point, off_bus_point):
    global Total
    global TotalCorrect
    global TotalCorrectCanCmp
    global TotalCorrectRight
    global TotalCorrectMis
    global BusMap
    global MissTimePeriod
    global UselessTotal

    if not bus_point.bus_id in BusMap.keys():
        BusMap[bus_point.bus_id] = OnlineResCountBus(bus_point.bus_id)

    if bus_point.is_assist_real_dectected:
        BusMap[bus_point.bus_id].is_detected_by_zhunbaozhan = True

    if int(bus_point.first_bit) < 0:
        UselessTotal += 1
        return

    Total += 1
    BusMap[bus_point.bus_id].total += 1

    if bus_point.is_rec:
        TotalCorrect += 1
        if off_bus_point.is_rec:
            TotalCorrectCanCmp += 1
            if bus_point.line_id == off_bus_point.line_id:
                TotalCorrectRight += 1
            else:
                BusMap[bus_point.bus_id].wrong += 1



    if not bus_point.is_rec and off_bus_point.is_rec:
        #print(bus_point.gps_time + ' ' + bus_point.gps_time[11:13])
        hour = bus_point.gps_time[11:13]
        if not hour in MissTimePeriod.keys():
            MissTimePeriod[hour] = 0
        MissTimePeriod[hour] += 1
        TotalCorrectMis += 1
        BusMap[bus_point.bus_id].addMiss()
