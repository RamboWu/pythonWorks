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
from Util.Business import CountOriginalWrong
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
    CountOriginalWrong.Count(bus_point,off_bus_point)

file_dir = ''
NoDetectBusSet = set()
WrongBusSet = set()
MissAfterBusSet = set()
DirWrongBusSet = set()
OnlineWrongBusSet = set()
OriginalDiffWrongBusSet = set()

def outputBuses(input_file, buses, output, index = 3, single_dir=None, postfix='.csv', noTotalFile=False):
    keys = ','.join(buses)
    PickUp.PickUp.run(input_file, keys, output, index, single_dir, postfix, noTotalFile)

def outputSingleBus(input_file, buses, output, index = 3, postfix = '.csv'):
    for bus in buses:
        haha = []
        haha.append(bus)
        outputBuses(input_file, haha, os.path.join(output,bus+postfix), index)

def outputDetail(sample_file, cmp_file):
    TotalBusSet = NoDetectBusSet | WrongBusSet | MissAfterBusSet | DirWrongBusSet | OnlineWrongBusSet | OriginalDiffWrongBusSet
    outputBuses(sample_file, TotalBusSet, os.path.join(file_dir,'total.csv'))
    outputBuses(os.path.join(file_dir,'total.csv'), NoDetectBusSet, os.path.join(file_dir, 'nodetect.csv'), single_dir='NoDetect')
    outputBuses(os.path.join(file_dir,'total.csv'), WrongBusSet, os.path.join(file_dir, 'wrong.csv'), single_dir='Wrong')
    outputBuses(os.path.join(file_dir,'total.csv'), MissAfterBusSet, os.path.join(file_dir, 'missafter.csv'), single_dir='Miss')
    outputBuses(os.path.join(file_dir,'total.csv'), DirWrongBusSet, os.path.join(file_dir, 'dirwrong.csv'), single_dir='DirWrong')
    outputBuses(os.path.join(file_dir,'total.csv'), OnlineWrongBusSet, os.path.join(file_dir, 'onlinewrong.csv'), single_dir='OnlineWrong')
    outputBuses(os.path.join(file_dir,'total.csv'), OriginalDiffWrongBusSet, os.path.join(file_dir, 'original_diff_wrong.csv'), single_dir='OriginalDiffWrong')

    outputBuses(cmp_file, TotalBusSet, os.path.join(file_dir,'sorted.cmp'), 1)
    outputBuses(os.path.join(file_dir,'sorted.cmp'),NoDetectBusSet,os.path.join(file_dir,'nodetect.csv.cmp'), 1, single_dir='NoDetect', postfix='.csv.cmp', noTotalFile=True)
    outputBuses(os.path.join(file_dir,'sorted.cmp'),WrongBusSet,os.path.join(file_dir,'wrong.csv.cmp'), 1, single_dir='Wrong', postfix='.csv.cmp', noTotalFile=True)
    outputBuses(os.path.join(file_dir,'sorted.cmp'),MissAfterBusSet,os.path.join(file_dir,'missafter.csv.cmp'), 1, single_dir='Miss', postfix='.csv.cmp', noTotalFile=True)
    outputBuses(os.path.join(file_dir,'sorted.cmp'),DirWrongBusSet,os.path.join(file_dir,'dirwrong.csv.cmp'), 1, single_dir='DirWrong', postfix='.csv.cmp', noTotalFile=True)
    outputBuses(os.path.join(file_dir,'sorted.cmp'),OnlineWrongBusSet,os.path.join(file_dir,'onlinewrong.csv.cmp'), 1, single_dir='OnlineWrong', postfix='.csv.cmp', noTotalFile=True)
    outputBuses(os.path.join(file_dir,'sorted.cmp'),OriginalDiffWrongBusSet,os.path.join(file_dir,'original_diff_wrong.csv.cmp'), 1, single_dir='OriginalDiffWrong', postfix='.csv.cmp', noTotalFile=True)
    os.remove(os.path.join(file_dir,'sorted.cmp'))

@file_reader.RegisterReport
def Report():
    global NoDetectBusSet, WrongBusSet, MissAfterBusSet, DirWrongBusSet, OnlineWrongBusSet, OriginalDiffWrongBusSet
    missafter_buses, dirwrong_buses, onlinewrong_buses = OnlineResCount.Report(file_dir)
    OnlineResAssistCount.Report(file_dir)
    nodetect_buses, wrong_buses = OfflineResHitCount.Report(file_dir)
    original_diff_wrong_buses = CountOriginalWrong.Report(file_dir)
    NoDetectBusSet = set(nodetect_buses)
    WrongBusSet = set(wrong_buses)
    MissAfterBusSet = set(missafter_buses)
    DirWrongBusSet = set(dirwrong_buses)
    OnlineWrongBusSet = set(onlinewrong_buses)
    OriginalDiffWrongBusSet = set(original_diff_wrong_buses)

def StartStatistic(sorted_file, cmp_file, original = None):
    global file_dir
    file_dir = os.path.join('log','Statistic'+DateHelp.getTime())
    file_reader.startCount(sample_file_name=sorted_file,cmp_file_name=cmp_file)
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
