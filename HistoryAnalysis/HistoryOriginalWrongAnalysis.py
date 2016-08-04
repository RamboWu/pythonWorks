#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
import datetime
import functools
from prettytable import PrettyTable

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from Util.Tools import FileHelper
from Util.Tools import LogHelper
from Util.Tools import MathHelper

class BusLineInfo:
    def __init__(self):
        self.original_line_id = ''
        self.real_line_id = ''

class OriginalWrongCount:
    def __init__(self):
        self.same_count = 0
        self.diff_count = 0

def getBusRelations(bus_relation_file):

    bus_file = codecs.open(bus_relation_file, 'r', 'utf-8')
    line = bus_file.readline()

    bus_relations = dict()

    while line:
        line = line.strip()
        tags = line.split(',')
        bus_relations[tags[1]] = BusLineInfo()
        bus_relations[tags[1]].original_line_id = tags[2]
        bus_relations[tags[1]].real_line_id = tags[3]
        line = bus_file.readline()

    bus_file.close()

    return bus_relations

def getLineFrontSimilar(file_):
    bus_file = codecs.open(file_, 'r', 'utf-8')
    line = bus_file.readline()

    relations = dict()

    while line:
        line = line.strip()
        tags = line.split(':')
        relations[tags[0]] = set()
        similar_tags = tags[1].split(',')
        for similar_line in similar_tags:
            relations[tags[0]].add(similar_line)
        line = bus_file.readline()

    bus_file.close()

    '''
    for key in relations.keys():
        tmp = key + ":"
        for line in relations[key]:
            tmp += line + ","
        print(tmp)
    '''

    return relations

class HistoryOriginalWrongAnalysis:
    def __init__(self):
        self.BusMap = dict()
        self.line_front_similar = dict()

    def readCity(self, city_dir):
        line_front_similar_file = os.path.join(city_dir, "LineFrontSimilar.csv")
        if not os.path.exists(line_front_similar_file):
            print(line_front_similar_file + ' dont exists!')
            return

        self.line_front_similar = getLineFrontSimilar(line_front_similar_file)

        list = os.listdir(city_dir)  #列出目录下的所有文件和目录
        for line in list:
            filepath = os.path.join(city_dir,line)
            if os.path.isdir(filepath):  #如果filepath是目录，则再列出该目录下的所有文件
                self.readOneDayFlight(filepath, line)

        self.report()

    def report(self):
        total_same = 0
        total_diff = 0
        for bus_id in self.BusMap.keys():
            total_same += self.BusMap[bus_id].same_count
            total_diff += self.BusMap[bus_id].diff_count

        print('same: %s, diff:%s, samePer:%s'%(total_same, total_diff, MathHelper.percentToString(total_same, total_same + total_diff)))

    def analysisSameLineFrontCount(self, one_line_id, other_line_id):
        if one_line_id == other_line_id:
            return 0, 0
        else:
            if not one_line_id in self.line_front_similar.keys():
                #print(today_line.real_line_id, today_line.original_line_id, 0 , 1)
                return 0, 1
            if not other_line_id in self.line_front_similar.keys():
                #print(today_line.real_line_id, today_line.original_line_id, 0 , 1)
                return 0, 1
            if not other_line_id in self.line_front_similar[one_line_id]:
                #print(today_line.real_line_id, today_line.original_line_id, 0 , 1)
                return 0, 1
            #print(today_line.real_line_id, today_line.original_line_id, 1, 0)
            return 1, 0

    def readOneDayFlight(self, dir, title):
        flight_file = os.path.join(dir, 'busline_busLineAll.log')
        if os.path.exists(flight_file):
            bus_relations = getBusRelations(flight_file)
            for key in bus_relations.keys():
                if not key in self.BusMap.keys():
                    self.BusMap[key] = OriginalWrongCount()
                same_count, diff_count = self.analysisSameLineFrontCount(bus_relations[key].real_line_id, bus_relations[key].original_line_id)
                self.BusMap[key].same_count += same_count
                self.BusMap[key].diff_count += diff_count
