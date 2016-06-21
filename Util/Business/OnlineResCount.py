#  -*- coding: utf-8 -*-
#!/usr/bin/python

#OnlineResCount.py

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


    def missRate(self):
        if self.total != 0:
            return float(self.miss) / float(self.total)
        else:
            return 0

    def report(self):
        global logger
        if logger != 0:
            logger.info(\
                'Bus_id: %s Total: %s Miss: %s Wrong: %s 丢失率: %.3f%%', \
                self.bus_id, self.total, self.miss, self.wrong, self.missRate() * 100)

Total = 0
TotalCorrect = 0
TotalCorrectCanCmp = 0
TotalCorrectRight = 0
TotalCorrectMis = 0
BusMap = dict()

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
