#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
import datetime
import functools
from prettytable import PrettyTable

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from Util.Tools import FileHelper
from Util.Tools import LogHelper
from Util.Tools import MathHelper



def getLineFrontSimilar(file_):
    bus_file = codecs.open(file_, 'r', 'utf-8')
    line = bus_file.readline()

    relations = dict()

    while line:
        line = line.strip()
        tags = line.split(':')
        relations[tags[0]] = set()
        similar_tags = tags[1].split(',')
        for similar_line in similar_tags:
            relations[tags[0]].add(similar_line)
        line = bus_file.readline()

    bus_file.close()

    '''
    for key in relations.keys():
        tmp = key + ":"
        for line in relations[key]:
            tmp += line + ","
        print(tmp)
    '''

    return relations

class OriginalWrongAnalysisHelper:
    def __init__(self, line_front_similar_file):
        self.line_front_similar = getLineFrontSimilar(line_front_similar_file)

    def analysisSameLineFrontCount(self, one_line_id, other_line_id):
        if one_line_id == other_line_id:
            return 0, 0
        else:
            if not one_line_id in self.line_front_similar.keys():
                #print(today_line.real_line_id, today_line.original_line_id, 0 , 1)
                return 0, 1
            if not other_line_id in self.line_front_similar.keys():
                #print(today_line.real_line_id, today_line.original_line_id, 0 , 1)
                return 0, 1
            if not other_line_id in self.line_front_similar[one_line_id]:
                #print(today_line.real_line_id, today_line.original_line_id, 0 , 1)
                return 0, 1
            #print(today_line.real_line_id, today_line.original_line_id, 1, 0)
            return 1, 0
            
