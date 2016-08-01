#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
import datetime
from prettytable import PrettyTable

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from Util.Tools import FileHelper
from Util.Tools import LogHelper

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
        pass

    def readCity(self, city_dir):
        list = os.listdir(city_dir)  #列出目录下的所有文件和目录
        for line in list:
            filepath = os.path.join(city_dir,line)
            if os.path.isdir(filepath):  #如果filepath是目录，则再列出该目录下的所有文件
                self.readOneDayFlight(filepath, line)
                self.dates.append(line)

        self.dates = sorted(self.dates, key=lambda d:d[0], reverse = False)
        self.prettyPrint()

    def prettyPrint(self):
        mix = PrettyTable()
        mix.field_names = ["Bus_ID"] + self.dates

        for key in self.BusMap.keys():
            items = []
            for date in self.dates:
                if date in self.BusMap[key].keys():
                    items.append(self.BusMap[key][date])
                else:
                    items.append('')
            mix.add_row([key] + items)

        LogHelper.printFile('log/tongji.log','w',mix.get_string())
        print(mix)

    def readOneDayFlight(self, dir, title):
        flight_file = os.path.join(dir, 'single.log')
        if os.path.exists(flight_file):
            bus_relations = getBusRelations(flight_file)
            for key in bus_relations.keys():
                if not key in self.BusMap.keys():
                    self.BusMap[key] = dict()
                self.BusMap[key][title] = bus_relations[key]
