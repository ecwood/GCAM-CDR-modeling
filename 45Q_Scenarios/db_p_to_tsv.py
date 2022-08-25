import json
import argparse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--inputFiles', type=str, nargs='+')
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def load_json(filename):
	with open(filename, 'r') as file:
		return json.load(file)

def convert_file(filedict):
	lines = ""
	for scenario in filedict:
		for state in filedict[scenario]:
			for tech in filedict[scenario][state]:
				for year in filedict[scenario][state][tech]:
					co2_removed = filedict[scenario][state][tech][year].get('co2 removed', None)
					energy = filedict[scenario][state][tech][year].get('energy', None)
					cost = filedict[scenario][state][tech][year].get('cost', '')
					if cost != '':
						cost_unit = cost.split(' ')[1]
					else:
						cost_unit = ""
					output = energy
					if co2_removed is not None:
						output = co2_removed
					output_unit = output.split(' ')[1]
					output = output.split(' ')[0]
					bill = scenario.split('_')[0]
					temp = scenario.split('_')[1].replace('p', '.')
					ng = str(scenario.split('_')[2] == 'NG')
					dump_list = [bill, temp, ng, tech, state, year, cost, cost_unit, output, output_unit]
					lines += '\t'.join(dump_list) + '\n'
	return lines

if __name__ == '__main__':
	args = get_args()
	header = ['bill', 'temp', 'ng', 'technology', 'state', 'year', 'cost', 'cost_units', 'output', 'output_units']
	lines = '\t'.join(header) + '\n'
	for input_file in args.inputFiles:
		lines += convert_file(load_json(input_file))
	with open(args.outputFile, 'w+') as outputfile:
		outputfile.write(lines)