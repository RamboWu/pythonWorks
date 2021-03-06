#  -*- coding: utf-8 -*-
#!/usr/bin/python
#统计原始线路编码给错，或者不给的情况下的，线路错误情况，并且看看如果车辆被准报站识别前后有多少 这种错误，还有没被识别的有多少错误
#OnlineResCount.py
import os
from Util.Tools import MathHelper
from Util.Tools import LogHelper
logger = 0

class CountOriginalWrongBus:
    '''
    classdocs
    '''
    def __init__(self,bus_id):

        self.bus_id = bus_id
        self.total_can_cmp = 0
        self.total_original_diff = 0
        self.total_original_diff_wrong = 0
        self.total_original_diff_miss = 0
        self.is_detected_by_zhunbaozhan = False
        self.wrong_before_detected_by_zhunbaozhan = 0
        self.miss_before_detected_by_zhunbaozhan = 0

    def addWrong(self):
        self.total_original_diff_wrong += 1
        if not self.is_detected_by_zhunbaozhan:
            self.wrong_before_detected_by_zhunbaozhan += 1

    def addMiss(self):
        self.total_original_diff_miss += 1
        if not self.is_detected_by_zhunbaozhan:
            self.miss_before_detected_by_zhunbaozhan += 1

    def info(self):

        wrong_tmp = ''
        miss_tmp = ''
        if self.is_detected_by_zhunbaozhan:
            wrong_tmp = str(self.wrong_before_detected_by_zhunbaozhan)
            miss_tmp = str(self.miss_before_detected_by_zhunbaozhan)
        else:
            wrong_tmp = 'NotDetect'
            miss_tmp = 'NotDetect'

        msg = 'Bus_id: %s TotalCanCmp: %s 原始线路编号不正确: %s 导致错误个数: %s WrongBefore:%s 错误率: %s 导致Miss数: %s MissBefore: %s'%\
                (self.bus_id, self.total_can_cmp, self.total_original_diff, \
                self.total_original_diff_wrong, wrong_tmp, \
                MathHelper.percentToString(self.total_original_diff_wrong, self.total_original_diff), \
                self.total_original_diff_miss, miss_tmp)
        return msg

BusMap = dict()

def initLogger(log_dir):
    global logger
    logger = LogHelper.makeConsoleAndFileLogger(os.path.join(log_dir,'原始线路编码给错分析.log'))

def GetKernalReport():
    original_diff_wrong_before = 0
    original_diff_wrong_after = 0
    original_diff_wrong_not_detect = 0
    original_diff_miss_before = 0
    original_diff_miss_after = 0
    original_diff_miss_not_detect = 0
    TotalCanCmp = 0
    TotalOriginalDiff = 0
    TotalOriginalDiffWrong = 0
    for key in BusMap.keys():
        if BusMap[key].is_detected_by_zhunbaozhan:
            original_diff_wrong_before += BusMap[key].wrong_before_detected_by_zhunbaozhan
            original_diff_wrong_after += BusMap[key].total_original_diff_wrong - BusMap[key].wrong_before_detected_by_zhunbaozhan
            original_diff_miss_before += BusMap[key].miss_before_detected_by_zhunbaozhan
            original_diff_miss_after += BusMap[key].total_original_diff_miss - BusMap[key].miss_before_detected_by_zhunbaozhan
        else:
            original_diff_wrong_not_detect += BusMap[key].total_original_diff_wrong
            original_diff_miss_not_detect += BusMap[key].total_original_diff_miss

        TotalCanCmp += BusMap[key].total_can_cmp
        TotalOriginalDiff += BusMap[key].total_original_diff
        TotalOriginalDiffWrong += BusMap[key].total_original_diff_wrong

    msg = '\n<原始线路编号错误分析>\n\n' + \
        '总共可比较:%s\n'%TotalCanCmp + \
        '线路编号给错总数:%s\n'%TotalOriginalDiff + \
        '导致错误数:%s\n'%TotalOriginalDiffWrong + \
        '导致Miss数:%s\n'%(original_diff_miss_before+original_diff_miss_after+original_diff_miss_not_detect) + \
        '错误率:%s\n'%MathHelper.percentToString(TotalOriginalDiffWrong, TotalOriginalDiff) + \
        '在识别前wrong:%s 在识别后wrong:%s 未识别wrong:%s\n'%(original_diff_wrong_before, original_diff_wrong_after, original_diff_wrong_not_detect) + \
        '在识别前Miss:%s 在识别后Miss:%s 未识别Miss:%s\n'%(original_diff_miss_before, original_diff_miss_after, original_diff_miss_not_detect)

    return msg

def Report(log_dir = 'log'):
    global logger
    initLogger(log_dir)

    original_diff_wrong_buses = []
    for key in BusMap.keys():
        if BusMap[key].total_original_diff > 0:
            original_diff_wrong_buses.append(key)

    if logger != 0:
        logger.info(GetKernalReport())

        logger.info('Original Diff Wrong Buses are: %s', original_diff_wrong_buses)

    for key in BusMap.keys():
        if BusMap[key].total_original_diff > 0:
            logger.info(BusMap[key].info())

    return original_diff_wrong_buses

def Count(bus_point, off_bus_point):
    global BusMap

    if not bus_point.bus_id in BusMap.keys():
        BusMap[bus_point.bus_id] = CountOriginalWrongBus(bus_point.bus_id)

    if bus_point.is_assist_real_dectected:
        BusMap[bus_point.bus_id].is_detected_by_zhunbaozhan = True

    if int(bus_point.first_bit) < 0:
        return

    if bus_point.is_rec and off_bus_point.is_rec:
        BusMap[bus_point.bus_id].total_can_cmp += 1
        if bus_point.original_line_id != off_bus_point.line_id:
            BusMap[bus_point.bus_id].total_original_diff += 1
            if bus_point.line_id != off_bus_point.line_id:
                BusMap[bus_point.bus_id].addWrong()

    if not bus_point.is_rec and off_bus_point.is_rec:
        if bus_point.original_line_id != off_bus_point.line_id:
            BusMap[bus_point.bus_id].addMiss()

def Clear():
    global BusMap
    global logger
    BusMap = dict()
    logger = 0
    print('CountOriginalWrong Clear')
