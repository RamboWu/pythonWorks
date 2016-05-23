#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os, http.client, urllib.request, urllib.parse
import http.cookiejar

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


if __name__ == '__main__':
    AutoSignIn()
