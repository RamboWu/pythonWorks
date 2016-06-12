#  -*- coding: utf-8 -*-
#!/usr/bin/python

#BusStat.py
import codecs
'''
Created on 2016-05-20

@author: RamboWu
'''

class BusStat:
    '''
    classdocs
    '''

    def __init__(self,bus_id):

        self.bus_id = bus_id
        self.correct = 0
        self.correct_right = 0

    def addStat(self, if_correct):
        global TotalCorrect
        global TotalCorrectRight
        TotalCorrect += 1
        self.correct += 1

        if if_correct:
            TotalCorrectRight += 1
            self.correct_right += 1

    def correctRate(self):
        if self.correct != 0:
            return float(self.correct_right) / float(self.correct)
        else:
            return 0

    def report(self):
        print(self.bus_id, ' 修正个数:', self.correct, '正确数:', self.correct_right, '准确率:', self.correctRate())

class OneFileTest:

    def __init__(self, sample_file, cmp_file):
        #总共判出多少个点
        self.total_correct = 0
        #总共判对多少个点
        self.total_correct_right = 0
        #总共判错多少个
        self.total_correct_wrong = 0
        #少判出多少个
        self.total_correct_mis = 0
        #准报站算法总共提供的意见数
        self.total_offline_assist_count = 0
        #没有使用准报站算法gps点数
        self.total_offline_assist_count_not_in_use = 0
        #准报站算法提供的意见准确率
        self.total_offline_assist_correct = 0

        self.sample_file = sample_file
        self.cmp_file = cmp_file


    def ReportTotalStat(self):
        if (self.total_correct == 0):
            self.total_correct = 1
        print(self.sample_file, " ReportTotalStat. ")
        print('识别总数:', self.total_correct, '正确数:', self.total_correct_right, '错误数:',self.total_correct_wrong, 'miss数:', self.total_correct_mis, '准确率:', float(self.total_correct_right) / float(self.total_correct))
        if (self.total_offline_assist_count == 0):
            self.total_offline_assist_count = 1
        print('准报站算法总gps点数:', self.total_offline_assist_count, '没有使用的个数:', self.total_offline_assist_count_not_in_use, '准确率:', float(self.total_offline_assist_correct)/float(self.total_offline_assist_count))

    def Judge(self, sample_line, cmp_line):
        sample_line_tags = sample_line.split(',')
        count = sample_line.count(',') + 1
        cmp_line_tags = cmp_line.split(',')

        if int(sample_line_tags[0]) == 1:
            self.total_correct += 1
            if int(cmp_line_tags[0]) == 0:
                self.total_correct_wrong += 1
            else:
                self.total_correct_right += 1

        if int(sample_line_tags[0]) != 1 and int(cmp_line_tags[0]) != 0:
            self.total_correct_mis += 1

        #统计准报站算法的使用率和准确率
        if count > 17 and sample_line_tags[17] != '-':
            self.total_offline_assist_count += 1
            if int(sample_line_tags[0]) == 0:
                self.total_offline_assist_count_not_in_use += 1
            if (int(cmp_line_tags[0]) != 0) and sample_line_tags[17] == cmp_line_tags[2]:
                self.total_offline_assist_correct += 1

    def CountAccuracy(self):
        print('开始统计:')
        sample_file = codecs.open(self.sample_file, 'r', 'utf-8')
        cmp_file = codecs.open(self.cmp_file, 'r', 'utf-8')

        sample_line = sample_file.readline()
        cmp_line = cmp_file.readline()

        while sample_line and cmp_line:
            self.Judge(sample_line, cmp_line)
            sample_line = sample_file.readline()
            cmp_line = cmp_file.readline()

        self.ReportTotalStat()
