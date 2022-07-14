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

def format_num(value, unit):
	return value + ' ' + unit


def process_carbon_storage_data(c_data):
	output_dict = {}
	for region in c_data['scenario']['world']['region']:
		region_name = region['@name']
		resource = region['resource']['subresource']
		output_unit = region['resource']['output-unit']
		price_unit = region['resource']['price-unit']
		resource_name = resource['@name']
		grades = {}
		for grade in resource['grade']:
			grade_name = grade['@name']
			quantity_available = format_num(grade['available'], output_unit)
			extraction_cost = format_num(grade['extractioncost'], price_unit)
			grades[grade_name] = {'Quantity Available': quantity_available,
								  'Extraction Cost': extraction_cost}
		unlimited_resource = region['unlimited-resource']['@name']
		region_dict = {resource_name: grades, 'Unlimited Resource': unlimited_resource}
		output_dict[region_name] = region_dict
	return output_dict



if __name__ == '__main__':
	args = get_args()
	data = load_xml(args.inputFile)
	save_json(process_carbon_storage_data(data), args.outputFile)
