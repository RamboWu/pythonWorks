#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess
import re
import datetime
import time
sys.path.append("..")
import Util.DateHelp

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

def selectGPS(input_file, days, buses):
    #string =
    index = input_file.find('matching.log')
    #print(index + )

if __name__=="__main__":


    date = '2015-12-16'
    print(time.strptime(date, "%Y-%m-%d"))

    print( Util.DateHelp.get_yestoday('2015-04-07'))
#解析命令行，来获取相应参数，具体见--help
    #input_file, days, buses = parseParams()
    selectGPS('input/matching.log.2015-04-16', 7 , 'input/matching.log.2015-04-16')
