# -*- coding: utf-8 -*-
#!/usr/bin/python

#用来统计离线结果中的 环线是哪些，主要是0，1方向都有的环线是哪些
import codecs, sys, getopt, subprocess, os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager
from Util.Business.BusPoint import BusPoint
from Util.Tools import MathHelper
from Util.Tools import LogHelper

logger = LogHelper.makeConsoleAndFileLogger('CountTheoryAssistCount')
logger.info('CountTheoryAssistCount Log init finish!')
diff_logger = LogHelper.makeConsoleAndFileLogger('Diff')
manager = Manager()
BusMap = dict()

class BusStat:
    def __init__(self, bus_id):
        self.bus_id = bus_id
        self.is_dected = False
        self.dect_count = 0
        self.assist_4 = 0
        self.assist_8 = 0
        self.assist_12 = 0
        self.assist = 0
        self.real_assist = 0
        self.real_assist_not_in_use = 0
        self.real_assist_diff = 0

    def countAssist(self):
        if self.dect_count >= 4:
            self.assist_4 += 1
        if self.dect_count >= 8:
            self.assist_8 += 1
        if self.dect_count >= 12:
            self.assist_12 += 1

    def addNewGps(self, is_dected):
        if is_dected:
            if (self.is_dected):
                self.dect_count += 1
                self.countAssist()
            else:
                self.is_dected = True
                self.dect_count = 0

            self.assist += 1
        else:
            self.dect_count = False
            self.dect_count = 0

    def report(self):
        logger.info('Bus[%s] Assist[%s] Assist4[%s] Assist8[%s] Assist12[%s] 真实Assist[%s], 真实没有使用[%s], 和老大不一样的点[%s]', \
            self.bus_id, self.assist, self.assist_4, self.assist_8, self.assist_12, \
            self.real_assist, self.real_assist_not_in_use, self.real_assist_diff)

def Count(line):
    line = line.strip()
    if (line == ""):
        return

    point = BusPoint(line)

    if not point.bus_id in BusMap.keys():
        BusMap[point.bus_id] = BusStat(point.bus_id)

    BusMap[point.bus_id].addNewGps(point.is_assist_real_dectected)

    if point.assist_line_id != '-':
        BusMap[point.bus_id].real_assist += 1
        if point.is_rec:
            if point.line_id != point.assist_line_id:
                BusMap[point.bus_id].real_assist_diff += 1
                diff_logger.info(line)

        if not point.is_rec:
            BusMap[point.bus_id].real_assist_not_in_use += 1

def report(input_file, lineno):

    total_assist_4 = 0
    total_assist_8 = 0
    total_assist_12 = 0
    total_assist = 0
    total_real_assist = 0
    total_real_assist_not_in_use = 0
    total_real_assist_diff = 0

    for key in BusMap.keys():
        total_assist_4 += BusMap[key].assist_4
        total_assist_8 += BusMap[key].assist_8
        total_assist_12 += BusMap[key].assist_12
        total_assist += BusMap[key].assist
        total_real_assist += BusMap[key].real_assist
        total_real_assist_not_in_use += BusMap[key].real_assist_not_in_use
        total_real_assist_diff += BusMap[key].real_assist_diff

    logger.info('%s 理论辅助统计报告', input_file)
    logger.info('总共%s行', lineno)
    logger.info('Assist:%s', total_assist)
    logger.info('Assist_4:%s', total_assist_4)
    logger.info('Assist_8:%s', total_assist_8)
    logger.info('Assist_12:%s', total_assist_12)
    logger.info('真实辅助:%s', total_real_assist)
    logger.info('真实辅助没有使用:%s', total_real_assist_not_in_use)
    logger.info('和老大差别的个数:%s', total_real_assist_diff)
    logger.info('差异占总比:%s', MathHelper.percentToString(total_real_assist_diff, total_assist))

    for key in BusMap.keys():
        BusMap[key].report()

@manager.option('-i', '--input', dest='input_file', required=True)
def run(input_file=None):

    print('Start to run, file=%s'%(input_file))

    _file = codecs.open(input_file, 'r', 'utf-8')
    line = _file.readline()
    lineno = 0

    while line:
        Count(line)
        line = _file.readline()
        lineno += 1

    report(input_file, lineno)

@manager.command
def test():
    command_line = 'python3 CountTheoryAssistCount.py run -i test/sample.csv1'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

    command_line = 'python3 CountTheoryAssistCount.py run -i test/10301.csv1'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

if  __name__ ==  '__main__':
    manager.run()
