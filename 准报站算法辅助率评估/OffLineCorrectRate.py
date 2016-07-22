#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess
import time

import NewStatistic
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager
from Util.Tools import FileHelper
from Util.Tools import LogHelper

system_logger = LogHelper.makeConsoleAndFileLogger('log/System.log')
manager = Manager()
@manager.option('-i', '--input_file', dest='input_file', required=True)
@manager.option('--bus_relation_file', dest='bus_relation_file', required=True)
@manager.option('--basedata', dest='basedata', required=True)
@manager.option('--sleep', dest='sleep_time', default = None)
@manager.option('-o', '--output', dest='output', default = None)
@manager.option('--detail', dest='detail', default = True)
def run(input_file = None, bus_relation_file=None, basedata=None, sleep_time = None, output = None, detail=True):
    system_logger.info('生成评测报告run input=%s single=%s s_json=%s delay=%s outputdetail=%s', \
        input_file, bus_relation_file, basedata, sleep_time, detail)

    if sleep_time != None:
        print('sleep %s seconds'%(sleep_time))
        time.sleep(int(sleep_time))

    #看看是否有必要生成排序好的Sample
    input_file_sorted = input_file + '.sort'
    if not os.path.exists(input_file_sorted):
        system_logger.info('排序: input:%s output:%s', input_file, input_file_sorted)
        FileHelper.sortFile(input_file)

    bus_relation_file = os.path.abspath(bus_relation_file)
    if not os.path.exists(bus_relation_file):
        system_logger.info('生成single.csv: input:%s s_json:%s, output:%s', input_file_sorted, basedata, bus_relation_file)
        FileHelper.generateBusLineRelationFile(basedata, input_file_sorted, bus_relation_file)
    else:
        system_logger.info('Single.csv already exist! move to next step!')

    input_file_cmp = input_file_sorted+".cmp"
    if not os.path.exists(input_file_cmp):
        system_logger.info('生成cmp: input:%s s_json:%s, single=%s output=%s', input_file_sorted, basedata, bus_relation_file, input_file_cmp)
        FileHelper.generateRealOffLineResult(basedata=basedata, input_file=input_file_sorted, bus_rel=bus_relation_file, output=input_file_cmp)
    else:
        system_logger.info('Cmp already exist! move to next step!')

    system_logger.info('StartStatistic: -i %s -j %s -o %s -detail %s', input_file_sorted, input_file_cmp, output, detail)
    NewStatistic.StartStatistic(input_file_sorted, input_file_cmp, original=input_file, output = output, detail=detail)

@manager.option('-l', '--location', dest='location', required=True)
@manager.option('--detail', dest='detail', default = True)
def batch(location = None, exucte_file = None, detail = True):
    detail = bool(int(detail) > 0)
    system_logger.info('')
    system_logger.info('批量测试: locaiton=%s outputdetail=%s ', location, detail )
    if not os.path.isdir(location):
        print(location + ' isn\'t a dir')
        return

    list = os.listdir(location)  #列出目录下的所有文件和目录
    for line in list:
        filepath = os.path.join(location,line)
        if os.path.isdir(filepath):  #如果filepath是目录，则再列出该目录下的所有文件
            batch(filepath, detail)

    input_file = os.path.join(location, 'matching.log')
    bus_relation_file = os.path.join(location, 'single.csv')
    basedata = os.path.join(location, 's_json.csv')
    if os.path.exists(input_file) and os.path.exists(basedata):
        run(input_file, bus_relation_file, basedata, output=location, detail=detail)
    else:

        online_file = os.path.join(location, 'online.log')
        if os.path.exists(online_file) and os.path.exists(basedata):
            system_logger.info('根据online.log=>matching.log: input=%s s_json=%s ', online_file, basedata )
            FileHelper.generateDataAfterBusMatching(online_file, basedata, input_file)
            if os.path.exists(input_file):
                run(input_file, bus_relation_file, basedata, output=location, detail=detail)
        else:

            offline_file = os.path.join(location, 'offline.log')
            if os.path.exists(offline_file) and os.path.exists(basedata):
                system_logger.info('根据offline.log=>matching.log: input=%s s_json=%s ', online_file, basedata )
                FileHelper.generateDataCompleteProcess(offline_file, basedata, input_file)
                if os.path.exists(input_file):
                    run(input_file, bus_relation_file, basedata, output=location, detail=detail)

@manager.option('-i', '--input', dest='input_file', required=True)
@manager.option('-j', '--judge', dest='judge_file', required=True)
@manager.option('--detail', dest='detail', default = True)
def count(input_file=None, judge_file = None, detail = True):
    detail = bool(int(detail) > 0)
    NewStatistic.StartStatistic(input_file, judge_file, detail=detail)

if __name__=="__main__":
    manager.run()
