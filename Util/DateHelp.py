#  -*- coding: utf-8 -*-
#!/usr/bin/python

import datetime
import time

def get_yestoday(mytime):
	myday = datetime.datetime( int(mytime[0:4]),int(mytime[5:7]),int(mytime[8:10]) )
	delta = datetime.timedelta(days=-1)
	my_yestoday = myday + delta
	my_yes_time = my_yestoday.strftime('%Y-%m-%d')
	return my_yes_time

def is_valid_date(str):
  '''判断是否是一个有效的日期字符串'''
  try:
    time.strptime(str, "%Y-%m-%d")
    return True
  except:
    return False
