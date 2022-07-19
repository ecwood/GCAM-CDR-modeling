import xmltodict
import json
import argparse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputXMLFile', type=str)
	parser.add_argument('inputCSVFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def load_xml(input_file):
	filedict = {}
	with open(input_file, 'r') as in_xml:
		filedict = xmltodict.parse(in_xml.read())
	return filedict

def save_xml(out_dict, output_file):
	with open(output_file, 'w') as out_xml:
		xml_out_str = xmltodict.unparse(out_dict, pretty=True)
		out_xml.write(xml_out_str)

def gcamify_fixedoutput(year, val):
	return {'@year': year, "fixedOutput": val, "share-weight": 0}

def edit_file(xml_dict, new_data):
	# Path to edit DAC deployment:
	# scenario---world---region (L)---supplysector (L - "CO2 removal") ---subsector---stub-technology (L - edit these dictionaries)
	region_index = 0
	for region in xml_dict['scenario']['world']['region']:
		sector_index = 0
		regional_data = new_data.get(region['@name'], {})
		if len(regional_data) == 0:
			region_index += 1
			continue
		for sector in region['supplysector']:
			if sector['@name'] == "CO2 removal":
				for tech in xml_dict['scenario']['world']['region'][region_index]['supplysector'][sector_index]['subsector']['stub-technology']:
					tech_name = tech['@name']
					tech_data = regional_data.get(tech_name, {})
					if tech_data == {}:
						continue
					if tech.get('period', None) == None:
						tech['period'] = []
						for year in tech_data:
							tech['period'].append(gcamify_fixedoutput(year, tech_data[year]))
					else:
						for period in tech['period']:
							for year in tech_data:
								if year == period['@year']:
									period['fixedOutput'] = tech_data[year]
									period['share-weight'] = 0
			sector_index += 1
		region_index += 1
	return xml_dict

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
		processed_csv_dict.setdefault(region, {}).setdefault(dactype, {})[year] = value
	return processed_csv_dict

if __name__ == '__main__':
	args = get_args()
	xml_dict = load_xml(args.inputXMLFile)
	csv_load = read_csv(args.inputCSVFile)
	processed_csv_dict = process_csv(csv_load)
	xml_dict = edit_file(xml_dict, processed_csv_dict)
	save_xml(xml_dict, args.outputFile)
