#  -*- coding: utf-8 -*-
#!/usr/bin/python
import os, subprocess, sys

def makeDir(dir_name):
    if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)

#排序文件
def sortFile(file_name):

    makeDir('temp')

    tags = os.path.split(__file__)
    now_dir = tags[0]+'/'

    file_sorted = file_name + ".sort"

    tags = os.path.split(file_name)
    command_line = 'java -jar ' + now_dir + 'FileSort.jar 2 ' + tags[0] + '/ ' + tags[1] + ' 3'
    print('Excute Command: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    return file_sorted

def generateRealOffLineResult(basedata, input_file, bus_rel, output):

    if not os.path.exists(basedata):
        print(basedata + ' not exist!')
        return False
    if not os.path.exists(input_file):
        print(input_file + 'not exist!')
        return False
    if not os.path.exists(bus_rel):
        print(bus_rel + ' not exist!')
        return False

    tags = os.path.split(__file__)
    now_dir = tags[0]+'/'

    command_line = now_dir + 'BusMatchingResultGenerator.exe -m=0 -lon=10 -lat=11 -l=' + basedata + ' -i=' + input_file + ' -b=' + bus_rel+ ' -o=' + output
    print('生成judgement_result.csv: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    return True
