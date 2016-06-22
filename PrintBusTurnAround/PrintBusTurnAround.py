# -*- coding: utf-8 -*-
#!/usr/bin/python

import codecs, sys, getopt, subprocess, os
sys.path.append("..")
from Util.CommandManager import Manager

manager = Manager()
BusMap = dict()
LineMap = dict()

class LineStat:
    def __init__(self, line_id):
        self._line_id = line_id
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

    def toString(self):
        return "%s,%s,%s,%s,%s"%(self._line_id, self._zero2zero, self._zero2one, self._one2zero, self._one2one)

class BusStat:
    def __init__(self, bus_id):
        self._bus_id = bus_id
        self._line_id = ''
        self._now_dir = -1
        self._now_station = 0

    def TurnAround(self, direction, station):

        if not self._line_id in LineMap.keys():
            LineMap[self._line_id] = LineStat(self._line_id)

        LineMap[self._line_id].TurnAround(self._now_dir, direction)
        self._now_dir = direction
        self._now_station = station

    def Forward(self, line_id, direction, station):
        self._line_id = line_id
        self._now_dir = direction
        self._now_station = station

    def addNewGps(self, line_id, direction, station):
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


def Count(line):
    line = line.strip()
    if (line == ""):
        return

    tags = line.split(',')

    if not tags[1] in BusMap.keys():
        BusMap[tags[1]] = BusStat(tags[1])

    if tags[0] == '1':
        BusMap[tags[1]].addNewGps(tags[2], int(tags[3]), int(tags[4]))

def getOutputFile(input_file):
    tags = os.path.split(input_file)
    output_file = os.path.join('output', tags[1])
    if (not os.path.exists('output')):
        os.makedirs('output')
    return output_file

def report(input_file):
    dest_file_name = getOutputFile(input_file)
    dest_file = codecs.open(dest_file_name, 'w', 'utf-8')
    for key in LineMap.keys():
        dest_file.write(LineMap[key].toString())
    dest_file.close()
    print('report finish! save to ' + dest_file_name)

@manager.option('-i', '--input', dest='input_file')
def run(input_file=None):
    print('start to run')

    _file = codecs.open(input_file, 'r', 'utf-8')
    line = _file.readline()

    while line:
        Count(line)
        line = _file.readline()

    report(input_file)

@manager.command
def test():
    command_line = 'python3 PrintBusTurnAround.py run -i test/sample.csv1'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

if  __name__ ==  '__main__':
    manager.run()
