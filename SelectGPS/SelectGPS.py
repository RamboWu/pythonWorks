#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess
import re
import datetime
import time
sys.path.append("..")
from Util import *

def usage():
    print('Help!! Please put in "-i input/matching.log.2015-04-16 -d 7 --buses=bus.csv"!')

#解析命令行，来获取相应参数，具体见--help
def parseParams():
    global one_dragon_service
    opts, args = getopt.getopt(sys.argv[1:], "hi:d:", ["buses="])

    input_file = ""
    days = 1
    buses = ""

    for op, value in opts:
        if op in ("-i"):
            input_file = value
        elif op in ("-d"):
            days = int(value)
        elif op in ("--buses"):
            buses = value
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("input_file=", input_file, "days=", days, "buses=", buses)

    return input_file, days, buses

def selectGPSFromFile(input_file, buses):
    print(input_file, buses)
    bus_file = codecs.open(buses, 'r', 'utf-8')
    bus_line = bus_file.readline()
    buses = []
    while bus_line:
        bus_line = bus_line.strip()
        if (bus_line != ''):
            buses.append(bus_line)
        bus_line = bus_file.readline()

    print(buses)

def selectGPS(input_file, days, buses):
    length = len(input_file)
    date = input_file[length-10:length]
    if not DateHelp.is_valid_date(date):
        print(input_file + ' doesn\'t has a valid date')

    selectGPSFromFile(input_file, buses)
    yesterday = date
    for i in range(days-1):
        yesterday = DateHelp.get_yestoday(yesterday)
        yes_file = input_file.replace(input_file[length-10:length], yesterday)
        selectGPSFromFile(yes_file, buses)

#初始化
def init():
    if (not os.path.exists('output')):
        os.makedirs('output')

if __name__=="__main__":

    init()
#解析命令行，来获取相应参数，具体见--help
    input_file, days, buses = parseParams()
    selectGPS(input_file, days , buses)
