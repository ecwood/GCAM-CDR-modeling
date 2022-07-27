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
					tech_output = tech.get('output-primary', {}).get('physical-output', {})
					if isinstance(tech_output, list):
						tech_output_copy = tech_output
						for list_year_item in tech_output_copy:
							list_year = list_year_item['@vintage']
							if tech_year == list_year:
								tech_output = list_year_item
								break
					co2_removed.setdefault(region_name, {}).setdefault(dactype, {})[tech_year] = {'cost': tech_cost, 'output': combine_value_and_unit(tech_output)}
	return co2_removed

def get_carbon_prices(gcam_dict):
	carbon_prices = {}
	marketplace = gcam_dict['scenario']['world']['Marketplace']['market']
	for market in marketplace:
		if 'CO2' in market['@name']:
			market_region = market.get('MarketRegion', '')
			market_task = market.get('MarketGoodOrFuel', '')
			market_year = market.get('@year', '')
			price = combine_value_and_unit(market.get('price', {}))
			supply = combine_value_and_unit(market.get('supply', {}))
			demand = combine_value_and_unit(market.get('demand', {}))
			carbon_prices.setdefault(market_region, {}).setdefault(market_task, {})[market_year] = {'price': price, 'supply': supply, 'demand': demand}
	return carbon_prices

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
		co2_removed = get_CO2_removed(filedict)
		temperature = get_temperature(filedict)
		carbon_prices = get_carbon_prices(filedict)
		out_json.write(json.dumps({"CO2 Removed": co2_removed, "Temperature": temperature, "Markets": carbon_prices}, indent=4, sort_keys=True))
	print(get_date())