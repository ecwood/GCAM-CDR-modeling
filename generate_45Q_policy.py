import json
import xmltodict
import argparse

TIMESTEP = 5
ENDING_YEAR = 2100

# https://www.in2013dollars.com/us/inflation/1975?amount=1
INFLATION_1975 = 5.51

# https://www.in2013dollars.com/us/inflation/1990?amount=1
INFLATION_1990 = 2.27

INFLATION_RATES = {1975: INFLATION_1975, 1990: INFLATION_1990}

SIZE_UNITS = {'t': 1, 'kg': 0.001, 'Mt': 1000000}

C_TO_CO2 = 0.2729214479

DAC_TECHS = ['hightemp DAC NG', 'hightemp DAC elec', 'lowtemp DAC heatpump']

STATES  = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
		   'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI',
		   'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV',
		   'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT',
		   'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--initialValue', nargs=1, type=float)
	parser.add_argument('--interestRate', nargs=1, type=float)
	parser.add_argument('--startingYear', nargs=1, type=int)
	parser.add_argument('--outputPriceYear', nargs=1, type=int)
	parser.add_argument('--outputPriceSizeUnit', nargs=1, type=str)
	parser.add_argument('--scenarioName', nargs=1, type=str)
	parser.add_argument('--subsidyName', nargs=1, type=str)
	parser.add_argument('outputFile', type=str)
	return parser.parse_args()

def load_json(filename):
	with open(filename, 'r') as file:
		return json.load(file)

def save_json(data, output_file):
	with open(output_file, 'w') as output_json:
		output_json.write(json.dumps(data, indent=4, sort_keys=True))

def save_xml(out_dict, output_file):
	with open(output_file, 'w') as out_xml:
		xml_out_str = xmltodict.unparse(out_dict, pretty=True)
		out_xml.write(xml_out_str)

def calculate_45Q_levels(initial_value, inflation_rate, starting_year, output_price_year, output_size_unit):
	subsidy_dict = dict()
	## Are units kgC or kgCO2??!!!
	## ASSUMING C:
	initial_value = initial_value / C_TO_CO2
	initial_value = initial_value / INFLATION_RATES[output_price_year]
	initial_value = initial_value * SIZE_UNITS[output_size_unit]

	for year in range(starting_year, ENDING_YEAR + TIMESTEP, TIMESTEP):
		subsidy_dict[year] = initial_value * pow(1 + inflation_rate, year - starting_year)
	return subsidy_dict, str(output_price_year) + '$/' + output_size_unit

def format_supplysector_info(subsidy_name, starting_year):
	periods = []
	for year in range(starting_year, ENDING_YEAR + TIMESTEP, TIMESTEP):
		periods.append({'@year': year, 'input-subsidy': {'@name': subsidy_name}})
	stub_techs = []
	for tech in DAC_TECHS:
		stub_techs.append({'@name': tech, 'period': periods})
	return {'@name': "CO2 removal",
			'subsector': {'@name': 'dac', 'stub-technology': stub_techs}}

def format_fixed_tax(subsidy_dict):
	fixed_taxes = []
	for year in subsidy_dict:
		fixed_taxes.append({'@year': year, '#text': str(subsidy_dict[year])})
	return fixed_taxes

def format_45Q_data(subsidy_dict, price_unit, scenario_name, subsidy_name, starting_year):
	regions = []
	for state in STATES:
		region = {'@name': state,
				  'policy-portfolio-standard': {'@name': subsidy_name,
				  								'market': 'USA',
				  								'fixedTax': format_fixed_tax(subsidy_dict),
				  								'policyType': 'subsidy',
				  								'price-unit': price_unit},
				  'supplysector': format_supplysector_info(subsidy_name, starting_year)}
		regions.append(region)
	return {'scenario': {'@name': scenario_name, 'world': {'region': regions}}}

if __name__ == '__main__':
	args = get_args()
	initial_value = args.initialValue[0]
	interest_rate = args.interestRate[0]
	starting_year = args.startingYear[0]
	output_price_year = args.outputPriceYear[0]
	output_price_size_unit = args.outputPriceSizeUnit[0]
	scenario_name = args.scenarioName[0]
	subsidy_name = args.subsidyName[0]

	subsidy_dict, price_unit = calculate_45Q_levels(initial_value, interest_rate, starting_year, output_price_year, output_price_size_unit)
	subsidy_formatted = format_45Q_data(subsidy_dict, price_unit, scenario_name, subsidy_name, starting_year)
	save_xml(subsidy_formatted, args.outputFile)
