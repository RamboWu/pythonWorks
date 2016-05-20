#  -*- coding: utf-8 -*-
#!/usr/bin/python

#BusStat.py
import codecs
'''
Created on 2016-05-20

@author: RamboWu
'''
#总的矫正数量
TotalCorrect = 0
#总的对的数量
TotalCorrectRight = 0

class BusStat:
    '''
    classdocs
    '''

    def __init__(self,bus_id):

        self.bus_id = bus_id
        self.correct = 0
        self.correct_right = 0

    def addStat(if_correct):
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


BusMap = dict()

def ReportTotalStat():
    global TotalCorrect
    global TotalCorrectRight
    if (TotalCorrect == 0):
        TotalCorrect = 1
    print('修正个数:', TotalCorrect, '正确数:', TotalCorrectRight, '准确率:', float(TotalCorrectRight) / float(TotalCorrect))

    for key in BusMap.keys():
        BusMap[key].report()

def Judge(off_line, judge_line):
    off_line_tags = off_line.split(',')
    judge_tags = judge_line.split(',')
    if off_line_tags[3] in BusMap.keys():
        bus_stat = BusMap.get(off_line_tags[3])
    else:
        bus_stat = BusStat(off_line_tags[3])
        BusMap[off_line_tags[3]] = bus_stat

    if (int(off_line_tags[0]) == 2):
        bus_stat.addStat(int(judge_tags[0]) == 1)

def CountAccuracy(offline_result_name, real_offline_result_name):
    print('开始统计:')
    offline_file = codecs.open(offline_result_name, 'r', 'utf-8')
    judgement_file = codecs.open(real_offline_result_name, 'r', 'utf-8')

    off_line = offline_file.readline()
    judge_line = judgement_file.readline()

    while off_line and judge_line:
        Judge(off_line, judge_line)
        off_line = offline_file.readline()
        judge_line = judgement_file.readline()

    ReportTotalStat()
