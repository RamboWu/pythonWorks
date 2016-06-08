#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess, BusStat
import Kernal

#是否一条龙
one_dragon_service = False

def IfContinueOn(tip):
    if one_dragon_service:
        return True
    a = 'O'
    while (not(a in ('Y','y','N','n'))):
        a=input(tip +"?Y/N ")

    if a in ('N','n'):
        return False
    else:
        return True

def usage():
    print('Help!! Please put in "--old_file=old_matching.log --new_file=new_matching.log --bus_relation_file=bus_rel.csv --basedata=input/s_json.csv --dragon"!')
#解析命令行，来获取相应参数，具体见--help
def parseParams():
    global one_dragon_service
    opts, args = getopt.getopt(sys.argv[1:], "h", ["old_file=","new_file=","bus_relation_file=","basedata=","dragon"])

    old_file = ""
    new_file = ""
    bus_relation_file = ""
    basedata = ""

    for op, value in opts:
        if op in ("--old_file"):
            old_file = value
        elif op in ("--new_file"):
            new_file = value
        elif op in ("--bus_relation_file"):
            bus_relation_file = value
        elif op == "--basedata":
            basedata = value
        elif op == "--dragon":
            one_dragon_service = True
        elif op == "-h":
            usage()
            sys.exit()

    if (old_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("old_file=", old_file, "new_file=", new_file, "bus_relation_file=", bus_relation_file, "basedata=", basedata, "one_dragon_service", one_dragon_service)

    return old_file, new_file, bus_relation_file, basedata

#初始化
def init():
    if (not os.path.exists('temp')):
        os.makedirs('temp')

    if (not os.path.exists('compare')):
        os.makedirs('compare')

#生成offline_result和 离线程序的result
def generateCompareSample(old_file_sorted, new_file_sorted, bus_relation_file, basedata):

    if not IfContinueOn('是否要生成对比Sample文件'):
        return

    old_file_cmp = old_file_sorted+".cmp"
    new_file_cmp = new_file_sorted+".cmp"
    Kernal.generateRealOffLineResult(basedata=basedata, input_file=old_file_sorted, bus_rel=bus_relation_file, output=old_file_compare)
    Kernal.generateRealOffLineResult(basedata=basedata, input_file=new_file_sorted, bus_rel=bus_relation_file, output=new_file_cmp)

    return old_file_cmp, new_file_cmp

#根据BusRelations来取出待排序的gps点，然后排序
def generateSortedSample(old_file, new_file):

    if not IfContinueOn('是否要生成排好序的Sample文件'):
        return
    #排序tmp文件
    Kernal.sortFile(old_file)
    Kernal.sortFile(new_file)

    old_file_sorted = old_file + ".sort"
    new_file_sorted = new_file + ".sort"

    return old_file_sorted, new_file_sorted


if __name__=="__main__":

#初始化
    init()
#解析命令行，来获取相应参数，具体见--help
    old_file, new_file, bus_relation_file, basedata = parseParams()
#看看是否有必要生成排序好的Sample
    old_file_sorted, new_file_sorted = generateSortedSample(old_file, new_file)
#产生对拍文件
    old_file_cmp, new_file_cmp = generateCompareSample(old_file_sorted, new_file_sorted, bus_relation_file, basedata)
#统计正确率
    BusStat.CountAccuracy(old_file_sorted, old_file_cmp)
    BusStat.CountAccuracy(new_file_sorted, new_file_cmp)
