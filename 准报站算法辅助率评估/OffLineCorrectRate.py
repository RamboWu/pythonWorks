#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess
import Kernal
import NewStatistic
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager

#初始化
def init():
    if (not os.path.exists('temp')):
        os.makedirs('temp')

manager = Manager()
@manager.option('-i', '--input_file', dest='input_file', required=True)
@manager.option('--bus_relation_file', dest='bus_relation_file', required=True)
@manager.option('--basedata', dest='basedata', required=True)
@manager.option('--dragon', dest='dragon', default=False)
def run(input_file = None, bus_relation_file=None, basedata=None, dragon=False):
    print(input_file, bus_relation_file, basedata, dragon)
    #看看是否有必要生成排序好的Sample
    input_file_sorted = Kernal.sortFile(input_file, dragon)
    input_file_cmp = input_file_sorted+".cmp"
    Kernal.generateRealOffLineResult(basedata=basedata, input_file=input_file_sorted, bus_rel=bus_relation_file, output=input_file_cmp, force = dragon)
    NewStatistic.StartStatistic(input_file_sorted, input_file_cmp)

if __name__=="__main__":
    init()
    manager.run()
