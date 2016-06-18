#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess

def usage():
    print('Help!! Please put in "--input_file=matching.log"!')
#解析命令行，来获取相应参数，具体见--help
def parseParams():
    global one_dragon_service
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input_file="])

    input_file = ""

    for op, value in opts:
        if op in ("-i","--input_file"):
            input_file = value
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("input_file=", input_file)

    return input_file

#初始化
def init():
    if (not os.path.exists('temp')):
        os.makedirs('temp')

    if (not os.path.exists('compare')):
        os.makedirs('compare')

def simpleCount(input_file):
    total_lines = 0
    total_offline_assist_count = 0
    #没有使用准报站算法gps点数
    total_offline_assist_count_not_in_use = 0

    total_laoda_count = 0

    print('开始统计:')
    sample_file = codecs.open(input_file, 'r', 'utf-8')
    sample_line = sample_file.readline()

    while sample_line:
        sample_line=sample_line.strip()
        #sample_line = '1,1,1,11340,606,606,1,15,1,5711.68,117.136207,39.183793,606,2016-06-09 07:59:59,2016-06-09 08:00:00,276.98,88.11,0,122,-'
        #print(total_lines, sample_line)
        total_lines += 1
        sample_line_tags = sample_line.split(',')
        count = sample_line.count(',') + 1

        #统计准报站算法的使用率和准确率
        if count > 18 and sample_line_tags[18] != '-':
            total_offline_assist_count += 1
            if int(sample_line_tags[0]) == 0:
                total_offline_assist_count_not_in_use += 1

        if count > 19 and sample_line_tags[19] != '-':
            total_laoda_count += 1

        sample_line = sample_file.readline()

    if (total_offline_assist_count == 0):
        total_offline_assist_count = 1
    print('准报站算法总gps点数:', total_offline_assist_count, '没有使用的个数:', total_offline_assist_count_not_in_use)
    print('总gps数:' + str(total_lines) + ' 没有使用的比例为:' + str(round(float(total_offline_assist_count_not_in_use) / float(total_lines),4)) )
    print('老大个数:' + str(total_laoda_count))

if __name__=="__main__":

#初始化
    init()
#解析命令行，来获取相应参数，具体见--help
    input_file = parseParams()
#统计正确率
    simpleCount(input_file)
