#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os, http.client, urllib.request, urllib.parse
import http.cookiejar
import time
from daemon import Daemon
import logging
import datetime
import ssl
import inspect


class TudouVpnAutoLoginService:

    #初始化
    def __init__(self):
        if (not os.path.exists('tmp')):
            os.makedirs('tmp')

        self.initLog()
        self.run_flag = True

    def initLog(self):

        self.logger = logging.getLogger('Tudou')
        self.logger.setLevel(logging.INFO)

        # 定义一个Handler打印INFO及以上级别的日志到sys.stdout
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        # 定义一个FileHandler
        this_file = inspect.getfile(inspect.currentframe())
        dirpath = os.path.abspath(os.path.dirname(this_file))
        file_handler = logging.FileHandler(os.path.join(dirpath,'tmp/test.log'))

        # 设置日志打印格式
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # 将定义好的console日志handler添加到root logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

        self.logger.info('TudouVpnAutoLoginService init finish!')


    def run(self):
        self.logger.info('TudouVpnAutoLoginService run!')
        old_time = time.time()
        self.AutoSignIn()

        while self.run_flag:
            new_time = time.time()
            if (int(new_time - old_time) > 7*60*60):
                self.AutoSignIn()
                old_time = time.time()
            time.sleep(10)

    def stop(self):
        self.logger.info('TudouVpnAutoLoginService stop!')
        self.run_flag = False

    def AutoSignIn(self):
        self.logger.info('Start to AutoSignIn')

        cookie = http.cookiejar.CookieJar()
        cjhdr  = urllib.request.HTTPCookieProcessor(cookie)
        opener = urllib.request.build_opener(cjhdr)
        urllib.request.install_opener(opener)


        details = urllib.parse.urlencode({'email': 'Rambo_Wu@foxmail.com', 'pass': '123456789'}).encode('UTF-8')
        url = urllib.request.Request('https://www.tudouvpn.com/login.php', details)
        url.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")

        ssl._create_default_https_context = ssl._create_unverified_context
        res = urllib.request.urlopen(url)

        self.logger.info('status:' + str(res.status) + 'reason:' + res.reason)
        self.logger.debug(res.read().decode('utf8', 'ignore'))
        self.logger.info(cookie)

        data = urllib.request.urlopen('https://www.tudouvpn.com/daily.php').read().decode('utf8', 'ignore')
        self.logger.info(data)

        return

if __name__ == "__main__":
    server = TudouVpnAutoLoginService()
    server.run()
