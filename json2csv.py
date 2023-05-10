import sys
import getopt
import os
import json

def get_args(argv):
	input = ''
	output = ''
	opts, args = getopt.getopt(argv, "hi:o:")
	for opt, argv in opts:
		if opt == '-h':
			print('json2csv.py -i [input folder] -o [output file]')
			sys.exit()
		elif opt ==	'-i':
			input = argv
		elif opt == '-o':
			output = argv
	return input, output

def json2csv(file):
	fo = open(file, 'r')
	data = json.load(fo)
	fo.close()
	return data

if __name__ == '__main__':
	argv = sys.argv[1:]
	input, output = get_args(argv)
	if input == '':
		input = './'
	if output == '':
		output = './'
	files = os.listdir(input)
	jsonArray = []
	for file in	files:
		if file.endswith('.jsonl'):
			joined = os.path.join(input, file)
			jsonData = json2csv(joined)
			jsonArray.append(a)