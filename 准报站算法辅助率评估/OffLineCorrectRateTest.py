#  -*- coding: utf-8 -*-
#!/usr/bin/python

#hello.py
import sys, getopt, codecs, os, subprocess
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager

manager = Manager()
@manager.command
def test():
    command_line = 'python3 OffLineCorrectRate.py run -i test/matching.log1 --bus_relation_file=test/bus_rel.csv1 --basedata=test/s_json.csv1'
    print(command_line)
    status = subprocess.call(command_line, shell=True)

if __name__=="__main__":
    manager.run()
