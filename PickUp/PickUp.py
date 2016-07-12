#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os, subprocess

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager


def writeOneLineToOneFile(line, file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))

    dest_file = codecs.open(file_name, 'a', 'utf-8')
    dest_file.write(line)
    dest_file.close()

def pickup(input_file_name, keys, index, output_file, single_dir, postfix, noTotalFile):
    print(input_file_name, keys, output_file, index, single_dir, postfix)
    if not os.path.exists(input_file_name):
        print(input_file_name + ' not exists')
        return

    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))

    keys = keys.split(',')
    input_file = codecs.open(input_file_name, 'r', 'utf-8')
    if not noTotalFile:
        dest_file = codecs.open(output_file, 'w', 'utf-8')
    line = input_file.readline()
    while line:
        tags = line.strip().split(',')
        if len(tags) >= index and tags[index] in keys:
            if not noTotalFile:
                dest_file.write(line)
            if single_dir != None:
                writeOneLineToOneFile(line, os.path.join(os.path.join(os.path.dirname(output_file),single_dir),tags[index]+postfix))

        line = input_file.readline()

    input_file.close()
    if not noTotalFile:
        dest_file.close()

manager = Manager()
@manager.option('-i', '--input', dest='input_file', required=True)
@manager.option('-k', '--keys', dest='keys', required = True)
@manager.option('-n', '--index', dest='index', default = 3)
@manager.option('-o', '--output', dest='output_file', default = 'output')
@manager.option('-d', '--dir', dest='single_dir', default = None)
@manager.option('-p', '--postfix', dest='postfix', default = '.csv')
def run(input_file = None, keys = None, output_file = 'output', index = 3, single_dir=None, postfix='.csv', noTotalFile=False):
    pickup(input_file, keys, index, output_file, single_dir, postfix, noTotalFile)

@manager.command
def test():
    command_line = 'python3 PickUp.py run -i test/input/test.csv1 -k 078113,078114 -o test/output/output.csv'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

if __name__ == "__main__":
    manager.run()
