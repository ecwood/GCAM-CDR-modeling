import json
import argparse
import os

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputDirectory', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def get_xml_files(input_dir):
	# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
	file_list = []
	for file in os.listdir(input_dir):
		if os.path.isfile(os.path.join(input_dir, file)) and file.endswith('xml'):
			file_list.append(os.path.join(input_dir, file))
	return file_list

def get_xml_tag(line):
	front_tag = line.find('<') + 1
	end_tag = line.find('>')
	return line[front_tag:end_tag].strip('/').split(' ')[0]

def get_tags_from_file(xml_file):
	tag_set = set()
	with open(xml_file, 'r') as file:
		for line in file:
			tag = get_xml_tag(line)
			if tag != "?xml":
				tag_set.add(get_xml_tag(line))
	return tag_set

if __name__ == '__main__':
	args = get_args()
	input_dir = args.inputDirectory
	xml_files = get_xml_files(input_dir)
	tags = set()
	for xml_file in xml_files:
		tags = tags | get_tags_from_file(xml_file)
	tags = list(tags)
	tags.sort()
	save_json(tags, args.outputFile)
