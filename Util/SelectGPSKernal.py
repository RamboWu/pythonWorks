#  -*- coding: utf-8 -*-
#!/usr/bin/python

import codecs

BUS_INDEX = 3
LINE_INDEX = 4

def selectGPS(input_file_name, buses = [], lines = [], output_file_name = 'output'):
	print('selectGPS in ' + input_file_name + ' store in ' + output_file_name)
	try:
		input_file = codecs.open(input_file_name, 'r', 'utf-8')
	except:
		print (input_file_name + 'doesn\'t exit!')
		return False

	output_file = codecs.open(output_file_name, 'w', 'utf-8')
	input_line = input_file.readline()

	while input_line:
		input_line = input_line.strip()
		if (input_line != ''):
			tags = input_line.split(',')
			if (tags[BUS_INDEX] in buses) or (tags[LINE_INDEX] in lines):
				output_file.write(input_line)
				output_file.write('\n')
		input_line = input_file.readline()

	input_file.close();
	output_file.close();
	return True
