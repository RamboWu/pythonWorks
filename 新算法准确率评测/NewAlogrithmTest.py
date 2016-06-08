#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess, BusStat

bus_relations = []

#是否一条龙
one_dragon_service = False

base_data_file_name = os.path.abspath('input/s_json.csv')
#bus_file有默认参数
bus_file_name = os.path.abspath('compare/bus_relations.csv')
#排序结果文件
tmp_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp')
sort_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp.sort')
#最终准备对拍的两个结果
real_offline_result_name = os.path.abspath('compare/real_offline_result.csv')
offline_result_name = os.path.abspath('compare/offline_result.csv')

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
    print('Help!! Please put in "-b busfile_name -i inputfile_name -o output_file_name --dragon"!')
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
    print("old_file", old_file, "new_file", new_file, "bus_relation_file", bus_relation_file, "basedata:", basedata, "one_dragon_service", one_dragon_service)

    return old_file, new_file, bus_relation_file, basedata

#初始化
def init():
    if (not os.path.exists('temp')):
        os.makedirs('temp')

    if (not os.path.exists('compare')):
        os.makedirs('compare')

#生成offline_result和 离线程序的result
def generateCompareSample():

    if not IfContinueOn('是否要生成对比Sample文件'):
        return

    command_line = 'BusMatching.exe --offline --output --baseData ' + base_data_file_name + ' --inputFile ' + sort_file_name + ' --outputfile ' + offline_result_name
    print('生成offline_result.csv: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    command_line = 'BusMatchingResultGenerator.exe -m=0 -lon=10 -lat=11 -l=' + base_data_file_name + ' -i=' + sort_file_name + ' -b=' + bus_file_name+ ' -o=' + real_offline_result_name
    print('生成judgement_result.csv: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)
        
#根据BusRelations来取出待排序的gps点，然后排序
def generateSortedSample(old_file, new_file):

    if not IfContinueOn('是否要生成排好序的Sample文件'):
        return
    #排序tmp文件
    sortFile(old_file)
    sortFile(new_file)

if __name__=="__main__":

#初始化
    init()
#解析命令行，来获取相应参数，具体见--help
    old_file, new_file, bus_relation_file, basedata = parseParams()
#看看是否有必要生成排序好的Sample
    generateSortedSample(old_file, new_file)
#产生对拍文件
    generateCompareSample()
#统计正确率
    BusStat.CountAccuracy(offline_result_name, real_offline_result_name)
