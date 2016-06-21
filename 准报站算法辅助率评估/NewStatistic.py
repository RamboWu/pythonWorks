#  -*- coding: utf-8 -*-
#!/usr/bin/python

#NewStatistic.py
import codecs, sys, getopt

sys.path.append("..")
from Util.Business import OnlineOfflineGPSFileReader
from Util.Business import OnlineResCount
from Util.Tools import LogHelper

logger = LogHelper.makeConsoleAndFileLogger('NewStatistic')
logger.info('BusState Log init finish!')
OnlineResCount.logger = logger

file_reader = OnlineOfflineGPSFileReader.OnlineOfflineGPSFileReader()

@file_reader.RegisterCount
def Count(bus_point, off_bus_point):
    OnlineResCount.Count(bus_point, off_bus_point)

@file_reader.RegisterReport
def Report():
    OnlineResCount.Report()

def StartStatistic(sample_file, cmp_file):
    file_reader.startCount(sample_file=sample_file,cmp_file=cmp_file)
    file_reader.Report()

if  __name__ ==  '__main__':
    file_reader.startCount(sample_file='test/matching.log.sort-100000',cmp_file='test/matching.log.sort.cmp-100000')
    file_reader.Report()
