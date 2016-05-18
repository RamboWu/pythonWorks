#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess

bus_relations = []
#bus_file有默认参数
bus_file_name = os.path.abspath('compare/bus_relations.csv')
tmp_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp')
sort_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp.sort')

#把input_file里相关的公交车辆GPS数据打印到tmp文件里，等待排序
def printRelateBus(src_file_name, dest_file_name):
    src_file = codecs.open(src_file_name, 'r', 'utf-8')
    dest_file = codecs.open(tmp_file_name, 'w', 'utf-8')

    line = src_file.readline()
    while line:
        tags = line.split(',')
        if int(tags[3]) in bus_relations:
            dest_file.write(line)
        line = src_file.readline()

    src_file.close();
    dest_file.close();
#从bus_file里获取公交车辆关系
def getBusRelations():
    bus_file = codecs.open(bus_file_name, 'r', 'utf-8')
    line = bus_file.readline()

    while line:
        tags = line.split(',')
        bus_relations.append(int(tags[0]))
        line = bus_file.readline()

    bus_file.close()
    print("BusRelations:")
    print(bus_relations)
#排序tmp文件
def sortTmp():
    tags = os.path.split(tmp_file_name)
    command_line = 'java -jar FileSort.jar 2 ' + tags[0] + '/ ' + tags[1] + ' 3'
    print('Excute Command: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

def usage():
    print('Help!! Please put in "-b busfile_name -i inputfile_name -o output_file_name"!')
#解析命令行，来获取相应参数，具体见--help
def parseParams():
    opts, args = getopt.getopt(sys.argv[1:], "hb:i:o:", ["busfile=","input=","output="])

    input_file = ""
    output_file = "output"
    bus_file = ""

    for op, value in opts:
        if op in ("-i","--input"):
            input_file = value
        elif op in ("-o","--output"):
            output_file = value
        elif op in ("-b","--busfile"):
            bus_file_name = value
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("busfile", bus_file, "input", input_file, "output", output_file)

    return input_file, output_file
#初始化
def init():
    if (not os.path.exists('temp')):
        os.makedirs('temp')

def generateBusRelations():
    a = 'O'
    while (not(a in ('Y','y','N','n'))):
        a='y'#raw_input("是否要进行生成BusRelations?Y/N ")

    if a in ('N','n'):
        return

    print('#TODO 产生BusRelations')

if __name__=="__main__":

#初始化
    init()
#解析命令行，来获取相应参数，具体见--help
    input_file, output_file = parseParams()

#看看是否有必要产生BusRelations文件
    generateBusRelations()
#从bus_file里获取公交车辆关系
    getBusRelations()
#把input_file里相关的公交车辆GPS数据打印到tmp文件里，等待排序
    printRelateBus(input_file, output_file)
#排序tmp文件
    sortTmp()
