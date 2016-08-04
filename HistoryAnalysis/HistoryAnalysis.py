#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
import datetime

from HistoryFlightsAnalysis import HistoryFlightsAnalysis
from HistoryOriginalWrongAnalysis import HistoryOriginalWrongAnalysis

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager


manager = Manager()
@manager.option('-i', '--input_dirs', dest='input_dirs', required=True)
def run(input_dirs = None):
    analysis = HistoryOriginalWrongAnalysis()
    analysis.readCity(input_dirs)

    analysis = HistoryFlightsAnalysis()
    analysis.readCity(input_dirs)

@manager.command
def test():
    run('test/TianJin')

if __name__ == "__main__":
    manager.run()
