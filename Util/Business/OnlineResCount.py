#  -*- coding: utf-8 -*-
#!/usr/bin/python

#OnlineResCount.py
import os
from Util.Tools import MathHelper
from Util.Tools import LogHelper
logger = 0
dir_wrong_logger = 0

class OnlineResCountBus:
    '''
    classdocs
    '''
    def __init__(self,bus_id):

        self.bus_id = bus_id
        self.total = 0
        self.miss = 0
        self.direction_wrong = 0
        self.wrong = 0
        self.wrong_2 = 0
        self.is_detected_by_zhunbaozhan = False
        self.miss_before_detected_by_zhunbaozhan = 0

    def addMiss(self):
        self.miss += 1
        if not self.is_detected_by_zhunbaozhan:
            self.miss_before_detected_by_zhunbaozhan += 1

    def tostring(self):
        global logger

        tmp = ''
        if self.is_detected_by_zhunbaozhan:
            tmp = str(self.miss_before_detected_by_zhunbaozhan)
        else:
            tmp = 'NotDetect'

        msg = 'Bus_id: %s Total: %s Miss: %s MissBefore:%s Wrong: %s Wrong2: %s 方向错误:%s 丢失率: %s'% \
            (self.bus_id, self.total, self.miss, tmp, self.wrong, self.wrong_2, self.direction_wrong, MathHelper.percentToString(self.miss,self.total))

        return msg

Total = 0
UselessTotal = 0
TotalCorrect = 0
TotalCorrectCanCmp = 0
TotalCorrectRight = 0
TotalCorrectMis = 0
TotalDirWrong = 0
BusMap = dict()

MissTimePeriod = dict()
dirWrongLines = []

def initLogger(log_dir):
    global logger
    global dir_wrong_logger
    logger = LogHelper.makeConsoleAndFileLogger(os.path.join(log_dir,'在线算法评测.log'))
    dir_wrong_logger = LogHelper.makeFileLogger(os.path.join(log_dir,'方向错误.log'))

def GetKernalReport():
    miss_before = 0
    miss_after = 0
    miss_not_detect = 0
    total_wrong = 0
    total_wrong2 = 0
    miss_caused_by_wrong = 0
    miss_caused_by_dir_wrong = 0
    for key in BusMap.keys():
        if BusMap[key].is_detected_by_zhunbaozhan:
            miss_before += BusMap[key].miss_before_detected_by_zhunbaozhan
            miss_after += BusMap[key].miss - BusMap[key].miss_before_detected_by_zhunbaozhan
        else:
            miss_not_detect += BusMap[key].miss
        total_wrong += BusMap[key].wrong
        total_wrong2 += BusMap[key].wrong_2
        if BusMap[key].wrong > 0:
            miss_caused_by_wrong += BusMap[key].miss
        if BusMap[key].direction_wrong > 0:
            miss_caused_by_dir_wrong += BusMap[key].miss

    msg = '在线统计分析:\n\n' + \
        '总共行数:%s\n'%Total + \
        '无效数据行数:%s\n'%UselessTotal + \
        '识别总数:%s\n'%TotalCorrect + \
        '线路错误:%s\n'%total_wrong + \
        '方向错误:%s\n'%TotalDirWrong + \
        '\t2号线路错误:%s\n'%total_wrong2 + \
        '\t可以比较的总数:%s\n'%TotalCorrectCanCmp + \
        '\t准确数:%s\n'%TotalCorrectRight + \
        '\t准确率:%s\n'%MathHelper.percentToString(TotalCorrectRight, TotalCorrectCanCmp) + \
        '\t占所有点准确率:%s\n'%MathHelper.percentToString(TotalCorrectRight, Total) + \
        'miss数:%s\n'%TotalCorrectMis + \
        '\t由线路错误导致的miss数:%s\n'%miss_caused_by_wrong + \
        '\t由方向错误导致的miss数:%s\n'%miss_caused_by_dir_wrong + \
        '\t在识别前miss:%s 在识别后miss:%s 未识别miss:%s\n'%(miss_before, miss_after, miss_not_detect)

    return msg

def Report(log_dir = 'log'):
    global logger
    global dir_wrong_logger
    initLogger(log_dir)

    if logger != 0:
        logger.info('\n' + GetKernalReport())

    items = sorted(MissTimePeriod.items(), key=lambda d:d[0], reverse = False)
    for item in items:
        logger.info('Miss Num At Hour[%s:%s] is %s.', str(int(item[0]*10/60)), str(item[0]%6*10), item[1])

    missafter_buses = []
    dirwrong_buses = []
    onlinewrong_buses = []
    for key in BusMap.keys():
        if BusMap[key].miss - BusMap[key].miss_before_detected_by_zhunbaozhan > 50 and \
            BusMap[key].is_detected_by_zhunbaozhan:
            missafter_buses.append(key)
        if BusMap[key].direction_wrong > 20:
            dirwrong_buses.append(key)
        if BusMap[key].wrong > 20:
            onlinewrong_buses.append(key)

    logger.info('MissAfter Buses are: %s', missafter_buses)
    logger.info('OnlineWrong Buses are: %s', onlinewrong_buses)
    logger.info('DirWrong Buses are: %s', dirwrong_buses)

    for key in BusMap.keys():
        logger.info(BusMap[key].tostring())

    for line in dirWrongLines:
        dir_wrong_logger.info(line)

    return missafter_buses, dirwrong_buses, onlinewrong_buses

def Count(bus_point, off_bus_point):
    global Total
    global TotalCorrect
    global TotalCorrectCanCmp
    global TotalCorrectRight
    global TotalCorrectMis
    global BusMap
    global MissTimePeriod
    global UselessTotal
    global TotalDirWrong

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
            if bus_point.dir != off_bus_point.dir:
                TotalDirWrong += 1
                BusMap[bus_point.bus_id].direction_wrong += 1
                dirWrongLines.append(\
                'Sample: %s %s %s %s %s %s Cmp: %s %s %s %s %s %s '%\
                (bus_point.first_bit, bus_point.bus_id, bus_point.dir, bus_point.line_id, bus_point.gps_time, bus_point.recv_time,\
                off_bus_point.first_bit, off_bus_point.bus_id, off_bus_point.dir, off_bus_point.line_id, off_bus_point.gps_time, off_bus_point.recv_time))
                #print(bus_point.gps_time)

        if off_bus_point.is_rec or off_bus_point.first_bit == '2':
            TotalCorrectCanCmp += 1
            if bus_point.line_id == off_bus_point.line_id:
                TotalCorrectRight += 1
            else:
                BusMap[bus_point.bus_id].wrong += 1
                if off_bus_point.first_bit == '2':
                    BusMap[bus_point.bus_id].wrong_2 += 1



    if not bus_point.is_rec and off_bus_point.is_rec:
        period = int((int(bus_point.gps_time[11:13])*60 + int(bus_point.gps_time[14:16]))/10)
        #print(bus_point.gps_time + ' ' + str(period) + ' ' + str(int(period*10/60)) + ' ' + str(period%6*10))
        if not period in MissTimePeriod.keys():
            MissTimePeriod[period] = 0
        MissTimePeriod[period] += 1
        TotalCorrectMis += 1
        BusMap[bus_point.bus_id].addMiss()

def Clear():
    global Total
    global UselessTotal
    global TotalCorrect
    global TotalCorrectCanCmp
    global TotalCorrectRight
    global TotalCorrectMis
    global TotalDirWrong
    global BusMap
    global MissTimePeriod
    global dirWrongLines
    global logger
    global dir_wrong_logger

    Total = 0
    UselessTotal = 0
    TotalCorrect = 0
    TotalCorrectCanCmp = 0
    TotalCorrectRight = 0
    TotalCorrectMis = 0
    TotalDirWrong = 0
    BusMap = dict()
    MissTimePeriod = dict()
    dirWrongLines = []
    logger = 0
    dir_wrong_logger = 0

    print('OnlineResCount Clear')
