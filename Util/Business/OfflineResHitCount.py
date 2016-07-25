#  -*- coding: utf-8 -*-
#!/usr/bin/python

'''
用于统计 离线情况下的 准报站算法识别情况，每一辆车的矫正情况，判出时间统计
'''

#OnlineResCount.py
import os
from Util.Tools import MathHelper
from Util.Tools import LogHelper
logger = None

class BusStat:
    '''
    classdocs
    '''
    def __init__(self,bus_id):

        self.bus_id = bus_id
        self.total = 0
        self.assist_real_detect = 0
        self.assist_real_detect_modify = 0
        self.assist_real_dectect_hit_miss = 0
        self.assist_real_dectect_wrong = 0
        self.assist_real_dectect_time = ''

    def report(self):
        global logger
        if logger != None:
            logger.info(\
                'Bus_id: %s Total: %s 识别时间:%s 识别数量:%s 矫正:%s, HitMiss:%s 识别率:%s, 错误:%s', \
                self.bus_id, self.total, \
                self.assist_real_dectect_time, \
                self.assist_real_detect, self.assist_real_detect_modify, self.assist_real_dectect_hit_miss,\
                MathHelper.percentToString(self.assist_real_detect, self.total), self.assist_real_dectect_wrong)
            if self.assist_real_dectect_wrong > 0:
                logger.info('Found it!')

Total = 0
TotalAssistRealDetect = 0
#矫正个数
TotalAssistRealDetectModify = 0
#hit_miss
TotalAssistRealDectectHitMiss = 0
TotalAssistRealDectectCanCmp = 0
TotalAssistRealDectectRight = 0
TotalAssistRealDectectWrong = 0
BusMap = dict()
DetectTimePeriod = dict()

def initLogger(log_dir):
    global logger
    logger = LogHelper.makeConsoleAndFileLogger(os.path.join(log_dir,'准报站统计.log'))

def GetKernalReport():
    msg = '\n<离线算法概况总览>\n\n' + \
        '总共行数:%s\n'%Total + \
        '离线识别总数:%s\n'%TotalAssistRealDetect + \
        '离线矫正总数:%s\n'%TotalAssistRealDetectModify + \
        'HitMiss:%s\n'%TotalAssistRealDectectHitMiss + \
        '可以比较的数量:%s\n'%TotalAssistRealDectectCanCmp + \
        '准确数:%s\n'%TotalAssistRealDectectRight + \
        '错误数:%s\n'%TotalAssistRealDectectWrong + \
        '准确率:%s\n'%MathHelper.percentToString(TotalAssistRealDectectRight, TotalAssistRealDectectCanCmp)

    return msg

def Report(log_dir = 'log'):
    global logger
    initLogger(log_dir)
    if logger != None:
        logger.info(GetKernalReport())

    items = sorted(DetectTimePeriod.items(), key=lambda d:d[0], reverse = False)
    detect_num = 0
    for item in items:
        detect_num += item[1]
        logger.info('Detect Num At Hour[%s] is %s.', item[0], item[1])
    logger.info('NoDetect Num is %s.', len(BusMap) - detect_num)

    nodetect_buses = []
    wrong_buses = []
    for key in BusMap.keys():
        if BusMap[key].assist_real_dectect_time == '':
            nodetect_buses.append(key)
        if BusMap[key].assist_real_dectect_wrong > 0:
            wrong_buses.append(key)

    logger.info('NoDetect Buses are: %s', nodetect_buses)
    logger.info('Wrong Buses are: %s', wrong_buses)

    if TotalAssistRealDetect == 0:
        nodetect_buses = []

    for key in BusMap.keys():
        BusMap[key].report()

    return nodetect_buses, wrong_buses

def Count(bus_point, off_bus_point):
    global Total
    global TotalAssistRealDetect
    global TotalAssistRealDetectModify
    global TotalAssistRealDectectHitMiss
    global TotalAssistRealDectectCanCmp
    global TotalAssistRealDectectRight
    global TotalAssistRealDectectWrong
    global BusMap

    if not bus_point.bus_id in BusMap.keys():
        BusMap[bus_point.bus_id] = BusStat(bus_point.bus_id)

    if bus_point.is_assist_real_dectected:
        if (BusMap[bus_point.bus_id].assist_real_dectect_time == ''):
            BusMap[bus_point.bus_id].assist_real_dectect_time = bus_point.gps_time
            hour = bus_point.gps_time[11:13]
            if not hour in DetectTimePeriod.keys():
                DetectTimePeriod[hour] = 0
            DetectTimePeriod[hour] += 1

    if int(bus_point.first_bit) < 0:
        return

    Total += 1
    BusMap[bus_point.bus_id].total += 1

    if bus_point.is_assist_real_dectected:
        TotalAssistRealDetect += 1
        BusMap[bus_point.bus_id].assist_real_detect += 1
        if not bus_point.is_rec:
            TotalAssistRealDetectModify += 1
            BusMap[bus_point.bus_id].assist_real_detect_modify += 1

            if off_bus_point.is_rec:
                TotalAssistRealDectectHitMiss += 1
                BusMap[bus_point.bus_id].assist_real_dectect_hit_miss += 1

        if off_bus_point.is_rec:
            TotalAssistRealDectectCanCmp += 1
            if bus_point.zhunbaozhan_line_id == off_bus_point.line_id:
                TotalAssistRealDectectRight += 1
            else:
                TotalAssistRealDectectWrong += 1
                BusMap[bus_point.bus_id].assist_real_dectect_wrong += 1

def Clear():
    global Total
    global TotalAssistRealDetect
    global TotalAssistRealDetectModify
    global TotalAssistRealDectectHitMiss
    global TotalAssistRealDectectCanCmp
    global TotalAssistRealDectectRight
    global TotalAssistRealDectectWrong
    global BusMap
    global DetectTimePeriod
    global logger

    Total = 0
    TotalAssistRealDetect = 0
    #矫正个数
    TotalAssistRealDetectModify = 0
    #hit_miss
    TotalAssistRealDectectHitMiss = 0
    TotalAssistRealDectectCanCmp = 0
    TotalAssistRealDectectRight = 0
    TotalAssistRealDectectWrong = 0
    BusMap = dict()
    DetectTimePeriod = dict()
    logger = None

    print('OfflineResHitCount Clear')
