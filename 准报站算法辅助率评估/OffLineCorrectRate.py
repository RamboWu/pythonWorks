#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess

import NewStatistic
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager
from Util.Tools import FileHelper

def IfContinueOn(tip):
    a = 'O'
    while (not(a in ('Y','y','N','n'))):
        a=input(tip +"?Y/N ")

    if a in ('N','n'):
        return False
    else:
        return True

manager = Manager()
@manager.option('-i', '--input_file', dest='input_file', required=True)
@manager.option('--bus_relation_file', dest='bus_relation_file', required=True)
@manager.option('--basedata', dest='basedata', required=True)
@manager.option('--dragon', dest='dragon', default=False)
def run(input_file = None, bus_relation_file=None, basedata=None, dragon=False):
    print(input_file, bus_relation_file, basedata, dragon)
    #看看是否有必要生成排序好的Sample
    input_file_sorted = input_file + '.sort'
    if not os.path.exists(input_file_sorted):
        FileHelper.sortFile(input_file)

    bus_relation_file = os.path.abspath(bus_relation_file)
    if not os.path.exists(bus_relation_file):
        FileHelper.generateBusLineRelationFile(basedata, input_file_sorted, bus_relation_file)
    else:
        print(bus_relation_file + ' already exist! move to next step!')

    input_file_cmp = input_file_sorted+".cmp"
    if not os.path.exists(input_file_cmp):
        FileHelper.generateRealOffLineResult(basedata=basedata, input_file=input_file_sorted, bus_rel=bus_relation_file, output=input_file_cmp)
    else:
        print(input_file_cmp + ' already exist! move to next step!')

    NewStatistic.StartStatistic(input_file_sorted, input_file_cmp, input_file)

@manager.option('-i', '--input', dest='input_file', required=True)
@manager.option('-j', '--judge', dest='judge_file', required=True)
def count(input_file=None, judge_file = None):
    NewStatistic.StartStatistic(input_file, judge_file)

if __name__=="__main__":
    manager.run()
