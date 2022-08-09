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
	distributed_solar = load_json(args.inputFile)
	output = strip_blocks(distributed_solar['output'])
	cum_prod = strip_blocks(distributed_solar['sub-renewable-resource']['cumulative-production'])
	max_annual_sub = strip_blocks(distributed_solar['sub-renewable-resource']['max-annual-subresource'])
	prod = strip_blocks(distributed_solar['sub-renewable-resource']['production'])
	tech = strip_tech_blocks(distributed_solar['sub-renewable-resource']['technology'])
	save_dict = {'output': output,
				 'cumulative-production': cum_prod,
				 'max-annual-subresource': max_annual_sub,
				 'production': prod,
				 'technology': tech}
	save_json(save_dict, args.outputFile)
