#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess, shutil
import re
import datetime
import time
sys.path.append("..")
from Util import *
from Util.Tools import *

def usage():
    print('Help!! Please put in "-c TianJin -i input/matching.log.2015-04-16 -d 7 --buses=bus.csv --basedatadir=D:\AlgorithmReport\Citys\TianJin"!')

#解析命令行，来获取相应参数，具体见--help
def parseParams():
    global one_dragon_service
    opts, args = getopt.getopt(sys.argv[1:], "hi:d:c:g:", ["buses=","init","basedatadir="])

    input_file = ""
    days = 1
    buses = ""
    city = ""
    init = False
    base_data_dir = ""

    for op, value in opts:
        if op in ("-i"):
            input_file = value
        elif op in ("-d"):
            days = int(value)
        elif op in ("--buses"):
            buses = value
        elif op in ("-c"):
            city = value
        elif op in ("--init"):
            init = True
        elif op in ("-g","--basedatadir"):
            base_data_dir = value
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == "" or city == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("city", city , "input_file=", input_file, "days=", days, "buses=", buses, "init", init, "base_data_dir", base_data_dir)

    return city, input_file, days, buses, init, base_data_dir

def selectGPSFromFile(input_file, buses, output_file):
    print('selectGPSFromFile', input_file, buses, output_file)
    tags = os.path.split(output_file)
    bus_rel = tags[0] + '/bus_rel.csv'
    res, bus_relations = FileHelper.getBusRelations(bus_rel)
    if not res:
        return False

    #print(bus_relations)

    bus_file = codecs.open(buses, 'r', 'utf-8')
    bus_line = bus_file.readline()
    buses = []
    while bus_line:
        bus_line = bus_line.strip()
        if (bus_line != '') and bus_line in bus_relations.keys():
            buses = buses + bus_relations[bus_line]
            #buses.append(bus_relations[bus_line])
        bus_line = bus_file.readline()

    print('buses', buses)
    bus_file.close()

    return SelectGPSKernal.selectGPS(input_file_name=input_file, buses=buses, output_file_name=output_file)

def selectGPSFromFileAndSort(input_file, buses, output_file):

    if selectGPSFromFile(input_file, buses, output_file):
        sorted_file = FileHelper.sortFile(output_file)
        os.remove(output_file)
        os.rename(sorted_file,output_file)
        RunOffLineForFile(output_file)

def CopyBaseDataToOutputDir(output_dir, date, base_data_dir):
    base_data_dir_s = os.path.join(base_data_dir, date)
    s_json_file = os.path.join(base_data_dir_s, 's_json.csv')
    bus_rel_file = os.path.join(base_data_dir_s, 'single.csv')
    output_dir_s = os.path.join(output_dir, date)
    s_json_dest = os.path.join(output_dir_s, 's_json.csv')
    bus_rel_dest = os.path.join(output_dir_s, 'bus_rel.csv')
    #print(base_data_dir_s, s_json_file, output_dir_s, s_json_dest)
    shutil.copy(s_json_file, s_json_dest)
    if not os.path.exists(bus_rel_dest):
        shutil.copy(bus_rel_file, bus_rel_dest)

def selectGPS(input_file, days, buses, output_dir, base_data_dir):
    print('SelectGPS')
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
        CopyBaseDataToOutputDir(output_dir, yesterday, base_data_dir)
        output_file = output_dir + yesterday + '/sample.log'
        selectGPSFromFileAndSort(yes_file, buses, output_file)
        yesterday = DateHelp.get_yestoday(yesterday)
        i -= 1

def RunOffLineForFile(input_file):
    print('RunOffLineForFile: ' + input_file)
    tags = os.path.split(input_file)
    basedata = tags[0] + '/s_json.csv'
    bus_rel = tags[0] + '/bus_rel.csv'
    output = tags[0] + '/answer.csv'
    FileHelper.generateRealOffLineResult(basedata=basedata, input_file=input_file, bus_rel=bus_rel, output=output)

def init(input_file, days, output_dir):
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
        yesterday = DateHelp.get_yestoday(yesterday)
        i -= 1

#D:\AlgorithmReport\Citys\TianJin
if __name__=="__main__":

    #解析命令行，来获取相应参数，具体见--help
    city, input_file, days, buses, initflag, base_data_dir = parseParams()

    if initflag:
        init(input_file, days, 'output/'+city+'/')
        sys.exit(0)

    selectGPS(input_file, days, buses, 'output/'+city+'/', base_data_dir)
