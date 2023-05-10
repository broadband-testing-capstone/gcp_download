import sys
import getopt

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

if __name__ == '__main__':
	argv = sys.argv[1:]
	input, output = get_args(argv)
	if input == '' or output == '':
		print('json2csv.py -i [input file] -o [output file]')
		sys.exit()
