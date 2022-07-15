import argparse

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('cropLength', type=int)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()


if __name__ == '__main__':
	args = get_args()
	input_filename = args.inputFile
	lines = args.cropLength
	output_filename = args.outputFile

	out_string = ""
	with open(input_filename, 'r') as input_file:
		line_count = 0
		for line in input_file:
			line_count += 1
			if line_count <= lines:
				out_string += line
			else:
				break

	with open(output_filename, 'w') as output_file:
		output_file.write(out_string)