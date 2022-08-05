import json
import argparse
import datetime

def get_date():
	return datetime.datetime.now().ctime()

def load_json(filename):
	with open(filename, 'r') as file:
		return json.load(file)

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def is_state(region_name):
	return len(region_name) == 2

def is_grid(region_name):
	return 'grid' in region_name

def get_tech_tags(regions_dict):
	state_tags = set()
	grid_tags = set()
	global_tags = set()
	for region in regions_dict:
		if is_state(region):
			state_tags.update(regions_dict[region].keys())
		elif is_grid(region):
			grid_tags.update(regions_dict[region].keys())
		else:
			global_tags.update(regions_dict[region].keys())
	return {'State Tags': sorted(list(state_tags)),
			'Grid Tags': sorted(list(grid_tags)),
			'Global Tags': sorted(list(global_tags))}

if __name__ == '__main__':
	args = get_args()
	file_dict = load_json(args.inputFile)
	scenario = [key for key in file_dict.keys()][0]
	regions_dict = file_dict[scenario]
	save_json(get_tech_tags(regions_dict), args.outputFile)
