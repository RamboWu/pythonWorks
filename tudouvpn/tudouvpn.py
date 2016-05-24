#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os, http.client, urllib.request, urllib.parse
import http.cookiejar
import time
from daemon import Daemon
import logging

def AutoSignIn():

    cookie = http.cookiejar.CookieJar()
    cjhdr  = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cjhdr)
    urllib.request.install_opener(opener)


    details = urllib.parse.urlencode({'email': 'Rambo_Wu@foxmail.com', 'pass': '123456789'}).encode('UTF-8')
    url = urllib.request.Request('https://www.tudouvpn.com/login.php', details)
    url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")

    res = urllib.request.urlopen(url)
    print(res.status, res.reason, res.read().decode('utf8', 'ignore'))
    print(res.getheaders())

    print(cookie)

    data = urllib.request.urlopen('https://www.tudouvpn.com/daily.php').read().decode('utf8', 'ignore')
    print(data)

    return

class MyDaemon(Daemon):
    def run(self):
        #AutoSignIn()
        while True:
            time.sleep(1)

#初始化
def init():
    if (not os.path.exists('tmp')):
        os.makedirs('tmp')

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='tmp/test.log',
                    filemode='w')
    # 定义一个Handler打印INFO及以上级别的日志到sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # 设置日志打印格式
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    # 将定义好的console日志handler添加到root logger
    logging.getLogger('').addHandler(console)

    logging.info('logging init finish!')

if __name__ == "__main__":

    init()

    daemon = MyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logging.info('daemon start!')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            logging.info('daemon stop!')
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            logging.info('daemon restart!')
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
