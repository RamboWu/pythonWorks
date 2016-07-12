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



file_dir = ''
NoDetectBusSet = set()
WrongBusSet = set()
MissAfterBusSet = set()

def outputBuses(input_file, buses, output, index = 3):
    keys = ','.join(buses)
    PickUp.PickUp.run(input_file, keys, output, index)

def outputSingleBus(input_file, buses, output, index = 3, postfix = '.csv'):
    for bus in buses:
        haha = []
        haha.append(bus)
        outputBuses(input_file, haha, os.path.join(output,bus+postfix), index)

def outputDetail(sample_file, cmp_file):
    outputBuses(sample_file, NoDetectBusSet | WrongBusSet | MissAfterBusSet, os.path.join(file_dir,'total.csv'))
    outputBuses(cmp_file, NoDetectBusSet | WrongBusSet | MissAfterBusSet, os.path.join(file_dir,'sorted.cmp'), 1)
    outputBuses(os.path.join(file_dir,'total.csv'),NoDetectBusSet,os.path.join(file_dir,'nodetect.csv'))
    outputBuses(os.path.join(file_dir,'total.csv'),WrongBusSet,os.path.join(file_dir,'wrong.csv'))
    outputBuses(os.path.join(file_dir,'total.csv'),MissAfterBusSet,os.path.join(file_dir,'missafter.csv'))
    outputSingleBus(os.path.join(file_dir,'total.csv'), NoDetectBusSet, os.path.join(file_dir, 'nodetect'))
    outputSingleBus(os.path.join(file_dir,'total.csv'), WrongBusSet, os.path.join(file_dir, 'wrong'))
    outputSingleBus(os.path.join(file_dir,'total.csv'), MissAfterBusSet, os.path.join(file_dir, 'missafter'))
    outputSingleBus(os.path.join(file_dir,'sorted.cmp'),NoDetectBusSet,os.path.join(file_dir,'nodetect'), 1, '.csv.cmp')
    outputSingleBus(os.path.join(file_dir,'sorted.cmp'),WrongBusSet,os.path.join(file_dir,'wrong'), 1, '.csv.cmp')
    outputSingleBus(os.path.join(file_dir,'sorted.cmp'),MissAfterBusSet,os.path.join(file_dir,'missafter'), 1, '.csv.cmp')

@file_reader.RegisterReport
def Report():
    global NoDetectBusSet, WrongBusSet, MissAfterBusSet
    missafter_buses = OnlineResCount.Report(file_dir)
    OnlineResAssistCount.Report(file_dir)
    nodetect_buses, wrong_buses = OfflineResHitCount.Report(file_dir)
    NoDetectBusSet = set(nodetect_buses)
    WrongBusSet = set(wrong_buses)
    MissAfterBusSet = set(missafter_buses)

def StartStatistic(sorted_file, cmp_file, original = None):
    global file_dir
    file_dir = os.path.join('log','Statistic'+DateHelp.getTime())
    file_reader.startCount(sample_file=sorted_file,cmp_file=cmp_file)
    file_reader.Report()
    if original == None:
        outputDetail(sorted_file, cmp_file)
    else:
        outputDetail(original, cmp_file)

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
