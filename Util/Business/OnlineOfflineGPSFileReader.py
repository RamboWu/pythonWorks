#  -*- coding: utf-8 -*-
#!/usr/bin/python

#DoubleFileReader.py
import codecs, sys, getopt

from Util.Business import BusPoint

class OnlineOfflineGPSFileReader:
    def __init__(self):
        self.count_func_set = []
        pass

    def RegisterCount(self, f):
        self.count_func_set.append(f)
        return f

    def CountEach(self, bus_point, off_bus_point):
        for f in self.count_func_set:
            f(bus_point, off_bus_point)

    def Verify(self, sample_line, cmp_line, lineno):
        if (sample_line.strip() == ""):
            return -1, 0, 0
        if (cmp_line.strip() == ""):
            return -2, 0, 0

        bus_point = BusPoint.BusPoint(sample_line)
        off_bus_point = BusPoint.OffLineBusPoint(cmp_line)

        if bus_point.bus_id < off_bus_point.bus_id:
            return -1, 0, 0
        if bus_point.bus_id > off_bus_point.bus_id:
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
            res, bus_point, off_bus_point= self.Verify(sample_line, cmp_line, lineno)
            if res == 0:
                lineno += 1
                self.CountEach(bus_point, off_bus_point)
                sample_line = sample_file.readline()
                cmp_line = cmp_file.readline()
            elif res == -1:
                lineno += 1
                sample_line = sample_file.readline()
            elif res == -2:
                cmp_line = cmp_file.readline()
