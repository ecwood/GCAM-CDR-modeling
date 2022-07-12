import xmltodict
import argparse
import pickle

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	parser.add_argument('--savePickle', action='store_true')
	parser.add_argument('--loadPickle', action='store_true')
	return parser.parse_args()

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

if __name__ == '__main__':
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
	print(get_temperature(filedict))