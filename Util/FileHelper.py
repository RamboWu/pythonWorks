#  -*- coding: utf-8 -*-
#!/usr/bin/python
import os

def makeDir(dir_name):
    if (not os.path.exists(dir_name)):
        os.makedirs(dir_name)
