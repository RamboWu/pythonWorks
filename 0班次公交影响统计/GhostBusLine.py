#  -*- coding: utf-8 -*-
#!/usr/bin/python

import sys, getopt, codecs, os


class Buses:
    def __init__(self):
        self.buses = dict()
        self.total_count = 0

    def addBusCount(self, bus_id):
        self.total_count += 1
        if (bus_id in self.buses.keys()):
            self.buses[bus_id] += 1
        else:
            self.buses[bus_id] = 0

ghost_buses = dict()
dest_file = 0

def staticFile(filename):
    global ghost_buses

    output("start to static file[" + filename + "]" )
    input_file = codecs.open(filename, 'r', 'utf-8')
    line = input_file.readline()

    while line:
        tags = line.split(',')
        if (tags[4] in ghost_buses.keys()) and (int(tags[0]) == 1):
            ghost_buses[tags[4]].addBusCount(tags[3])

        line = input_file.readline()

    input_file.close()

#统计
def static(data_dir):
    global ghost_buses

    files = get_right_files(data_dir)
    print(files)

    for f in files:
        for one_key in ghost_buses.keys():
            ghost_buses[one_key] = Buses()
        staticFile(f)
        report()
        #output(sorted(ghost_buses.items(), key=lambda d:d[1], reverse = True))

def report():
    for key in ghost_buses.keys():
        one_ghost = ghost_buses[key]
        if (one_ghost.total_count > 0):
            output('LineID:' + key + ', Count:' + str(one_ghost.total_count))
            output(sorted(one_ghost.buses.items(), key=lambda d:d[1], reverse = True))

def output(result):
    global dest_file

    print(result)
    dest_file.write(result.__str__() + '\n')
    #dest_file.writerow(result.__str__())


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
            ghost_buses[tags[0]] = Buses()
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
    #global dest_file

    ghost_file, input_dir = parseParams()

    getGhostBuses(ghost_file)

    dest_file = codecs.open('output', 'w', 'utf-8')
    static(input_dir)
    dest_file.close()
