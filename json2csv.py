import sys
import getopt
import os
import json
import csv

#get user arguments
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
	if input == '':
		input = './'
	if output == '':
		output = './'
	return input, output

#reads a json file and returns a json dictionary
def json2csv(file):
	fo = open(file, 'r')
	data = json.load(fo)
	fo.close()
	return data

#writes to a csv file
def writeCSV(folder, file, jsonArray):
	joined = os.path.join(folder, file)
	fo = open(os.path.join(joined), 'w', newline='')
	writer = csv.writer(fo)
	writer.writerow(jsonArray[0].keys())
	for row in jsonArray:
		writer.writerow(row.values())
	fo.close()

#homogenizes the data between the different tests
def cleanData(data):
	allowedKeys = ["TestName", "TestStartTime", "TestEndTime",
			   "MurakamiLocation", "MurakamiConnectionType", "MurakamiNetworkType",
			    "DownloadValue", "DownloadUnit",	"UploadValue", "UploadUnit"]
	ogKeys = list(data.keys())
	for key in ogKeys:
		if key not in allowedKeys:
			data.pop(key)
	return data

if __name__ == '__main__':
	print("Running")
	argv = sys.argv[1:]
	input, output = get_args(argv)
	files = os.listdir(input)
	ndt5Array = []
	ndt7Array = []
	multiArray = []
	singleArray = []
	for file in	files:
		if file.endswith('.jsonl'):
			joined = os.path.join(input, file)
			jsonData = json2csv(joined)
			if "TestError" in jsonData: #Checking if there was any errors, skipping the file if there was
				continue
			jsonData = cleanData(jsonData)
			if 'ndt5' in file:
				ndt5Array.append(jsonData)
			elif 'ndt7' in file:
				ndt7Array.append(jsonData)
			elif 'multi-stream' in file:
				multiArray.append(jsonData)
			elif 'single-stream' in file:
				singleArray.append(jsonData)
	writeCSV(output, 'ndt5.csv', ndt5Array)
	writeCSV(output, 'ndt7.csv', ndt7Array)
	writeCSV(output, 'multi-stream.csv', multiArray)
	writeCSV(output, 'single-stream.csv', singleArray)
	print("Done")