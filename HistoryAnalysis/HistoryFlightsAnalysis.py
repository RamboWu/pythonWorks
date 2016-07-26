#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
import datetime

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from Util.Tools import FileHelper

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
        pass

    def readCity(self, city_dir):
        list = os.listdir(city_dir)  #列出目录下的所有文件和目录
        for line in list:
            filepath = os.path.join(city_dir,line)
            if os.path.isdir(filepath):  #如果filepath是目录，则再列出该目录下的所有文件
                self.readOneDayFlight(filepath, line)

    def readOneDayFlight(self, dir, title):
        flight_file = os.path.join(dir, 'single.log')
        if os.path.exists(flight_file):
            bus_relations = getBusRelations(flight_file)
            print(bus_relations,'\n')
