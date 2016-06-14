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
    print('Help!! Please put in "-c TianJin -i input/matching.log.2015-04-16 -d 7 --buses=bus.csv"!')

#解析命令行，来获取相应参数，具体见--help
def parseParams():
    global one_dragon_service
    opts, args = getopt.getopt(sys.argv[1:], "hi:d:c:", ["buses="])

    input_file = ""
    days = 1
    buses = ""
    city = ""

    for op, value in opts:
        if op in ("-i"):
            input_file = value
        elif op in ("-d"):
            days = int(value)
        elif op in ("--buses"):
            buses = value
        elif op in ("-c"):
            city = value
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == "" or city == "" or buses == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("city", city , "input_file=", input_file, "days=", days, "buses=", buses)

    return city, input_file, days, buses

def selectGPSFromFile(input_file, buses, output_file):
    print(input_file, buses, output_file)
    bus_file = codecs.open(buses, 'r', 'utf-8')
    bus_line = bus_file.readline()
    buses = []
    while bus_line:
        bus_line = bus_line.strip()
        if (bus_line != ''):
            buses.append(bus_line)
        bus_line = bus_file.readline()

    print(buses)
    bus_file.close()

    SelectGPSKernal.selectGPS(input_file_name=input_file, lines=buses, output_file_name=output_file)

def selectGPS(input_file, days, buses, output_dir):
    length = len(input_file)
    date = input_file[length-10:length]
    if not DateHelp.is_valid_date(date):
        print(input_file + ' doesn\'t has a valid date')

    i = days;
    yesterday = date
    while (i>0):
        yes_file = input_file.replace(input_file[length-10:length], yesterday)
        tags = os.path.split(yes_file)
        FileHelper.makeDir(output_dir + yesterday)
        output_file = output_dir + yesterday + '/' + tags[1]
        selectGPSFromFile(yes_file, buses, output_file)
        yesterday = DateHelp.get_yestoday(yesterday)
        i -= 1

if __name__=="__main__":

    #解析命令行，来获取相应参数，具体见--help
    city, input_file, days, buses = parseParams()
    selectGPS(input_file, days, buses, 'output/'+city+'/')
