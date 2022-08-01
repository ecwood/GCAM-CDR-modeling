import json
import argparse
import datetime
import re

SCENARIO_REGEX = '<scenario name="(.*)" date="(.*)">'
REGION_REGEX = '<region name="(.*)" type="region">'
SUPPLYSECTOR_REGEX = '<supplysector name="CO2 removal" type="sector">'
SUBSECTOR_REGEX = '<subsector name="dac" type="subsector">'
TECH_REGEX = '<technology year="(.*)" name="(.*)" type="technology">'
COST_REGEX = '<cost unit="(.*)" year="(.*)">(.*)<\/cost>'
CO2_REMOVAL_REGEX = '<CO2 name="CO2" type="GHG">'
REMOVED_REGEX = '<emissions-sequestered unit="(.*)" year="(.*)">(.*)<\/emissions-sequestered>'
TECH_END_REGEX = '</technology>'
SUBSECTOR_END_REGEX = '</subsector>'
SUPPLYSECTOR_END_REGEX = '</supplysector>'
REGION_END_REGEX = '</region>'

def get_date():
	return datetime.datetime.now().ctime()

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def check_scenario(line):
	mat_chk = re.match(SCENARIO_REGEX, line)
	if mat_chk:
		return {'name': mat_chk[1], 'date': mat_chk[2]}
	return False

def check_region(line):
	mat_chk = re.match(REGION_REGEX, line)
	if mat_chk:
		return {'region': mat_chk[1]}
	return False

def check_supplysector(line):
	mat_chk = re.match(SUPPLYSECTOR_REGEX, line)
	if mat_chk:
		return True
	return False

def check_subsector(line):
	mat_chk = re.match(SUBSECTOR_REGEX, line)
	if mat_chk:
		return True
	return False

def check_tech(line):
	mat_chk = re.match(TECH_REGEX, line)
	if mat_chk:
		return {'year': mat_chk[1], 'name': mat_chk[2]}
	return False

def check_cost(line):
	mat_chk = re.match(COST_REGEX, line)
	if mat_chk:
		return {'unit': mat_chk[1], 'year': mat_chk[2], 'cost': mat_chk[3]}
	return False

def check_co2_removal(line):
	mat_chk = re.match(CO2_REMOVAL_REGEX, line)
	if mat_chk:
		return True
	return False

def check_removed(line):
	mat_chk = re.match(REMOVED_REGEX, line)
	if mat_chk:
		return {'unit': mat_chk[1], 'year': mat_chk[2], 'value': mat_chk[3]}
	return {}

def check_subsector_end(line):
	mat_chk = re.match(SUBSECTOR_END_REGEX, line)
	if mat_chk:
		return True
	return False

def check_supplysector_end(line):
	mat_chk = re.match(SUPPLYSECTOR_END_REGEX, line)
	if mat_chk:
		return True
	return False

def check_region_end(line):
	mat_chk = re.match(REGION_END_REGEX, line)
	if mat_chk:
		return True
	return False

def check_tech_end(line):
	mat_chk = re.match(TECH_END_REGEX, line)
	if mat_chk:
		return True
	return False

def isdict(val):
	return isinstance(val, dict)

def process_file(filename):
	file_dict = {}
	SCENARIO = False
	scenario_name = ""
	scenario_date = ""
	REGION = True
	region_name = ""
	SUPPLYSECTOR = False
	SUBSECTOR = False
	TECH = False
	tech_year = ""
	tech_name = ""
	cost = ""
	CO2_REMOVAL = False
	with open(filename, 'r') as file:
		line_num = 0
		for line in file:
			line_num += 1
			if line_num % 10000000 == 0:
				print(line_num)
				# print(SCENARIO, REGION, SUPPLYSECTOR, SUBSECTOR, TECH, CO2_REMOVAL)
			line = line.strip()
			scen_val = check_scenario(line)
			SCENARIO |= isdict(scen_val)
			if isdict(scen_val):
				scenario_name = scen_val['name']
				scenario_date = scen_val['date']
			if SCENARIO:
				reg_val = check_region(line)
				REGION |= isdict(reg_val)
				if isdict(reg_val):
					region_name = reg_val['region']
			if REGION:
				SUPPLYSECTOR |= check_supplysector(line)
			if SUPPLYSECTOR:
				SUBSECTOR |= check_subsector(line)
			if SUBSECTOR:
				tech_val = check_tech(line)
				TECH |= isdict(tech_val)
				if isdict(tech_val):
					tech_year = tech_val['year']
					tech_name = tech_val['name']
			if TECH:
				cost_val = check_cost(line)
				if isdict(cost_val):
					cost = cost_val['cost'] + ' ' + cost_val['unit']
				CO2_REMOVAL |= check_co2_removal(line)
			if CO2_REMOVAL:
				removed_vals = check_removed(line)
				# print(removed_vals, line)
				if removed_vals.get('year', None) == tech_year:
					file_dict.setdefault(scenario_name, {}).setdefault(region_name, {}).setdefault(tech_name, {})[tech_year] = {'cost': cost, 'co2 removed': removed_vals.get('value', '') + ' ' + removed_vals.get('unit', '')}
					CO2_REMOVAL = False
					TECH = False
			if check_tech_end(line):
				TECH = False
			if check_subsector_end(line):
				SUBSECTOR = False
			if check_supplysector_end(line):
				SUPPLYSECTOR = False
			if check_region_end(line):
				REGION = False
	return file_dict

if __name__ == '__main__':
	args = get_args()
	file_dict = process_file(args.inputFile)
	save_json(file_dict, args.outputFile)

	'''
<scenario name="GCAM-USA_Reference" date="2022-18-7T22:03:41-00:00">
	<world>
		<region name="WY" type="region">
				<supplysector name="CO2 removal" type="sector">
					<subsector name="dac" type="subsector">
						<technology year="2100" name="lowtemp DAC heatpump" type="technology">
							<cost unit="1975$/kg" year="2100">452.349</cost>
							<output-primary name="CO2 removal" type="output">
									<physical-output unit="Mt" vintage="2100">0.0509629</physical-output>
							</output-primary>
							<CO2 name="CO2" type="GHG">
									<emissions-sequestered unit="MTC" year="2100">0.0509629</emissions-sequestered>
							</CO2>
							<input-energy name="airCO2" type="input">
									<demand-physical unit="Mt" vintage="2100">0.0509629</demand-physical>
									<IO-coefficient unit="unitless" vintage="2100">1</IO-coefficient>
									<carbon-content unit="MTC" vintage="2100">0.0509629</carbon-content>
							</input-energy>
							<input-energy name="elect_td_ind" type="input">
									<demand-physical unit="EJ" vintage="2100">0.000474984</demand-physical>
									<IO-coefficient unit="unitless" vintage="2100">0.0093202</IO-coefficient>
							</input-energy>
							<input-non-energy name="non-energy" type="input">
									<price-paid unit="1975$/kg" vintage="2100">0.2035</price-paid>
							</input-non-energy>
						</technology>
					</subsector>
				</supplysector>
		</region>
	</world>
</scenario>
'''