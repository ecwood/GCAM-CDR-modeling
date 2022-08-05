import json
import argparse
import datetime
import re

SCENARIO_REGEX = '<scenario name="(.*)" date="(.*)">'
REGION_REGEX = '<region name="(.*)" type="region">'
SUPPLYSECTOR_DAC_REGEX = '<supplysector name="CO2 removal" type="sector">'
SUPPLYSECTOR_SOLAR_REGEX = '<supplysector name="electricity" type="sector">'
NESTING_SUBSECTOR_SOLAR_USA_REGEX = '<nesting-subsector name="solar" type="subsector">'
SUBSECTOR_DAC_REGEX = '<subsector name="dac" type="subsector">'
SUBSECTOR_SOLAR_REGEX = '<subsector name="(.*)" type="subsector">'
SUBSECTOR_SOLAR_REGEX_USA = '<subsector depth="1" name="(.*)" type="subsector">'
TECH_DAC_REGEX = '<technology year="(.*)" name="(.*)" type="technology">'
TECH_SOLAR_REGEX_GLOBAL = '<intermittent-technology year="(.*)" name="(.*)" type="technology">'
TECH_SOLAR_REGEX_USA = '<technology year="(.*)" name="(.*)" type="technology">'
COST_REGEX = '<cost unit="(.*)" year="(.*)">(.*)<\/cost>'
CO2_REMOVAL_REGEX = '<CO2 name="CO2" type="GHG">'
SOLAR_OUTPUT_REGEX = '<output-primary name="(.*)" type="output">'
REMOVED_DAC_REGEX = '<emissions-sequestered unit="(.*)" year="(.*)">(.*)<\/emissions-sequestered>'
SOLAR_ELEC_REGEX = '<physical-output unit="(.*)" vintage="(.*)">(.*)<\/physical-output>'
TECH_END_REGEX = '</technology>'
INTER_TECH_END_REGEX = '</intermittent-technology>'
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

def check_supplysector_dac(line):
	mat_chk = re.match(SUPPLYSECTOR_DAC_REGEX, line)
	if mat_chk:
		return True
	return False

def check_supplysector_solar(line):
	mat_chk_gl = re.match(SUPPLYSECTOR_SOLAR_REGEX, line)
	mat_chk_usa = re.match(NESTING_SUBSECTOR_SOLAR_USA_REGEX, line)
	if mat_chk_gl or mat_chk_usa:
		return True
	return False

def check_subsector_dac(line):
	mat_chk = re.match(SUBSECTOR_DAC_REGEX, line)
	if mat_chk:
		return True
	return False

def check_subsector_solar(line):
	mat_chk_gl = re.match(SUBSECTOR_SOLAR_REGEX, line)
	mat_chk_usa = re.match(SUBSECTOR_SOLAR_REGEX_USA, line)
	if mat_chk_gl or mat_chk_usa:
		return True
	return False

def check_tech_dac(line):
	mat_chk = re.match(TECH_DAC_REGEX, line)
	if mat_chk:
		return {'year': mat_chk[1], 'name': mat_chk[2]}
	return False

def check_tech_solar(line):
	mat_chk_gl = re.match(TECH_SOLAR_REGEX_GLOBAL, line)
	mat_chk_usa = re.match(TECH_SOLAR_REGEX_USA, line)
	if mat_chk_gl:
		return {'year': mat_chk_gl[1], 'name': mat_chk_gl[2]}
	if mat_chk_usa:
		return {'year': mat_chk_usa[1], 'name': mat_chk_usa[2]}
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

def check_solar_output(line):
	mat_chk = re.match(SOLAR_OUTPUT_REGEX, line)
	if mat_chk:
		return True
	return False

def check_removed(line):
	mat_chk = re.match(REMOVED_DAC_REGEX, line)
	if mat_chk:
		return {'unit': mat_chk[1], 'year': mat_chk[2], 'value': mat_chk[3]}
	return {}

def check_solar_elec(line):
	mat_chk = re.match(SOLAR_ELEC_REGEX, line)
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

def check_tech_dac_end(line):
	mat_chk = re.match(TECH_END_REGEX, line)
	if mat_chk:
		return True
	return False

def check_tech_solar_end(line):
	mat_chk = re.match(INTER_TECH_END_REGEX, line)
	if mat_chk:
		return True
	return False

def isdict(val):
	return isinstance(val, dict)

def is_state(name):
	return len(name) == 2

def process_file(filename):
	file_dict = {}
	SCENARIO = False
	scenario_name = ""
	scenario_date = ""
	REGION = False
	region_name = ""
	SUPPLYSECTOR_DAC = False
	SUPPLYSECTOR_SOLAR = False
	SUBSECTOR_DAC = False
	SUBSECTOR_SOLAR = False
	TECH_DAC = False
	TECH_SOLAR = False
	tech_dac_year = ""
	tech_solar_year = ""
	tech_dac_name = ""
	tech_solar_name = ""
	cost_dac = ""
	cost_solar = ""
	CO2_REMOVAL = False
	SOLAR_OUTPUT = False
	with open(filename, 'r') as file:
		line_num = 0
		for line in file:
			line_num += 1
			if line_num % 10000000 == 0:
				print(line_num)
#			if is_state(region_name) and SUPPLYSECTOR_SOLAR and SUBSECTOR_SOLAR and TECH_SOLAR and SOLAR_OUTPUT:
#				print(region_name)
#				print(SCENARIO, REGION, SUPPLYSECTOR_SOLAR, SUBSECTOR_SOLAR, TECH_SOLAR, SOLAR_OUTPUT)
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
				SUPPLYSECTOR_DAC |= check_supplysector_dac(line)
				SUPPLYSECTOR_SOLAR |= check_supplysector_solar(line)
			if SUPPLYSECTOR_DAC:
				SUBSECTOR_DAC |= check_subsector_dac(line)
			if SUPPLYSECTOR_SOLAR:
				SUBSECTOR_SOLAR |= check_subsector_solar(line)
			if SUBSECTOR_DAC:
				tech_dac_val = check_tech_dac(line)
				TECH_DAC |= isdict(tech_dac_val)
				if isdict(tech_dac_val):
					tech_dac_year = tech_dac_val['year']
					tech_dac_name = tech_dac_val['name']
			if SUBSECTOR_SOLAR:
				tech_solar_val = check_tech_solar(line)
				TECH_SOLAR |= isdict(tech_solar_val)
				if isdict(tech_solar_val):
					tech_solar_year = tech_solar_val['year']
					tech_solar_name = tech_solar_val['name']
			if TECH_DAC:
				cost_val = check_cost(line)
				if isdict(cost_val):
					cost_dac = cost_val['cost'] + ' ' + cost_val['unit']
				CO2_REMOVAL |= check_co2_removal(line)
			if TECH_SOLAR:
				cost_val = check_cost(line)
				if isdict(cost_val):
					cost_solar = cost_val['cost'] + ' ' + cost_val['unit']
				SOLAR_OUTPUT |= check_solar_output(line)
			if CO2_REMOVAL:
				removed_vals = check_removed(line)
				# print(removed_vals, line)
				if removed_vals.get('year', None) == tech_dac_year:
					file_dict.setdefault(scenario_name, {}).setdefault(region_name, {}).setdefault(tech_dac_name, {})[tech_dac_year] = {'cost': cost_dac, 'co2 removed': removed_vals.get('value', '') + ' ' + removed_vals.get('unit', '')}
					CO2_REMOVAL = False
					TECH_DAC = False
			if SOLAR_OUTPUT:
				solar_elec_vals = check_solar_elec(line)
				# print(removed_vals, line)
				if solar_elec_vals.get('year', None) == tech_solar_year:
					file_dict.setdefault(scenario_name, {}).setdefault(region_name, {}).setdefault(tech_solar_name, {})[tech_solar_year] = {'cost': cost_solar, 'energy': solar_elec_vals.get('value', '') + ' ' + solar_elec_vals.get('unit', '')}
					SOLAR_OUTPUT = False
					TECH_SOLAR = False
			if check_tech_dac_end(line):
				TECH_DAC = False
			if check_tech_solar_end(line):
				TECH_SOLAR = False
			if check_subsector_end(line):
				SUBSECTOR_DAC = False
				SUBSECTOR_SOLAR = False
			if check_supplysector_end(line):
				SUPPLYSECTOR_DAC = False
				SUPPLYSECTOR_SOLAR = False
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