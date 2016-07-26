#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
import datetime

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager


manager = Manager()
@manager.option('-i', '--input_dirs', dest='input_dirs', required=True)
@manager.option('--immediate', dest='immediate', default = False)
def run(input_dirs = None, immediate = False):

if __name__ == "__main__":
    manager.run()
