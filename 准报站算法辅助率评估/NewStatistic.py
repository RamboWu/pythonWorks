#  -*- coding: utf-8 -*-
#!/usr/bin/python

#NewStatistic.py
import codecs, sys, getopt, os, subprocess

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager
from Util.Business import OnlineOfflineGPSFileReader
from Util.Business import OnlineResCount
from Util.Business import OnlineResAssistCount
from Util.Business import OfflineResHitCount
from Util.Business import BusPoint
from Util.Tools import LogHelper
from Util.Tools import DateHelp

import PickUp.PickUp

file_reader = OnlineOfflineGPSFileReader.OnlineOfflineGPSFileReader(BusPoint.WENCAN_MODE)

@file_reader.RegisterCount
def Count(bus_point, off_bus_point):
    OnlineResCount.Count(bus_point, off_bus_point)
    OnlineResAssistCount.Count(bus_point, off_bus_point)
    OfflineResHitCount.Count(bus_point,off_bus_point)

def outputBuses(input_file, buses, output, index = 3):
    keys = ','.join(buses)
    PickUp.PickUp.run(input_file, keys, output, index)

file_dir = ''
nodetect_buses = []
wrong_buses = []
missafter_buses = []

@file_reader.RegisterReport
def Report():
    global missafter_buses, nodetect_buses, wrong_buses
    missafter_buses = OnlineResCount.Report(file_dir)
    OnlineResAssistCount.Report(file_dir)
    nodetect_buses, wrong_buses = OfflineResHitCount.Report(file_dir)

def StartStatistic(sample_file, cmp_file):
    global file_dir
    file_dir = os.path.join('log','Statistic'+DateHelp.getTime())

    file_reader.startCount(sample_file=sample_file,cmp_file=cmp_file)
    file_reader.Report()
    outputBuses(sample_file,nodetect_buses+wrong_buses+missafter_buses,os.path.join(file_dir,'total.csv'))
    outputBuses(cmp_file,nodetect_buses+wrong_buses+missafter_buses,os.path.join(file_dir,'total.csv.cmp'), 1)

manager = Manager()
@manager.option('-i', '--input', dest='input_file', required=True)
@manager.option('-j', '--judge', dest='judge_file', required=True)
def run(input_file=None, judge_file = None):
    StartStatistic(input_file, judge_file)

@manager.command
def test():
    command_line = 'python3 NewStatistic.py run -i test/matching.log.sort-100000 -j test/matching.log.sort.cmp-100000'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

if  __name__ ==  '__main__':
    manager.run()
