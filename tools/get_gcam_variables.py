import xmltodict
import json
import argparse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	return parser.parse_args()

def parse_file(input_file):
	with open(input_file) as xmlinput:
		filedict = xmltodict.parse(xmlinput.read())
		return filedict

def format_pathway_string(base, new_string):
	new_string = new_string.strip('@').strip('#')
	base = base.strip('-')
	return base + '---' + new_string

def generate_file_pathways(working_dict, working_string):
	pathways = []
	for item in working_dict:
		value = working_dict[item]
		if isinstance(value, dict):
			pathways += generate_file_pathways(value, format_pathway_string(working_string, item))
		elif isinstance(value, str):
			pathways.append(format_pathway_string(working_string, item))
		elif isinstance(value, list):
			for list_item in value:
				if isinstance(list_item, dict):
					pathways += generate_file_pathways(list_item, format_pathway_string(working_string, item))
				elif isinstance(list_item, str):
					pathways.append(format_pathway_string(working_string, item))
	return pathways

if __name__ == '__main__':
	args = get_args()
	input_file = args.inputFile
	input_dict = parse_file(input_file)
	pathways = list(set(generate_file_pathways(input_dict, '')))
	print(json.dumps(pathways, indent=4, sort_keys=True))