#  -*- coding: utf-8 -*-
#!/usr/bin/python

#BusStat.py
import codecs
'''
Created on 2016-05-20

@author: RamboWu
'''

#产生公交关系
def generateBusRelations(base_data_file, input_file, bus_relation_file):

    command_line = 'BusMatching.exe --offline --baseData ' + base_data_file + ' --inputFile ' + input_file + ' --bus_rel_file ' + bus_relation_file
    print('生成BusRelations: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

#从bus_file里获取公交车辆关系
def getBusRelations(bus_relation_file):
    bus_file = codecs.open(bus_relation_file, 'r', 'utf-8')
    line = bus_file.readline()

    bus_relations = []

    while line:
        tags = line.split(',')
        bus_relations.append(tags[0])
        line = bus_file.readline()

    bus_file.close()
    print("BusRelations:")
    print(bus_relations)

    return bus_relations

#把input_file里相关的公交车辆GPS数据打印到tmp文件里，等待排序
def printRelateBus(src_file_name, dest_file_name, bus_relations):
    src_file = codecs.open(src_file_name, 'r', 'utf-8')
    dest_file = codecs.open(tmp_file_name, 'w', 'utf-8')

    line = src_file.readline()
    while line:
        tags = line.split(',')
        if tags[3] in bus_relations:
            dest_file.write(line)
        line = src_file.readline()

    src_file.close();
    dest_file.close();

#根据BusRelations来取出待排序的gps点，然后排序
def generateSortedSample(input_file, output_file, bus_relation_file):

    #从bus_file里获取公交车辆关系
    bus_relations = getBusRelations(bus_relation_file)
    #把input_file里相关的公交车辆GPS数据打印到tmp文件里，等待排序
    printRelateBus(input_file, output_file, bus_relations)
    #排序tmp文件
    sortTmp()
