#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os


ghost_buses = dict()


def staticFile(filename):
    global ghost_buses

    print("start to static file[" + filename + "]" )
    input_file = codecs.open(filename, 'r', 'utf-8')
    line = input_file.readline()

    while line:
        tags = line.split(',')
        if tags[4] in ghost_buses.keys():
            ghost_buses[tags[4]] += 1

        line = input_file.readline()

    input_file.close()

#统计
def static(data_dir):
    global ghost_buses

    files = get_right_files(data_dir)
    print(files)

    for f in files:
        staticFile(f)
        output()


def output():
    global ghost_buses

    result = sorted(ghost_buses.items(), key=lambda d:d[1], reverse = True)
    print(result)
    dest_file = codecs.open('output', 'w', 'utf-8')
    dest_file.write(ghost_buses.__str__())
    dest_file.close()

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
    tags = filename.split('.')
    ext = tags[1].lower()
    if 'log' != ext:
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
        if not tags[0] in ghost_buses.keys():
            ghost_buses[tags[0]] = 0
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
