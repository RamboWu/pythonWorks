#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess, BusStat
import Kernal

bus_relations = []

#是否一条龙
one_dragon_service = False

base_data_file_name = ""
#TODO 这些目录全部通过方法获得
#bus_file有默认参数
#bus_file_name = os.path.abspath('compare/bus_relations.csv')
#排序结果文件
#tmp_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp')
#sort_file_name = os.path.abspath('temp/print_relate_bus_middle.tmp.sort')
#最终准备对拍的两个结果
#real_offline_result_name = os.path.abspath('compare/real_offline_result.csv')
#offline_result_name = os.path.abspath('compare/offline_result.csv')

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

def getBaseFileName(input_file):

    if os.path.isfile(input_file):
        return os.path.abspath(os.path.join(os.path.dirname(input_file),'s_json.csv'))
    else:
        return os.path.abspath(os.path.join(input_file,'s_json.csv'))

def getBusRelationsFileName(sample_file):

    tags = os.path.splitext(os.path.basename(sample_file))
    file_name = tags[0] + '_bus_rel.csv'
    return os.path.abspath(os.path.join('compare', file_name))

def usage():
    print('Help!! Please put in "-b busfile_name -i inputfile_name -o output_file_name --dragon"!')

def dosatisfy(filename):
    tags = filename.split('.')
    ext = tags[1].lower()
    if 'log' != ext:
        return False
    return True

#产生公交关系
def generateBusRelations(input_file):

    if not IfContinueOn('是否要进行生成BusRelations'):
        return

    if os.path.isfile(input_file):
        Kernal.generateBusRelations(base_data_file=base_data_file_name, input_file=input_file, bus_relation_file=getBusRelationsFileName(input_file))
    else:

        '''Get a list of files under input dir.'''
        for root,dirs,files in os.walk(dir):
            for f in files:
                if (dosatisfy(f)):
                    sample_file = os.path.join(root, f)
                    Kernal.generateBusRelations(base_data_file=base_data_file_name, input_file=sample_file, bus_relation_file=getBusRelationsFileName(sample_file))

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
def generateSortedSample(input_file, output_file):

    if not IfContinueOn('是否要生成排好序的Sample文件'):
        return

    #Kernal.generateSortedSample(input_file, output_file)



#解析命令行，来获取相应参数，具体见--help
def parseParams():
    global base_data_file_name
    global one_dragon_service
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input=","basedata=","dragon"])

    input_file = ""
    base_data_file_name = ""

    for op, value in opts:
        if op in ("-i","--input"):
            input_file = os.path.abspath(value)
        elif op == "--basedata":
            base_data_file_name = os.path.abspath(value)
        elif op == "--dragon":
            one_dragon_service = True
        elif op == "-h":
            usage()
            sys.exit()

    if input_file == "":
        usage()
        sys.exit()
    if (not os.path.exists(input_file)):
        print("%s don't exist!" % input_file)
        sys.exit()

    if (base_data_file_name == ""):
        base_data_file_name = getBaseFileName(input_file)

    print("CommandParam:")
    print("input", input_file, "base_data_file_name:", base_data_file_name, "one_dragon_service", one_dragon_service)

    return input_file

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
    input_file = parseParams()
    #看看是否有必要产生BusRelations文件
    generateBusRelations(input_file)
    #看看是否有必要生成排序好的Sample
    generateSortedSample(input_file, output_file)
    #产生对拍文件
    generateCompareSample()
    #统计正确率
    BusStat.CountAccuracy(offline_result_name, real_offline_result_name)



    #path = 'hahaha/Input/Sample.csv'
    #tags = os.path.split(path)
    #print(os.path.pardir)
    #print(os.path.dirname(path))
    #print(os.path.abspath(path))
    #print(os.path.abspath(os.path.join(os.path.dirname(path),os.path.pardir)))
    #print(tags)
    #print(os.path.basename(path))
    #bus_relation_file = tags[0]+'../'
    #print(os.path.split('hahaha/Input/Sample.csv'))
