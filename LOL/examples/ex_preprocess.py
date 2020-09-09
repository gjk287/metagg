import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src\\preprocess\\tests'))
from test_preprocess_gamepedia import preprocess_and_save as pas_gamepedia

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src\\preprocess'))
from preprocess_create_table import preprocess_and_save as pas_create_table
from preprocess_matchschedule import preprocess_and_save as pas_matchschedule

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from database import DB
from utils import tableUniqueKey, tablePK_dict

db = DB()
db.initialise()

def main():
	# # create league, betting_site, bet_type table and input to DB
	# table_name = 'league'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# table_name = 'betting_site'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# table_name = 'bet_type_special'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# table_name = 'bet_type_ou'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# table_name = 'bet_type_handicap'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# table_name = 'bet_type_both'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# # preprocess gamepedia data
	# pas_gamepedia('game_schedule')

	# # create team, match and input to DB
	# table_name = 'team'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# table_name = 'match'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# table_name = 'match_info_by_team'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	table_name = 'set_match'
	preprocess_and_input(table_name)
	input_to_csv(table_name)
	
	
	
	#pas_gamepedia('match_history_url')



def preprocess_and_input(table_name=None):
	if table_name == 'league':
		pas_create_table(table_name)

	elif table_name == 'betting_site':
		pas_create_table(table_name)

	elif table_name == 'bet_type_special':
		pas_create_table('bet_type', table_name)

	elif table_name == 'bet_type_ou':
		pas_create_table('bet_type', table_name)

	elif table_name == 'bet_type_handicap':
		pas_create_table('bet_type', table_name)
		db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique.csv', dtype={'handicap_amount':str}), table_name)
		return

	elif table_name == 'bet_type_both':
		pas_create_table('bet_type', table_name)

	elif table_name == 'team':
		pas_matchschedule(table_name)

	elif table_name == 'match':
		pas_matchschedule(table_name)

	elif table_name == 'match_info_by_team':
		pas_matchschedule(table_name)

	elif table_name == 'set_match':
		pas_matchschedule(table_name)


	db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique.csv'), table_name)
	return

	
def input_to_csv(table_name=None):
	temp_df = db.get_table(table_name)
	temp_df = temp_df[tableUniqueKey[table_name] + [tablePK_dict[table_name]]]
	temp_df.to_csv(f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_pk.csv', index=False)
	return

if __name__ == "__main__":
	main()