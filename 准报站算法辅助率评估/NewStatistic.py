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

file_reader = OnlineOfflineGPSFileReader.OnlineOfflineGPSFileReader(BusPoint.WENCAN_MODE)

@file_reader.RegisterCount
def Count(bus_point, off_bus_point):
    OnlineResCount.Count(bus_point, off_bus_point)
    OnlineResAssistCount.Count(bus_point, off_bus_point)
    OfflineResHitCount.Count(bus_point,off_bus_point)

def outputBuses():
    pass

nodetect_buses = []
wrong_buses = []
missafter_buses = []

@file_reader.RegisterReport
def Report():
    global missafter_buses, nodetect_buses, wrong_buses
    file_name = os.path.join('log','Statistic'+DateHelp.getTime())
    missafter_buses = OnlineResCount.Report(file_name)
    OnlineResAssistCount.Report(file_name)
    nodetect_buses, wrong_buses = OfflineResHitCount.Report(file_name)

def StartStatistic(sample_file, cmp_file):
    file_reader.startCount(sample_file=sample_file,cmp_file=cmp_file)
    file_reader.Report()
    print(missafter_buses, nodetect_buses, wrong_buses)

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
