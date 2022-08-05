# For output by `process_broken_debug_db.py` (bed30e3)

import json
import argparse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def load_json(filename):
	with open(filename, 'r') as file:
		return json.load(file)

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def get_sequestrated_levels(file_dict):
	sequestration_dict = dict()
	energy_dict = dict()
	file_dict = file_dict['GCAM-USA_Reference']
	for region in file_dict:
		if len(region) > 2:
			continue
		for key in file_dict[region]:
			if key in ['hightemp DAC NG', 'hightemp DAC elec', 'lowtemp DAC heatpump']:
				for year in file_dict[region][key]:
					if year not in sequestration_dict:
						sequestration_dict[year] = 0
					sequestration_dict[year] += float(file_dict[region][key][year]['co2 removed'].split(' ')[0])
			else:
				for year in file_dict[region][key]:
					if key not in energy_dict:
						energy_dict[key] = dict()
					if year not in energy_dict[key]:
						energy_dict[key][year] = 0
					energy_dict[key][year] += float(file_dict[region][key][year]['energy'].split(' ')[0])
	return sequestration_dict, energy_dict

if __name__ == '__main__':
	args = get_args()
	sequestration_dict, energy_dict = get_sequestrated_levels(load_json(args.inputFile))
	save_json({"Sequestration": sequestration_dict, "Energy": energy_dict}, args.outputFile)