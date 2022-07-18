import xmltodict
import argparse
import json

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def load_xml(input_file):
	filedict = {}
	with open(input_file, 'r') as in_xml:
		filedict = xmltodict.parse(in_xml.read())
	return filedict

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def get_DAC_potentials(gcam_dict):
	regions = gcam_dict['scenario']['world']['region']
	dac_potentials = {}
	for region in regions:
		region_name = region['@name']
		if region_name == 'USA':
			continue
		base_service_demand = region.get('energy-final-demand', {}).get('base-service', {}).get('#text', 0)
		cal_data_output = 0
		for sector in region['supplysector']:
			sector_name = sector['@name']
			if sector_name == 'CO2 removal':
				for tech in sector.get('subsector', {}).get('stub-technology', []):
					tech_name = tech['@name']
					if tech_name == 'no DAC':
						for period in tech.get('period', []):
							if period['@year'] == "2015":
								cal_data_output = period.get('CalDataOutput', {}).get('calOutputValue', 0)

		# According to Jay Fuhrman, this is by definition
		assert cal_data_output == base_service_demand
		dac_potentials[region_name] = float(base_service_demand)
	return dac_potentials

def sum_dict_vals(value_dict):
	dict_sum = 0
	for item in value_dict:
		dict_sum += value_dict[item]
	return dict_sum

def get_ratio_dict(dac_potentials, sum):
	ratio_dict = {}
	for state in dac_potentials:
		ratio_dict[state] = dac_potentials[state] / sum
	return ratio_dict

if __name__ == '__main__':
	args = get_args()
	xml_dict = load_xml(args.inputFile)
	dac_potentials = get_DAC_potentials(xml_dict)
	dict_sum = sum_dict_vals(dac_potentials)
	ratio_dict = get_ratio_dict(dac_potentials, dict_sum)
	save_json(ratio_dict, args.outputFile)
