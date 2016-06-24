#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess, BusStat
import Kernal
import NewStatistic

#是否一条龙
one_dragon_service = False

def usage():
    print('Help!! Please put in "--input_file=matching.log --bus_relation_file=bus_rel.csv --basedata=input/s_json.csv --dragon"!')
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

#初始化
def init():
    if (not os.path.exists('temp')):
        os.makedirs('temp')

    if (not os.path.exists('compare')):
        os.makedirs('compare')

if __name__=="__main__":

#初始化
    init()
#解析命令行，来获取相应参数，具体见--help
    input_file, bus_relation_file, basedata = parseParams()
#看看是否有必要生成排序好的Sample
    input_file_sorted = Kernal.sortFile(input_file, one_dragon_service)
#产生对拍文件
    input_file_cmp = input_file_sorted+".cmp"
    Kernal.generateRealOffLineResult(basedata=basedata, input_file=input_file_sorted, bus_rel=bus_relation_file, output=input_file_cmp, force = one_dragon_service)
#统计正确率
    NewStatistic.StartStatistic(input_file_sorted, input_file_cmp)
