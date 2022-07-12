import xmltodict
import json
import argparse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

if __name__ == '__main__':
	args = get_args()
	input_file = args.inputFile
	output_file = args.outputFile
	filedict = {}
	with open(input_file, 'r') as in_xml:
		filedict = xmltodict.parse(in_xml.read())
	out_dict = json.dumps(filedict, indent=4, sort_keys=True)
	with open(output_file, 'w') as out_json:
		out_json.write(out_dict)