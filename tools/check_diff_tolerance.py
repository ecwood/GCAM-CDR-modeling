import argparse
import json

RED_LINE = 1
BLUE_LINE = 2
BREAK_LINE = 3
INTRO_LINE = 4

STARTING_INTRO = 'starting_intro'
BLUE_LINE_KEY = 'blue'
RED_LINE_KEY = 'red'

TOLERANCE = 0.1
TOLERATED = 'Tolerated'

NOT_A_NUM = 'NOT_A_NUMBER_CODE'

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	return parser.parse_args()

def get_line_type(line):
	intro_char = line[0]
	if intro_char == '<':
		return RED_LINE
	if intro_char == '>':
		return BLUE_LINE
	if intro_char == '-':
		return BREAK_LINE
	return INTRO_LINE

def format_line(line):
	line = line[1:].strip().replace('"', "'")
	return extract_number(line)

def process_diff_file(diff_filename):
	diff_dict = {}
	with open(diff_filename) as diff_file:
		red_list = []
		blue_list = []
		intro_line = STARTING_INTRO
		for line in diff_file:
			line_type = get_line_type(line)
			if line_type == INTRO_LINE:
				if intro_line != STARTING_INTRO:
					diff_dict[intro_line][BLUE_LINE_KEY] = blue_list
					blue_list = []
				intro_line = line.strip()
				diff_dict[intro_line] = dict()
			elif line_type == RED_LINE:
				red_list.append(format_line(line))
			elif line_type == BLUE_LINE:
				blue_list.append(format_line(line))
			elif line_type == BREAK_LINE:
				diff_dict[intro_line][RED_LINE_KEY] = red_list
				red_list = []
			else:
				assert(False)
	return diff_dict

def extract_number(line):
	original_line = line
	num_start = line.find('>') + 1
	line = line[num_start:]
	num_end = line.find('<')
	try:
		num = float(line[:num_end])
	except ValueError:
		return [original_line, NOT_A_NUM]
	return [num, line[num_end + 2:].strip('>')]

def average(num1, num2):
	return (float(num1) + float(num2)) / 2.0

def get_percent_difference(num1, num2):
	return abs(num1 - num2) / average(num1, num2)

def under_tolerance(num1, num2):
	if num1 == num2:
		return True
	return get_percent_difference(num1, num2) < TOLERANCE

def unwind_diffs(item, blue_diff, red_diff):
	return_list = []
	if len(blue_diff) != len(red_diff):
		return "Skipping"
	for x in range(len(blue_diff)):
		blue_item = blue_diff[x]
		red_item = red_diff[x]
		if blue_item[1] != NOT_A_NUM and red_item[1] != NOT_A_NUM:
			tolerated = under_tolerance(blue_item[0], red_item[0]) and (blue_item[1] == red_item[1])
		else:
			tolerated = True
		if tolerated == False:
			entry = {'Blue Value': blue_item[0], 'Red Value': red_item[0]}
			return_list.append(entry)
	if len(return_list) == 0:
		return TOLERATED
	return return_list

if __name__ == '__main__':
	args = get_args()
	diff_file_dict = process_diff_file(args.inputFile)
	diff_file_dict_dup = {}
	for item in diff_file_dict:
		blue_diff = diff_file_dict[item].get(BLUE_LINE_KEY, [])
		red_diff = diff_file_dict[item].get(RED_LINE_KEY, [])
		diffs_check = unwind_diffs(item, blue_diff, red_diff)
		if diffs_check != TOLERATED:
			diff_file_dict_dup[item] = diffs_check
	print(json.dumps(diff_file_dict_dup, indent=4, sort_keys=True))