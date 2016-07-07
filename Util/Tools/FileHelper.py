#  -*- coding: utf-8 -*-
#!/usr/bin/python
import os, subprocess, sys, codecs, shutil
import random

def makeDir(dir_name):
    if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)

def BundleTest():
     #获取脚本路径
    frozen = 'not'
    if getattr(sys, 'frozen', False):
            # we are running in a bundle
            frozen = 'ever so'
            bundle_dir = sys._MEIPASS
    else:
            # we are running in a normal Python environment
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
    print( 'we are',frozen,'frozen')
    print( 'bundle dir is', bundle_dir )
    print( 'sys.argv[0] is', sys.argv[0] )
    print( 'sys.executable is', sys.executable )
    print( 'os.getcwd is', os.getcwd() )

#获取jar等执行文件的目录位置
def GetExcuatbleDir():

    #如果是pyinstaller的exe
    if getattr(sys, 'frozen', False):
        return os.getcwd()
    else:
        return os.path.dirname(os.path.abspath(__file__))

#排序文件
def sortFile(file_name):

    makeDir('temp')

    filesort = os.path.join(GetExcuatbleDir(),'FileSort.jar')

    file_sorted = file_name + ".sort"

    tags = os.path.split(file_name)
    command_line = 'java -jar ' + filesort + ' 2 ' + tags[0] + '/ ' + tags[1] + ' 3'
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

    excute_file = os.path.join(GetExcuatbleDir(),'OfflineJudgeAlg.jar')
    #java -jar OfflineJudgeAlg.jar r=1 j=s_json.csv i=42255.csv  b=single.csv o=tmp/
    tmp_dir = os.path.basename(output).replace('.','_')
    parent_dir = os.path.dirname(output)
    new_dir = os.path.join(parent_dir,tmp_dir)

    command_line = 'java -jar ' + excute_file + ' r=1 j=' + basedata + ' i=' + input_file + ' b=' + bus_rel+ ' o=' + new_dir
    print('生成judgement_result.csv: ' + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

    os.rename(os.path.join(new_dir,'answer.log'), output)
    return True

def generateBusLineRelationFile(basedata, input_file, output):
    if not os.path.exists(basedata):
        print(basedata + ' not exist!')
        return False
    if not os.path.exists(input_file):
        print(input_file + 'not exist!')
        return False


    tmpdir = os.path.join('temp','temp'+str(random.randint(1, 1000000)))
    makeDir(tmpdir)

    excute_file = os.path.join(GetExcuatbleDir(),'BusLineRelation.exe')
    '''
	cmdArg[1] = "-l=" + Configuration.lineDataFile;
	cmdArg[2] = "-i=" + Configuration.getFileInTemp(ResultConfig.mergerResult);
	cmdArg[3] = "-a=" + Configuration.getFileInTemp(ResultConfig.answerFile);
	cmdArg[4] = "-o=" + Configuration.tempDir;
    '''
    command_line = excute_file + ' -l=' + basedata + ' -i=' + input_file + ' -a=' + output+ ' -o=' + tmpdir

    print('生成 '+ output + " :\n" + command_line)
    status = subprocess.call(command_line, shell=True)
    if (status != 0):
        print("Error: Program End.")
        sys.exit(-1)

#从bus_file里获取公交车辆关系
def getBusRelations(bus_relation_file):

    if not os.path.exists(bus_relation_file):
        print(bus_relation_file + ' not exists')
        return False, []

    bus_file = codecs.open(bus_relation_file, 'r', 'utf-8')
    line = bus_file.readline()

    bus_relations = dict()

    while line:
        line = line.strip()
        tags = line.split(',')
        #bus_relations[tags[1]] = tags[0]
        if not tags[1] in bus_relations.keys():
            bus_relations[tags[1]] = []
        bus_relations[tags[1]].append(tags[0])
        #bus_relations.append((tags[0],tags[1]))
        line = bus_file.readline()

    bus_file.close()
    #print("BusRelations:")
    #print(bus_relations)

    return True, bus_relations
