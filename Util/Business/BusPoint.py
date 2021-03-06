#  -*- coding: utf-8 -*-
#!/usr/bin/python
import os, subprocess, sys, codecs

LAODA_MODE = 0
WENCAN_MODE = 1

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
        self.first_bit = ''
        self.dir = ''
        self.original_line_id = ''
        self.recv_time = ''
        self.parse(line)

        #print('是否被准报站算法识别:', self.is_assist_real_dectected)

    def parse(self, line):
        line = line.strip()
        line_tags = line.split(',')
        count = line.count(',') + 1

        self.bus_id = line_tags[3]
        self.gps_time = line_tags[13]
        self.recv_time = line_tags[14]
        if count > 18:
            self.assist_line_id = line_tags[18]
        self.first_bit = line_tags[0]
        self.is_rec = line_tags[0] == '1'
        self.line_id = line_tags[4]
        self.is_assist_real_dectected = line_tags[1] == 'D'
        self.zhunbaozhan_line_id = line_tags[2]
        self.dir = line_tags[6]
        self.original_line_id = line_tags[12]

class OffLineBusPoint:

    '''
    classdocs
    '''

    def __init__(self, line, mode = LAODA_MODE):

        self.bus_id = ""
        self.gps_time = ""
        self.is_rec = False
        self.line_id = ""
        self.dir = ''
        self.station = 0
        self.first_bit = ''
        self.recv_time = ''
        if mode == LAODA_MODE:
            self.parseLaoDa(line)
        else:
            self.parseWenCan(line)

    def parseLaoDa(self, line):
        line = line.strip()
        line_tags = line.split(',')

        self.bus_id = line_tags[3]
        self.gps_time = line_tags[12]
        self.recv_time = line_tags[13]
        self.is_rec = line_tags[0] == '1'
        self.first_bit = line_tags[0]
        self.line_id = line_tags[4]
        self.dir = line_tags[6]
        self.station = int(line_tags[7])

    def parseWenCan(self, line):
        line = line.strip()
        line_tags = line.split(',')

        self.bus_id = line_tags[1]
        self.gps_time = line_tags[9]
        self.recv_time = line_tags[10]
        self.is_rec = line_tags[0] == '1'
        self.first_bit = line_tags[0]
        self.line_id = line_tags[2]
        self.dir = line_tags[3]
        self.station = int(line_tags[4])

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
