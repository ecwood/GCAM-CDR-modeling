import argparse
import json
import datetime
import re

NAME_REGEX = '<(.*) name="(.*)"'

def get_date():
	return datetime.datetime.now().ctime()

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def get_name(line):
	matchk = re.match(NAME_REGEX, line)
	if matchk:
		label = matchk[1].split(' ')[0]
		name = matchk[2].split('"')[0]
		return label, name
	return None, None

def get_name_tags(filename):
	name_tags = dict()
	with open(filename, 'r') as file:
		line_num = 0
		for line in file:
			line_num += 1
			if line_num % 10000000 == 0:
				print(line_num)
			line = line.strip()
			label, name = get_name(line)
			if name is not None:
				name_tags.setdefault(label, set()).add(name)
	for label in name_tags:
		name_tags[label] = list(name_tags[label])
	return name_tags

if __name__ == '__main__':
	print(get_date())
	args = get_args()
	name_tags = get_name_tags(args.inputFile)
	save_json(name_tags, args.outputFile)
	print(get_date())