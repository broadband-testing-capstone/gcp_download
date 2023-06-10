import csv
import sys
import getopt
import os

def get_args(argv):
	input = ''
	output = ''
	opts, args = getopt.getopt(argv, "hi:o:")
	for opt, argv in opts:
		if opt == '-h':
			print('txt2csv.py -i [input folder] -o [output file]')
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

def extractValUnit(line, ValIdx, UnitIdx):
    val = line.split()[ValIdx]
    unit = line.split()[UnitIdx].strip('()')
    return val, unit

def writeCSV(folder, file, jsonArray):
	joined = os.path.join(folder, file)
	fo = open(os.path.join(joined), 'w', newline='')
	writer = csv.writer(fo)
	writer.writerow(jsonArray[0].keys())
	for row in jsonArray:
		writer.writerow(row.values())
	fo.close()

def parseTxt(file, type):
	fo = open(file, 'r')
	lines = fo.readlines()
	fo.close()
	pcktLine = lines[4]
	pcktLossStr = pcktLine.split()[2]
	pcktLoss = pcktLossStr.strip('%')
	avgRTTLine = lines[5]
	avgRTTVal, avgRTTUnit = extractValUnit(avgRTTLine, 2, 3)
	minRTTLine = lines[6]
	minRTTVal, minRTTUnit = extractValUnit(minRTTLine, 2, 3)
	maxRTTLine = lines[7]
	maxRTTVal, maxRTTUnit = extractValUnit(maxRTTLine, 2, 3)
	RTTStdDev = lines[8]
	RTTStdDevVal, RTTStdDevUnit = extractValUnit(RTTStdDev, 3, 4)
	if len(lines) > 11: #If ran with ndt7/ookla (not just mandatory google)
		downLine = lines[11]
		downVal, downUnit = extractValUnit(downLine, 1, 2)
		upLine = lines[12]
		upVal, upUnit = extractValUnit(upLine, 1, 2)
		if type == 'ndt7':
			latencyLine = lines[14].split(':')[1]
			latencyVal, latencyUnit = extractValUnit(latencyLine, 0, 1)
		elif type == 'ookla':
			latencyLine = lines[13]
			latencyVal, latencyUnit = extractValUnit(latencyLine, 1, 2)
	else:
		downVal = 0
		downUnit = ''
		upVal = 0
		upUnit = ''
		latencyVal = 0
		latencyUnit = ''
	parsedTxt = dict({'Packet Loss (%)': float(pcktLoss), 'Average RTT': float(avgRTTVal), 'Average RTT Unit': avgRTTUnit, 
					'Minimum RTT': float(minRTTVal), 'Minimum RTT Unit': minRTTUnit, 'Maximum RTT': float(maxRTTVal), 'Maximum RTT Unit': maxRTTUnit, 
					'RTT Standard Deviation': float(RTTStdDevVal), 'RTT Standard Deviation Unit': RTTStdDevUnit, 'Download Speed': float(downVal), 
					'Download Speed Unit': downUnit, 'Upload Speed': float(upVal), 'Upload Speed Unit': upUnit, 'Latency': float(latencyVal), 'Latency Unit': latencyUnit})
	return parsedTxt


if __name__ == '__main__':
	print("Running txt2csv.py")
	argv = sys.argv[1:]
	input, output = get_args(argv)
	files = os.listdir(input)
	ndt7Array = []
	ooklaArray = []
	for file in files:
		if file.endswith(".txt") & file.startswith("ndt7"):
			try:
				joined = os.path.join(input, file)
				txtData = parseTxt(joined, 'ndt7')
				ndt7Array.append(txtData)
			except:
				continue
		elif file.endswith(".txt") & file.startswith("ookla"):
			try: 
				joined = os.path.join(input, file)
				txtData = parseTxt(joined, 'ookla')
				ooklaArray.append(txtData)
			except:
				continue
	writeCSV(output, 'ndt7.csv', ndt7Array)
	writeCSV(output, 'ookla.csv', ooklaArray)
	print("Done")