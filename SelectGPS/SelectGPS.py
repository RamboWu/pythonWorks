#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess
import re
import datetime
import time

def usage():
    print('Help!! Please put in "-p matching.log.2016-06-11 -f file -d dir --buses=bus.csv"!')

'''
#解析命令行，来获取相应参数，具体见--help
def parseParams():
    global one_dragon_service
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input_file=","bus_relation_file=","basedata=","dragon"])

    input_file = ""
    bus_relation_file = ""
    basedata = ""

    for op, value in opts:
        if op in ("-i","--input_file"):
            input_file = value
        elif op in ("--bus_relation_file"):
            bus_relation_file = value
        elif op == "--basedata":
            basedata = value
        elif op == "--dragon":
            one_dragon_service = True
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("input_file=", input_file, "bus_relation_file=", bus_relation_file, "basedata=", basedata, "one_dragon_service", one_dragon_service)

    return input_file, bus_relation_file, basedata
'''


def get_yestoday(mytime):
	myday = datetime.datetime( int(mytime[0:4]),int(mytime[5:7]),int(mytime[8:10]) )
	#now = datetime.datetime.now()
	delta = datetime.timedelta(days=-1)
	my_yestoday = myday + delta
	my_yes_time = my_yestoday.strftime('%Y-%m-%d')
	return my_yes_time

if __name__=="__main__":

    date = '2015-12-16'
    print( get_yestoday('2015-04-07'))
#解析命令行，来获取相应参数，具体见--help
    #input_file, bus_relation_file, basedata = parseParams()
