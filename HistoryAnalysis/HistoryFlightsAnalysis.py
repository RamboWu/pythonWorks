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

def getBusRelations(bus_relation_file):

    bus_file = codecs.open(bus_relation_file, 'r', 'utf-8')
    line = bus_file.readline()

    bus_relations = dict()

    while line:
        line = line.strip()
        tags = line.split(',')
        bus_relations[tags[0]] = tags[1]
        line = bus_file.readline()

    bus_file.close()

    return bus_relations

class HistoryFlightsAnalysis:
    def __init__(self):
        self.BusMap = dict()
        self.dates = []
        self.BusCommonLine = dict()
        pass

    def readCity(self, city_dir):
        list = os.listdir(city_dir)  #列出目录下的所有文件和目录
        for line in list:
            filepath = os.path.join(city_dir,line)
            if os.path.isdir(filepath):  #如果filepath是目录，则再列出该目录下的所有文件
                self.readOneDayFlight(filepath, line)
                self.dates.append(line)

        self.dates = sorted(self.dates, key=lambda d:d[0], reverse = False)

        LogHelper.printFile('log/tongji.log', 'w', self.getString(self.BusMap.keys()))
        self.analysis(city_dir)

    def analysisCommonLine(self):
        for bus_id in self.BusMap.keys():
            bus_line_count = dict()
            for date in self.BusMap[bus_id].keys():
                if self.BusMap[bus_id][date] != '':
                    if not self.BusMap[bus_id][date] in bus_line_count.keys():
                        bus_line_count[self.BusMap[bus_id][date]] = 0
                    bus_line_count[self.BusMap[bus_id][date]] += 1

            sorted_count = sorted(bus_line_count.items(), key=lambda d:d[1], reverse = True)
            total = sum(x[1] for x in sorted_count)
            if float(sorted_count[0][1]) / total > 0.6:
                self.BusCommonLine[bus_id] = sorted_count[0][0]

        print('CommonLinePercent:', MathHelper.percentToString(len(self.BusCommonLine.keys()),len(self.BusMap.keys())))

    def analysisDiffCount(self):
        diff_buses = []
        for bus_id in self.BusMap.keys():
            same = True
            bus_line = ''
            for date in self.BusMap[bus_id].keys():
                if self.BusMap[bus_id][date] != '':
                    if bus_line == '':
                        bus_line = self.BusMap[bus_id][date]
                    elif self.BusMap[bus_id][date] != bus_line:
                        same = False
                        break

            if not same:
                diff_buses.append(bus_id)

        print('DiffCountPercent:', MathHelper.percentToString(len(diff_buses),len(self.BusMap.keys())))
        #print(self.getString(diff_buses))

    def analysisContinueDiff(self):
        continue_diff_count = dict()
        #只遍历具有CommonLine的公交车辆
        for bus_id in self.BusCommonLine.keys():
            continue_diff = 0
            sorted_items = sorted(self.BusMap[bus_id].keys(), key=lambda d:d, reverse = False)
            for date in sorted_items:
                if self.BusMap[bus_id][date] != '':
                    if self.BusMap[bus_id][date] != self.BusCommonLine[bus_id]:
                        continue_diff += 1
                    else:
                        if continue_diff > 0:
                            if not continue_diff in continue_diff_count.keys():
                                continue_diff_count[continue_diff] = 0
                            continue_diff_count[continue_diff] += 1
                            if continue_diff >= 7:
                                print(bus_id, self.BusCommonLine[bus_id])
                        continue_diff = 0


        total = sum(x[1] for x in continue_diff_count.items())
        print(continue_diff_count)
        print(total)

    def analysisTodayYesterdaySameLineFrontCount(self, city_dir):
        line_front_similar_file = os.path.join(city_dir, "LineFrontSimilar.csv")
        total_diff = 0
        if not os.path.exists(line_front_similar_file):
            print(line_front_similar_file + ' dont exists!')
            return

        analysis_helper = OriginalWrongAnalysisHelper(line_front_similar_file)
        for bus_id in self.BusCommonLine.keys():
            sorted_items = sorted(self.BusMap[bus_id].keys(), key=lambda d:d, reverse = False)
            yesterday = None
            for date in sorted_items:
                if yesterday == None:
                    yesterday = self.BusMap[bus_id][date]
                else:
                    if yesterday != self.BusMap[bus_id][date]:
                        total_diff += 1
                    analysis_helper.analysisSameLineFrontCountWithBusId(bus_id, yesterday, self.BusMap[bus_id][date], True)
                    yesterday = self.BusMap[bus_id][date]

        print('total_diff', total_diff)
        analysis_helper.report()

    def analysis(self, city_dir):
        self.analysisDiffCount()
        self.analysisCommonLine()
        self.analysisContinueDiff()
        self.analysisTodayYesterdaySameLineFrontCount(city_dir)


    def getString(self, buses):
        mix = PrettyTable()
        mix.field_names = ["Bus_ID"] + self.dates

        for key in buses:
            items = []
            for date in self.dates:
                if date in self.BusMap[key].keys():
                    items.append(self.BusMap[key][date])
                else:
                    items.append('')
            mix.add_row([key] + items)

        return mix.get_string()


    def readOneDayFlight(self, dir, title):
        flight_file = os.path.join(dir, 'single.log')
        if os.path.exists(flight_file):
            bus_relations = getBusRelations(flight_file)
            for key in bus_relations.keys():
                if not key in self.BusMap.keys():
                    self.BusMap[key] = dict()
                self.BusMap[key][title] = bus_relations[key]
