#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os, http.client, urllib.request, urllib.parse
import http.cookiejar
import time
import logging
import datetime
import ssl
import inspect

def getTime():
    ISOTIMEFORMAT = '%Y-%m-%d-%H-%M'
    return time.strftime( ISOTIMEFORMAT, time.localtime() )

def usage():
    print('Help!! Please put in "-i matching.log"!')

#解析命令行，来获取相应参数，具体见--help
def parseParams():
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["input_file="])

    input_file = ""

    for op, value in opts:
        if op in ("-i","--input_file"):
            input_file = value
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("CommandParam:")
    print("input_file=", input_file)

    return input_file

from itertools import islice

def run(input_file):
    print('开始统计:', getTime())
    sample_file = codecs.open(input_file, 'r', 'utf-8')

    sample_line = sample_file.readline()

    lineno = 0
    n = 100000
#    while sample_line:
#        lineno+=1
#        sample_line = sample_file.readline()

    with codecs.open(input_file, 'r', 'utf-8') as f:
        '''
        while True:
            next_n_lines = list(islice(f, n))
            if not next_n_lines:
                break

            for line in next_n_lines:
                lineno+=1
        '''
        for line in f:
            lineno+=1

    print('总行数:', lineno, getTime())

if __name__ == "__main__":
    input_file = parseParams();
    run(input_file)
