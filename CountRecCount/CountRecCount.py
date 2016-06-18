#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os, http.client, urllib.request, urllib.parse
import http.cookiejar
import time
import logging
import datetime
import ssl
import inspect
import re

def getTime():
    ISOTIMEFORMAT = '%Y-%m-%d-%H-%M'
    return time.strftime( ISOTIMEFORMAT, time.localtime() )

def usage():
    print('Help!! Please put in "-i matching.log"!')

#解析命令行，来获取相应参数，具体见--help
def parseParams():
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input_file="])

    input_file = ""

    for op, value in opts:
        if op in ("-i","--input_file"):
            input_file = value
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("input_file=", input_file)

    return input_file

class Analysis:
    def __init__(self, date):
        self.date = date
        self.total_msg = 0
        self.online_not_rec = 0
        self.offline_rec = 0
        self.offline_rec_than_online = 0
        self.rec_different = 0

    def report(self):
        print(self.date, \
        ' 总处理数据:', self.total_msg, \
        '报站算法未识别:', self.online_not_rec, \
        '准报站算法识别:', self.offline_rec, \
        '准报站算法识别，报站算法未识别:', self.offline_rec_than_online, \
        '差异:', self.rec_different)

Analysis_Date = dict()

def dealwith(sample_line):
    date = sample_line[0:10]
    if not date in Analysis_Date.keys():
        Analysis_Date[date] = Analysis(date)

    #2016-06-14 00:02:02 INFO  system - Total msg = 0, online not rec count 0, offline rec count 0, offline_rec_than_online = 0, rec different = 0
    pattern = r"Total msg = (\d*), online not rec count (\d*), offline rec count (\d*), offline_rec_than_online = (\d*), rec different = (\d*)"
    if re.search(pattern, sample_line):
        res = re.search(pattern, sample_line).groups()
        Analysis_Date[date].total_msg += int(res[0])
        Analysis_Date[date].online_not_rec += int(res[1])
        Analysis_Date[date].offline_rec += int(res[2])
        Analysis_Date[date].offline_rec_than_online += int(res[3])
        Analysis_Date[date].rec_different += int(res[4])

def run(input_file):
    sample_file = codecs.open(input_file, 'r', 'utf-8')

    sample_line = sample_file.readline()

    lineno = 0
    n = 100000
    while sample_line:
        lineno+=1
        if (sample_line != ""):
            dealwith(sample_line)
        sample_line = sample_file.readline()


if __name__ == "__main__":

    input_file = parseParams();
    print('开始统计:%s'%getTime())
    run(input_file)
    for key in Analysis_Date.keys():
        Analysis_Date[key].report()

    print('结束统计:%s'%getTime())
