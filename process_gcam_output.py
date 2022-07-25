import xmltodict
import argparse
import pickle
import json
import datetime

def get_date():
	return datetime.datetime.now().ctime()

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	parser.add_argument('--savePickle', action='store_true')
	parser.add_argument('--loadPickle', action='store_true')
	return parser.parse_args()


def combine_value_and_unit(value_dict):
	return value_dict.get('#text', '') + ' ' + value_dict.get('@unit', '')

def get_temperature(gcam_dict):
	temperature_dict = {}
	scenario = gcam_dict['scenario']
	world = scenario['world']
	temperatures = world['climate-model']['global-mean-temperature']
	for temperature_year in temperatures:
		year = temperature_year['@year']
		change = temperature_year['#text']
		temperature_dict[year] = change
	return temperature_dict

def get_CO2_removed(gcam_dict):
	co2_removed = {}
	world = gcam_dict['scenario']['world']
	for region in world['region']:
		region_name = region['@name']
		supplysector_list = region['supplysector']
		sectors = []
		for sector in supplysector_list:
			sector_name = sector['@name']
			if sector_name == "CO2 removal":
				techs = sector['subsector']['technology']
				for tech in techs:
					dactype = tech.get('@name', '')
					tech_year = tech.get('@year', '')
					tech_cost = combine_value_and_unit(tech.get('cost', {}))
					tech_output = combine_value_and_unit(tech.get('output-primary', {}).get('physical-output', {}))
					co2_removed.setdefault(region_name, {}).setdefault(dactype, {})[tech_year] = {'cost': tech_cost, 'output': tech_output}
	return co2_removed

if __name__ == '__main__':
	print(get_date())
	args = get_args()
	input_file = args.inputFile
	pickle_file = input_file.replace('xml', 'pickle')
	output_file = args.outputFile
	filedict = {}
	if args.loadPickle:
		with open(pickle_file, 'rb') as pickle_in:
			filedict = pickle.load(pickle_in)
	else:
		with open(input_file, 'r') as in_xml:
			filedict = xmltodict.parse(in_xml.read())
			if args.savePickle:
				with open(pickle_file, 'wb') as pickle_out:
					pickle.dump(filedict, pickle_out)
	print("Data Loaded at " + str(get_date()))
	with open(output_file, 'w') as out_json:
		out_json.write(json.dumps(get_CO2_removed(filedict), indent=4, sort_keys=True))
	print(get_date())