import argparse
import xmltodict
import json

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def save_xml(out_dict, output_file):
	with open(output_file, 'w') as out_xml:
		xml_out_str = xmltodict.unparse(out_dict, pretty=True)
		out_xml.write(xml_out_str)

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

def process_csv(csv_load):
	processed_csv_dict = {}
	for csv_line in csv_load:
		region = csv_line['region']
		dactype = csv_line['type']
		value = csv_line['value']
		year = csv_line['year']
		processed_csv_dict.setdefault(region, {}).setdefault(year, {})[dactype] = value
	return processed_csv_dict

def format_constraint(year, year_data):
	dac_sum = 0
	for item in year_data:
		dac_sum += float(year_data[item])
	return {'#text': str(dac_sum), '@year': year}

def format_regional_policy(region, region_data):
	constraints = [format_constraint(year, region_data[year]) for year in region_data]
	return {'@name': region, "policy-portfolio-standard": {'@name': "DAC-floor", 'constraint': constraints}}

def format_policy_file(csv_data):
	regions = [format_regional_policy(region, csv_data[region]) for region in csv_data]
	return {'scenario': {'world': {'region': regions}}}

if __name__ == '__main__':
	args = get_args()
	csv_vals = process_csv(read_csv(args.inputFile))
	policy_file = format_policy_file(csv_vals)
	save_xml(policy_file, args.outputFile)