#  -*- coding: utf-8 -*-
#!/usr/bin/python

#DoubleFileReader.py
import codecs, sys, getopt

from Util.Business import BusPoint

class OnlineOfflineGPSFileReader:
    def __init__(self, offline_mode = BusPoint.LAODA_MODE):
        self.__count_func_set = []
        self.__report_func_set = []
        self.__offline_mode = offline_mode
        pass

    def RegisterCount(self, f):
        self.__count_func_set.append(f)
        return f

    def RegisterReport(self, f):
        self.__report_func_set.append(f)
        return f

    def Report(self):
        for f in self.__report_func_set:
            f();

    def __CountEach(self, bus_point, off_bus_point):
        for f in self.__count_func_set:
            f(bus_point, off_bus_point)

    def __Verify(self, sample_line, cmp_line, lineno):
        if (sample_line.strip() == ""):
            return -1, 0, 0
        if (cmp_line.strip() == ""):
            return -2, 0, 0

        bus_point = BusPoint.BusPoint(sample_line)
        off_bus_point = BusPoint.OffLineBusPoint(cmp_line, self.__offline_mode)

        if bus_point.bus_id < off_bus_point.bus_id:
            return -1, 0, 0
        if bus_point.bus_id > off_bus_point.bus_id:
            return -2, 0, 0

        if bus_point.gps_time < off_bus_point.gps_time:
            #print("-1 lineNo:%s sample_line: %s; cmp_line: %s. "% (lineno, sample_line, cmp_line))
            return -1, 0, 0
        if bus_point.gps_time > off_bus_point.gps_time:
            #print("-2 lineNo:%s sample_line: %s; cmp_line: %s. "% (lineno, sample_line, cmp_line))
            return -2, 0, 0

        if bus_point.bus_id != off_bus_point.bus_id or bus_point.gps_time != off_bus_point.gps_time:
            print("lineNo:%s sample_line: %s; cmp_line: %s. "% (lineno, sample_line, cmp_line))
            sys.exit(0)

        return 0, bus_point, off_bus_point

    def startCount(self, sample_file, cmp_file):

        sample_file = codecs.open(sample_file, 'r', 'utf-8')
        cmp_file = codecs.open(cmp_file, 'r', 'utf-8')

        sample_line = sample_file.readline()
        cmp_line = cmp_file.readline()

        lineno = 0
        while sample_line and cmp_line:
            res, bus_point, off_bus_point= self.__Verify(sample_line, cmp_line, lineno)
            if res == 0:
                lineno += 1
                self.__CountEach(bus_point, off_bus_point)
                sample_line = sample_file.readline()
                cmp_line = cmp_file.readline()
            elif res == -1:
                lineno += 1
                sample_line = sample_file.readline()
            elif res == -2:
                cmp_line = cmp_file.readline()
