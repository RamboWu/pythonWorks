#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os, http.client, urllib.request, urllib.parse
import http.cookiejar
import time
import logging
import datetime
import ssl
import inspect



def OffLineServerRun():

    command_line = '.\BusMatching.exe --offline --inputFile input/matching.log --backup --line 100000'
    print('Cmd: ' + command_line)
    status = subprocess.call(command_line, shell=True)

def run():

    old_time = time.time()

    while True:
        new_time = time.time()
        if (int(new_time - old_time) > 5):
            print('OffLineServer run!',new_time)
            OffLineServerRun()
            old_time = time.time()
        time.sleep(1)

if __name__ == "__main__":
    run()
