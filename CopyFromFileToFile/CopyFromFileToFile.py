#!/usr/bin/python

#hello.py
import sys, getopt, codecs

def copyFromFileToFile(src_file_name, dest_file_name, lines, somestring, start = 0):
    src_file = codecs.open(src_file_name, 'r', 'utf-8')
    dest_file = codecs.open(dest_file_name, 'w', 'utf-8')

    line = src_file.readline()
    i = 0;
    num = 0;
    while line:
        i += 1
        if (i >= start):
            num+= 1
            if num>lines:
                break

            if (line.find(somestring) >= 0):
                dest_file.write(line)

        line = src_file.readline()

    src_file.close();
    dest_file.close();

def usage():
    print('Help!! Please put in "-i inputfile_name -o output_file_name -l 10000 -c somestring -s 50"!')

def parseParams():
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:l:c:s:")

    input_file=""
    output_file="output"
    lines = 1000
    somestring = "";
    start = 0

    for op, value in opts:
        if op == "-i":
            input_file = value
        elif op == "-o":
            output_file = value
        elif op == "-l":
            lines = int(value)
        elif op == "-c":
            somestring = value
        elif op == "-s":
            start = int(value)
        elif op == "-h":
            usage()
            sys.exit()

    if (input_file == ""):
        usage()
        sys.exit()

    print("input", input_file, "output", output_file, "line", lines, "contain", somestring, "start from:", start)

    return input_file, output_file, lines, somestring, start

if __name__=="__main__":

    input_file, output_file, lines, somestring, start = parseParams()

    copyFromFileToFile(input_file, output_file, lines, somestring, start)
