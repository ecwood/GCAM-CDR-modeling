import xmltodict
import argparse
import json

HEADER = '''# File: dac_usa.csv
# Title: Yearly values for each regions DAC deployment
# Units: MtC
# Column types: ccin
# ----------'''


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputPotentialsFile', type=str)
	parser.add_argument('inputPolicyFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def read_csv(csv_filename):
	file_list = []
	with open(csv_filename) as csv_file:
		header = []
		for line in csv_file:
			items = line.split(',')
			if line.startswith('#'):
				continue
			if len(header) == 0:
				for item in items:
					header.append(item.strip())
			else:
				assert(len(items) == len(header))
				index = 0
				line_dict = {}
				for item in items:
					line_dict[header[index]] = item.strip()
					index += 1
				file_list.append(line_dict)
	return file_list

def organize_csv(csv_dict):
	organized_csv = {}
	last_year = 0
	last_removed = 0
	final_year = 2100
	step = 5
	for year in csv_dict:
		last_year = int(year['Year'])
		last_removed = float(year['MtC Removed'])
		organized_csv[last_year] = last_removed
	if last_year < final_year:
		for year in range(last_year, final_year + step, step):
		 organized_csv[year] = last_removed
	return organized_csv

def read_json(input_file):
	with open(input_file, 'r') as input_json:
		data = json.load(input_json)
		return data

def set_state_levels(dac_potentials, policy):
	state_levels = {}
	for state in dac_potentials:
		potential = dac_potentials[state]
		state_levels[state] = {}
		for year in policy:
			state_levels[state][year] = policy[year] * potential
	return state_levels

def reorganize_levels_into_csv(state_levels):
	lowtemp_DAC_heatpump = "lowtemp DAC heatpump"
	hightemp_DAC_elec = "hightemp DAC elec"
	hightemp_DAC_NG = "hightemp DAC NG"
	csv_list = []
	csv_list.append(["region","type","year","value"])
	for state in state_levels:
		for year in state_levels[state]:
			line_lowtemp_DAC_heatpump = [state, lowtemp_DAC_heatpump, str(year), str(state_levels[state][year])]
			line_hightemp_DAC_elec = [state, hightemp_DAC_elec, str(year), str(0)]
			line_hightemp_DAC_NG = [state, hightemp_DAC_NG, str(year), str(0)]
			csv_list.append(line_lowtemp_DAC_heatpump)
			csv_list.append(line_hightemp_DAC_elec)
			csv_list.append(line_hightemp_DAC_NG)
	return csv_list

def save_csv(header, csv_list, output_file):
	outstring = header + '\n'
	for line in csv_list:
		outstring += ','.join(line) + '\n'
	with open(output_file, 'w') as output_csv:
		output_csv.write(outstring.strip())

if __name__ == '__main__':
	args = get_args()
	dac_potential_ratios = read_json(args.inputPotentialsFile)
	policy = organize_csv(read_csv(args.inputPolicyFile))
	state_levels = set_state_levels(dac_potential_ratios, policy)
	csv_levels = reorganize_levels_into_csv(state_levels)
	save_csv(HEADER, csv_levels, args.outputFile)
