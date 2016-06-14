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
