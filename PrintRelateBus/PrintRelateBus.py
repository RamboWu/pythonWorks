#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess

bus_relations = []


base_data_file_name = os.path.abspath('input/s_json.csv')
#bus_file有默认参数
bus_file_name = os.path.abspath('compare/bus_relations.csv')
#排序结果文件
tmp_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp')
sort_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp.sort')
#最终准备对拍的两个结果
real_offline_result_name = os.path.abspath('compare/real_offline_result.csv')
offline_result_name = os.path.abspath('compare/offline_result.csv')

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
    global base_data_file_name
    opts, args = getopt.getopt(sys.argv[1:], "hb:i:o:", ["busfile=","input=","output=","basedata="])

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
        elif op == "--basedata":
            base_data_file_name = os.path.abspath(value)
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("busfile", bus_file, "input", input_file, "output", output_file, "base_data_file_name:", base_data_file_name)

    return input_file, output_file
#初始化
def init():
    if (not os.path.exists('temp')):
        os.makedirs('temp')

    if (not os.path.exists('compare')):
        os.makedirs('compare')
#产生公交关系
def generateBusRelations(input_file):
    a = 'O'
    while (not(a in ('Y','y','N','n'))):
        a=input("是否要进行生成BusRelations?Y/N ")

    if a in ('N','n'):
        return

    command_line = 'BusMatching.exe --offline --baseData ' + base_data_file_name + ' --inputFile ' + input_file
    print('Excute Command: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)
#生成offline_result和 离线程序的result
def generateCompareSample():

    a = 'O'
    while (not(a in ('Y','y','N','n'))):
        a=input("是否要生成对比Sample文件?Y/N ")

    if a in ('N','n'):
        return

    command_line = 'BusMatching.exe --offline --output --baseData ' + base_data_file_name + ' --inputFile ' + sort_file_name + ' --outputfile ' + offline_result_name
    print('Excute Command: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    command_line = 'BusMatchingResultGenerator.exe -m=0 -lon=10 -lat=11 -l=' + base_data_file_name + ' -i=' + sort_file_name + ' -b=' + bus_file_name+ ' -o=' + real_offline_result_name
    print('Excute Command: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)
#根据BusRelations来取出待排序的gps点，然后排序
def generateSortedSample(input_file, output_file):
    a = 'O'
    while (not(a in ('Y','y','N','n'))):
        a=input("是否要生成排好序的Sample文件?Y/N ")

    if a in ('N','n'):
        return

    #从bus_file里获取公交车辆关系
    getBusRelations()
    #把input_file里相关的公交车辆GPS数据打印到tmp文件里，等待排序
    printRelateBus(input_file, output_file)
    #排序tmp文件
    sortTmp()

if __name__=="__main__":

#初始化
    init()
#解析命令行，来获取相应参数，具体见--help
    input_file, output_file = parseParams()
#看看是否有必要产生BusRelations文件
    generateBusRelations(input_file)
#看看是否有必要生成排序好的Sample
    generateSortedSample(input_file, output_file)
#产生对拍文件
    generateCompareSample()
