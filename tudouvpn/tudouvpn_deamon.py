#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os
from daemon import Daemon
from tudouvpn import *

class MyDaemon(Daemon):
    def __init__(self, pidfile):
        Daemon.__init__(self,pidfile)
        self.server = TudouVpnAutoLoginService()
    def run(self):
        self.server.run()

#初始化
def init():
    if (not os.path.exists('tmp')):
        os.makedirs('tmp')

if __name__ == "__main__":

    init()

    daemon = MyDaemon('/tmp/daemon-example.pid')

    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('daemon start')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print('daemon stop!')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print('daemon restart!')
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
