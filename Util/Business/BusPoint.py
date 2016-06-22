#  -*- coding: utf-8 -*-
#!/usr/bin/python
import os, subprocess, sys, codecs

class BusPoint:
    '''
    classdocs
    '''

    def __init__(self, line):

        self.bus_id = ""
        self.gps_time = ""
        self.assist_line_id = "-"
        self.is_rec = False
        self.line_id = ""
        #在准报站算法中是否被识别
        self.is_assist_real_dectected = False
        self.parse(line)

        #print('是否被准报站算法识别:', self.is_assist_real_dectected)

    def parse(self, line):
        line = line.strip()
        line_tags = line.split(',')
        count = line.count(',') + 1

        self.bus_id = line_tags[3]
        self.gps_time = line_tags[13]
        if count > 18:
            self.assist_line_id = line_tags[18]
        self.is_rec = line_tags[0] == '1'
        self.line_id = line_tags[4]
        self.is_assist_real_dectected = line_tags[1] == 'D'

class OffLineBusPoint:
    '''
    classdocs
    '''

    def __init__(self, line):

        self.bus_id = ""
        self.gps_time = ""
        self.is_rec = False
        self.line_id = ""
        self.parse(line)

    def parse(self, line):
        line = line.strip()
        line_tags = line.split(',')

        self.bus_id = line_tags[3]
        self.gps_time = line_tags[12]
        self.is_rec = line_tags[0] == '1'
        self.line_id = line_tags[4]

class WenCanOffLinePoint:
    def __init__(self, line):

        self.bus_id = ""
        self.gps_time = ""
        self.is_rec = False
        self.line_id = ""
        self.dir = 0
        self.station = 0
        self.parse(line)

    def parse(self, line):
        line = line.strip()
        line_tags = line.split(',')

        self.bus_id = line_tags[1]
        self.gps_time = line_tags[9]
        self.is_rec = line_tags[0] == '1'
        self.line_id = line_tags[2]
        self.dir = int(line_tags[3])
        self.station = int(line_tags[4])
