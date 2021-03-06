# -*- coding: utf-8 -*-
#!/usr/bin/python

#用来统计离线结果中的 环线是哪些，主要是0，1方向都有的环线是哪些
import codecs, sys, getopt, subprocess, os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager
from Util.Business.BusPoint import WenCanOffLinePoint
from Util.Business.BusPoint import OffLineBusPoint
from Util.Tools import MathHelper

manager = Manager()
BusMap = dict()
LineMap = dict()

class LineStat:
    def __init__(self, line_id):
        self.line_id = line_id
        self._zero2zero = 0
        self._zero2one = 0
        self._one2zero = 0
        self._one2one = 0

    def TurnAround(self, pre_dir, now_dir):
        if pre_dir == 0:
            if now_dir == 0:
                self._zero2zero += 1
            else:
                self._zero2one += 1
        else:
            if now_dir == 0:
                self._one2zero += 1
            else:
                self._one2one += 1

    def NeedOutput(self):
        per = MathHelper.percent(self._zero2zero + self._one2one, self._zero2zero + self._zero2one + self._one2zero + self._one2one)
        if per > 0.5:
            return True
        return False

    def toString(self):
        return "%s,%s,%s,%s,%s\n"%(self.line_id, self._zero2zero, self._zero2one, self._one2zero, self._one2one)

class BusStat:
    def __init__(self, bus_id):
        self._bus_id = bus_id
        self._line_id = ''
        self._now_dir = -1
        self._now_station = 0

    def TurnAround(self, direction, station):

        LineMap[self._line_id].TurnAround(self._now_dir, direction)
        self._now_dir = direction
        self._now_station = station

    def Forward(self, line_id, direction, station):
        self._line_id = line_id
        self._now_dir = direction
        self._now_station = station

    def addNewGps(self, line_id, direction, station):
        if not line_id in LineMap.keys():
            LineMap[line_id] = LineStat(line_id)

        #如果是最开始，或者是换线路开了
        if self._now_dir == -1 or self._line_id != line_id:
            self.Forward(line_id, direction, station)
        elif self._now_dir == direction:
            if station >= self._now_station:
                self.Forward(line_id, direction, station)
            elif station + 5 < self._now_station:
                self.TurnAround(direction, station)
        else:
            self.TurnAround(direction, station)


def Count(line, PointClass):
    line = line.strip()
    if (line == ""):
        return

    point = PointClass(line)

    if not point.bus_id in BusMap.keys():
        BusMap[point.bus_id] = BusStat(point.bus_id)

    if point.is_rec:
        BusMap[point.bus_id].addNewGps(point.line_id, point.dir, point.station)

def getOutputFile(input_file, output_dir):
    tags = os.path.split(input_file)
    output_file = os.path.join(output_dir, tags[1])
    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)
    return output_file

def report(input_file, output_dir):
    dest_file_name = getOutputFile(input_file, output_dir)
    tmp_file_name = dest_file_name + '.tmp'
    dest_file = codecs.open(dest_file_name, 'w', 'utf-8')
    tmp_file = codecs.open(tmp_file_name, 'w', 'utf-8')

    for key in LineMap.keys():
        if LineMap[key].NeedOutput():
            dest_file.write('%s\n'%LineMap[key].line_id)
        tmp_file.write(LineMap[key].toString())

    dest_file.close()
    tmp_file.close()
    print('report finish! save to ' + dest_file_name)

@manager.option('-i', '--input', dest='input_file', required=True)
@manager.option('-m', '--point_mode', dest='point_mode', default=0)
@manager.option('-o', '--output', dest='output_dir', default='output/')
def run(input_file=None, point_mode = 0, output_dir = None):

    output_dir = os.path.abspath(output_dir)
    print('Start to run, file=%s, mode=%s, output_dir=%s'%(input_file, point_mode, output_dir))

    _file = codecs.open(input_file, 'r', 'utf-8')
    line = _file.readline()

    while line:
        #print('xmode:%s'%(point_mode))
        if int(point_mode) == 0:
            Count(line, WenCanOffLinePoint)
        else:
            Count(line, OffLineBusPoint)
        line = _file.readline()

    report(input_file, output_dir)

@manager.command
def test():
    command_line = 'python3 PrintBusTurnAround.py run -i test/sample.csv1'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

    command_line = 'python3 PrintBusTurnAround.py run -i test/matching.log.sort.cmp-100000 -m 1'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

if  __name__ ==  '__main__':
    manager.run()
