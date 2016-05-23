#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os

ghost_buses = []


#统计
def static(data_dir):

    files = get_right_files(data_dir)
    print(files)

# End of datatab_convert().

def get_right_files(dir):
    '''Get a list of files under input dir.'''
    result = []
    for root,dirs,files in os.walk(dir):
        for f in files:
            if (dosatisfy(f)):
                result.append(os.path.join(root, f))
    return result
# End of get_files().

def dosatisfy(filename):
    ext = os.path.splitext(filename)[1].lower()
    if '.csv' != ext:
        return False
    return True

# End of dosatisfy().

#从bus_file里获取公交车辆关系
def getGhostBuses(ghost_file_name):
    global ghost_buses

    ghost_file = codecs.open(ghost_file_name, 'r', 'utf-8')
    line = ghost_file.readline()

    while line:
        tags = line.split(',')
        ghost_buses.append(tags[0])
        line = ghost_file.readline()

    ghost_file.close()
    print("GhostBuses:")
    print(ghost_buses)


def parseParams():

    opts, args = getopt.getopt(sys.argv[1:], "hg:i:", ["ghost=", "input="])

    ghost_file = ""
    input_dir = ""

    for op, value in opts:
        if op in ("-g","--ghost"):
            ghost_file = os.path.abspath(value)
        elif op in ("-i","--input"):
            input_dir = os.path.abspath(value)

    if (ghost_file == ""):
        print("ghost_file can't be none")
        sys.exit()

    print("CommandParam:")
    print("ghost", ghost_file, "input", input_dir)

    return ghost_file, input_dir

if __name__ == '__main__':

    ghost_file, input_dir = parseParams()

    getGhostBuses(ghost_file)

    static(input_dir)
