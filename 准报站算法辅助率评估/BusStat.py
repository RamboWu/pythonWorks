#  -*- coding: utf-8 -*-
#!/usr/bin/python

#BusStat.py
import codecs, sys
import logging
import inspect
import os
import time
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
log_file = 'log/' + getTime() + '.log'
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

    def missRate(self):
        if self.total != 0:
            return float(self.miss) / float(self.total)
        else:
            return 0

    def report(self):
        logger.info(\
            'Bus_id: %s Total: %s Miss: %s Wrong: %s 丢失率: %.3f%%', \
            self.bus_id, self.total, self.miss, self.wrong, self.missRate() * 100)


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

        logger.info(self.sample_file + " 准报站统计: ")

        logger.info('准报站算法总gps点数:%s', self.total_offline_assist_count)
        logger.info('没有使用的个数:%s', self.total_offline_assist_count_not_in_use)
        logger.info('可以cmp的总个数:%s', self.total_offline_assist_can_cmp)
        logger.info('准确的个数:%s', self.total_offline_assist_correct)
        logger.info('准确率:%s', float(self.total_offline_assist_correct)/float(self.total_offline_assist_can_cmp))

        for key in self.BusMap.keys():
            self.BusMap[key].report()

    def Judge(self, sample_line, cmp_line,lineno):
        sample_line = sample_line.strip()
        sample_line_tags = sample_line.split(',')
        count = sample_line.count(',') + 1
        cmp_line_tags = cmp_line.split(',')

        if sample_line_tags[3] != cmp_line_tags[3]:
            logger.error("lineNo:%s sample_line: %s; cmp_line: %s. ", lineno, sample_line, cmp_line)
            sys.exit(0)

        if sample_line_tags[3] in self.BusMap.keys():
            bus_stat = self.BusMap.get(sample_line_tags[3])
        else:
            #print ('create Bus:', sample_line_tags[3])
            bus_stat = BusStat(sample_line_tags[3])
            self.BusMap[sample_line_tags[3]] = bus_stat

        self.total += 1
        self.BusMap[sample_line_tags[3]].total += 1

        if int(sample_line_tags[0]) == 1:
            self.total_correct += 1
            if int(cmp_line_tags[0]) == 1:
                self.total_correct_can_cmp += 1
                if sample_line_tags[4] == cmp_line_tags[4]:
                    self.total_correct_right += 1
                else:
                    self.BusMap[sample_line_tags[3]].wrong += 1

        if int(sample_line_tags[0]) != 1 and int(cmp_line_tags[0]) == 1:
            self.total_correct_mis += 1
            self.BusMap[sample_line_tags[3]].miss += 1

        #统计准报站算法的使用率和准确率
        index = 18
        if count > index and sample_line_tags[index] != '-':
            self.total_offline_assist_count += 1
            if int(sample_line_tags[0]) == 0:
                self.total_offline_assist_count_not_in_use += 1

        if count > index and sample_line_tags[index] != '-' and int(cmp_line_tags[0]) == 1:
            self.total_offline_assist_can_cmp += 1
            if sample_line_tags[index] == cmp_line_tags[4]:
                self.total_offline_assist_correct += 1
            else:
                #print(sample_line_tags[19])
                #print(cmp_line_tags[4])
                #print("lineNo:"+str(lineno), sample_line, ' cmp:', cmp_line)
                #sys.exit(0)
                pass


    def CountAccuracy(self):
        logger.info('开始统计:')
        sample_file = codecs.open(self.sample_file, 'r', 'utf-8')
        cmp_file = codecs.open(self.cmp_file, 'r', 'utf-8')

        sample_line = sample_file.readline()
        cmp_line = cmp_file.readline()

        lineno = 0
        while sample_line and cmp_line:
            lineno+=1
            self.Judge(sample_line, cmp_line,lineno)
            sample_line = sample_file.readline()
            cmp_line = cmp_file.readline()

        logger.info('总行数:%s', lineno)
        self.ReportTotalStat()
