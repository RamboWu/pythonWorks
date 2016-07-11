#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)
from Util.CommandManager import Manager




def check():
    #检查一些必要的测试文件是否存在
    pass

def dailytest():
    #一些统计
    pass


dailytest_dirs = None

#@schedudler.cron_schedule(hour=17, minute=5, second=0)
def dailytest():
    print('dailytest at:', datetime.datetime.now())
    dirs = dailytest_dirs.split(',')
    for _dir in dirs:
        

schedudler = BlockingScheduler(daemonic = False)
schedudler.add_job(dailytest, 'cron', id='dailytest', hour=1, minute=0, second=0)

manager = Manager()
@manager.option('-i', '--input_dirs', dest='input_dirs', required=True)
@manager.option('--immediate', dest='immediate', default = False)
def run(input_dirs = None, immediate = False):
    global dailytest_dirs
    print('input_dirs', input_dirs, 'immediate', immediate)
    dailytest_dirs = input_dirs
    check()
    #接受要测试的几个目录，文件名
    #定时统计 dailytest
    if immediate:
        dailytest()
    schedudler.start()

if __name__ == "__main__":

    manager.run()
