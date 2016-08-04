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

from OriginalWrongAnalysisHelper import OriginalWrongAnalysisHelper

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

class HistoryOriginalWrongAnalysis:
    def __init__(self):
        self.BusMap = dict()
        self.analysis_helper = None

    def readCity(self, city_dir):

        line_front_similar_file = os.path.join(city_dir, "LineFrontSimilar.csv")
        if not os.path.exists(line_front_similar_file):
            print(line_front_similar_file + ' dont exists!')
            return

        self.analysis_helper = OriginalWrongAnalysisHelper(line_front_similar_file)

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

    def readOneDayFlight(self, dir, title):
        flight_file = os.path.join(dir, 'busline_busLineAll.log')
        if os.path.exists(flight_file):
            bus_relations = getBusRelations(flight_file)
            for key in bus_relations.keys():
                if not key in self.BusMap.keys():
                    self.BusMap[key] = OriginalWrongCount()
                same_count, diff_count = \
                    self.analysis_helper.analysisSameLineFrontCount(bus_relations[key].real_line_id, bus_relations[key].original_line_id)
                self.BusMap[key].same_count += same_count
                self.BusMap[key].diff_count += diff_count
