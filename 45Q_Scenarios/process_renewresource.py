import argparse
import json

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

def process_unit_year_text_block(block):
	return block['@year'], block['#text'] + ' ' + block['@unit']

def process_tech_block(block):
	try:
		block = block['output-primary']['physical-output']
		return block['@vintage'], block['#text'] + ' ' + block['@unit']
	except KeyError:
		return block['@year'], "0"
	

def strip_blocks(data):
	return_dict = dict()
	for year_block in data:
		year, val = process_unit_year_text_block(year_block)
		return_dict[year] = val
	return return_dict

def strip_tech_blocks(data):
	return_dict = dict()
	for year_block in data:
		year, val = process_tech_block(year_block)
		return_dict[year] = val
	return return_dict

if __name__ == '__main__':
	args = get_args()
	renewresources = load_json(args.inputFile)
	save_dict = dict()
	for renewresource in renewresources['renewresource']:
		output = strip_blocks(renewresource['output'])
		cum_prod = strip_blocks(renewresource['sub-renewable-resource']['cumulative-production'])
		max_annual_sub = strip_blocks(renewresource['sub-renewable-resource']['max-annual-subresource'])
		prod = strip_blocks(renewresource['sub-renewable-resource']['production'])
		tech = strip_tech_blocks(renewresource['sub-renewable-resource']['technology'])
		resource_dict = {'output': output,
						 'cumulative-production': cum_prod,
						 'max-annual-subresource': max_annual_sub,
						 'production': prod,
						 'technology': tech}
		save_dict[renewresource['@name']] = resource_dict
	save_json(save_dict, args.outputFile)
