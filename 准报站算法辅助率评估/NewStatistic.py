#  -*- coding: utf-8 -*-
#!/usr/bin/python

#NewStatistic.py
import codecs, sys, getopt

sys.path.append("..")
from Util.Business import OnlineOfflineGPSFileReader

file_reader = OnlineOfflineGPSFileReader.OnlineOfflineGPSFileReader()

@file_reader.RegisterCount
def CountOffline(bus_point, off_bus_point):
    print(bus_point, off_bus_point)

if  __name__ ==  '__main__':
    file_reader.startCount(sample_file='test/matching.log.sort-100000',cmp_file='test/matching.log.sort.cmp-100000')
