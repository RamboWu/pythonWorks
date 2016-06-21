#  -*- coding: utf-8 -*-
#!/usr/bin/python

#BusStat.py
import codecs, sys, getopt
import logging
import inspect
import os
import time

sys.path.append("..")
from Util.Business import BusPoint
'''
Created on 2016-05-20

@author: RamboWu
'''

def getTime():
    ISOTIMEFORMAT = '%Y-%m-%d-%H-%M'
    return time.strftime( ISOTIMEFORMAT, time.localtime() )

logger = logging.getLogger('BusStat')
logger.setLevel(logging.INFO)

# 定义一个Handler打印INFO及以上级别的日志到sys.stdout
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
# 定义一个FileHandler
this_file = inspect.getfile(inspect.currentframe())
dirpath = os.path.abspath(os.path.dirname(this_file))

if (not os.path.exists('log')):
    os.makedirs('log')
log_file = 'log/bus_stat_' + getTime() + '.log'
file_handler = logging.FileHandler(log_file)

# 设置日志打印格式
formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将定义好的console日志handler添加到root logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


logger.info('BusState Log init finish!')



class BusStat:
    '''
    classdocs
    '''

    def __init__(self,bus_id):

        self.bus_id = bus_id
        self.total = 0
        self.miss = 0
        self.wrong = 0

        self.assist_real_detect_modify = 0
        self.assist_real_dectect_hit_miss = 0


    def missRate(self):
        if self.total != 0:
            return float(self.miss) / float(self.total)
        else:
            return 0

    def report(self):
        logger.info(\
            'Bus_id: %s Total: %s Miss: %s Wrong: %s 丢失率: %.3f%%, 离线矫正:%s, HitMiss:%s', \
            self.bus_id, self.total, self.miss, self.wrong, self.missRate() * 100, \
            self.assist_real_detect_modify, self.assist_real_dectect_hit_miss)

        #logger.info('Bus_id: %s 准报站算法矫正: %s 击中漏判: %s', \
            #self.bus_id, self.assist_real_detect_modify, self.assist_real_dectect_hit_miss)


class OneFileTest:

    def __init__(self, sample_file, cmp_file):
        #总共多少行
        self.total = 0
        #总共判出多少个点
        self.total_correct = 0
        #总共判对多少个点
        self.total_correct_right = 0
        #总共判错多少个
        self.total_correct_can_cmp = 0
        #少判出多少个
        self.total_correct_mis = 0
        #准报站算法总共提供的意见数
        self.total_offline_assist_count = 0
        #没有使用准报站算法gps点数
        self.total_offline_assist_count_not_in_use = 0
        #准报站算法提供的意见准确率
        self.total_offline_assist_can_cmp = 0
        self.total_offline_assist_correct = 0

        #在准报站算法里确实被识别了
        self.total_assist_real_detect = 0
        #矫正个数
        self.total_assist_real_detect_modify = 0
        #hit_miss
        self.total_assist_real_dectect_hit_miss = 0
        self.total_assist_real_dectect_can_cmp = 0
        self.total_assist_real_dectect_right = 0

        self.sample_file = sample_file
        self.cmp_file = cmp_file

        self.BusMap = dict()


    def ReportTotalStat(self):
        if (self.total == 0):
            self.total = 1
        if (self.total_correct == 0):
            self.total_correct = 1
        if (self.total_correct_can_cmp == 0):
            self.total_correct_can_cmp = 1

        logger.info(self.sample_file + " 概况总览: ")
        logger.info('总共%s行'%self.total)
        logger.info('识别总数:%s', self.total_correct)
        logger.info('可以比较的总数:%s', self.total_correct_can_cmp)
        logger.info('准确数:%s', self.total_correct_right)
        logger.info('miss数:%s', self.total_correct_mis)
        logger.info('准确率:%s', float(self.total_correct_right) / float(self.total_correct_can_cmp))
        logger.info('占所有点准确率:%s', float(self.total_correct_right) / float(self.total))

        if (self.total_offline_assist_count == 0):
            self.total_offline_assist_count = 1
        if (self.total_offline_assist_can_cmp == 0):
            self.total_offline_assist_can_cmp = 1

        logger.info(self.sample_file + " 辅助统计: ")

        logger.info('总辅助gps点数:%s', self.total_offline_assist_count)
        logger.info('没有使用的个数:%s', self.total_offline_assist_count_not_in_use)
        logger.info('可以cmp的总个数:%s', self.total_offline_assist_can_cmp)
        logger.info('准确的个数:%s', self.total_offline_assist_correct)
        logger.info('准确率:%s', float(self.total_offline_assist_correct)/float(self.total_offline_assist_can_cmp))

        logger.info(self.sample_file + " 准报站真实统计: ")
        logger.info('准报站算法总识别:%s', self.total_assist_real_detect)
        logger.info('共矫正:%s', self.total_assist_real_detect_modify)
        logger.info('击中漏判个数:%s', self.total_assist_real_dectect_hit_miss)
        logger.info('可以cmp的总个数:%s', self.total_assist_real_dectect_can_cmp)
        logger.info('准确个数:%s', self.total_assist_real_dectect_right)
        if self.total_assist_real_dectect_can_cmp == 0:
            self.total_assist_real_dectect_can_cmp = 1
        logger.info('准确率:%s', float(self.total_assist_real_dectect_right)/float(self.total_assist_real_dectect_can_cmp))

        for key in self.BusMap.keys():
            self.BusMap[key].report()

    def JudgeOnline(self, bus_point, off_bus_point):
        if bus_point.is_rec:
            self.total_correct += 1
            if off_bus_point.is_rec:
                self.total_correct_can_cmp += 1
                if bus_point.bus_id == off_bus_point.bus_id:
                    self.total_correct_right += 1
                else:
                    self.BusMap[bus_point.bus_id].wrong += 1

        if not bus_point.is_rec and off_bus_point.is_rec:
            self.total_correct_mis += 1
            self.BusMap[bus_point.bus_id].miss += 1

    def JudgeOffLineAssist(self, bus_point, off_bus_point):
        #统计辅助使用率和准确率
        if bus_point.assist_line_id != '-':
            self.total_offline_assist_count += 1
            if not bus_point.is_rec:
                self.total_offline_assist_count_not_in_use += 1

        if bus_point.assist_line_id != '-' and bus_point.is_rec:
            self.total_offline_assist_can_cmp += 1
            if bus_point.assist_line_id == off_bus_point.line_id:
                self.total_offline_assist_correct += 1

    def JudgeRealAssist(self, bus_point, off_bus_point):
        if bus_point.is_assist_real_dectected:
            self.total_assist_real_detect += 1
            if not bus_point.is_rec:
                self.total_assist_real_detect_modify += 1
                self.BusMap[bus_point.bus_id].assist_real_detect_modify += 1

                if off_bus_point.is_rec:
                    self.total_assist_real_dectect_hit_miss += 1
                    self.BusMap[bus_point.bus_id].assist_real_dectect_hit_miss += 1

            if off_bus_point.is_rec:
                self.total_assist_real_dectect_can_cmp += 1
                if bus_point.line_id == off_bus_point.line_id:
                    self.total_assist_real_dectect_right += 1

    def Judge(self, sample_line, cmp_line,lineno):
        if (sample_line.strip() == ""):
            return -1
        if (cmp_line.strip() == ""):
            return -2

        bus_point = BusPoint.BusPoint(sample_line)
        off_bus_point = BusPoint.OffLineBusPoint(cmp_line)

        if bus_point.bus_id < off_bus_point.bus_id:
            return -1
        if bus_point.bus_id > off_bus_point.bus_id:
            return -2

        if bus_point.bus_id != off_bus_point.bus_id or bus_point.gps_time != off_bus_point.gps_time:
            logger.error("lineNo:%s sample_line: %s; cmp_line: %s. ", lineno, sample_line, cmp_line)
            sys.exit(0)

        if bus_point.bus_id in self.BusMap.keys():
            bus_stat = self.BusMap.get(bus_point.bus_id)
        else:
            #print ('create Bus:', sample_line_tags[3])
            bus_stat = BusStat(bus_point.bus_id)
            self.BusMap[bus_point.bus_id] = bus_stat

        self.total += 1
        self.BusMap[bus_point.bus_id].total += 1

        self.JudgeOnline(bus_point, off_bus_point)
        self.JudgeOffLineAssist(bus_point, off_bus_point)
        self.JudgeRealAssist(bus_point, off_bus_point)

        return 0

    def CountAccuracy(self):
        logger.info('开始统计:')
        sample_file = codecs.open(self.sample_file, 'r', 'utf-8')
        cmp_file = codecs.open(self.cmp_file, 'r', 'utf-8')

        sample_line = sample_file.readline()
        cmp_line = cmp_file.readline()

        lineno = 0
        while sample_line and cmp_line:

            res = self.Judge(sample_line, cmp_line,lineno)
            if res == 0:
                lineno+=1
                sample_line = sample_file.readline()
                cmp_line = cmp_file.readline()
            elif res == -1:
                lineno+=1
                sample_line = sample_file.readline()
            elif res == -2:
                cmp_line = cmp_file.readline()

        logger.info('总行数:%s', lineno)
        self.ReportTotalStat()

def parseParams():
    opts, args = getopt.getopt(sys.argv[1:], "hi:j:", ["input_file=","judge_file="])

    input_file = ""
    judge_file = ""

    for op, value in opts:
        if op in ('-i','--input_file'):
            input_file = value
        elif op == '-j':
            judge_file = value

    print("CommandParam:")
    print("input_file=", input_file, "judge_file=", judge_file)

    if (input_file == ""):
        print('not right command line')
        sys.exit()

    return input_file, judge_file

if __name__=="__main__":
    input_file, judge_file = parseParams()
    test = OneFileTest(input_file, judge_file)
    test.CountAccuracy()
