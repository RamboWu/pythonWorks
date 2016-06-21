#  -*- coding: utf-8 -*-
#!/usr/bin/python

#NewStatistic.py
import codecs, sys, getopt

sys.path.append("..")
from Util.Business import OnlineOfflineGPSFileReader
from Util.Business import OnlineResCount

file_reader = OnlineOfflineGPSFileReader.OnlineOfflineGPSFileReader()

@file_reader.RegisterCount
def Count(bus_point, off_bus_point):
    OnlineResCount.Count(bus_point, off_bus_point)

if  __name__ ==  '__main__':
    file_reader.startCount(sample_file='test/matching.log.sort-100000',cmp_file='test/matching.log.sort.cmp-100000')
