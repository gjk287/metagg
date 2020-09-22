import pandas as pd
import glob
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src\\preprocess\\tests'))
from test_preprocess_gamepedia import preprocess_and_save as pas_gamepedia
from test_preprocess_oracleelixir import preprocess_and_save as pas_oracleelixir
from test_preprocess_matchhistory import preprocess_and_save as pas_matchhistory

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

	# table_name = 'set_match'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)
	
	# table_name = 'set_match_info_by_team'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)
	
	# table_name = 'player'
	# preprocess_and_input(table_name, data_name='oracle_elixir')
	# input_to_csv(table_name)

	# table_name = 'champion'
	# preprocess_and_input(table_name, data_name='oracle_elixir')
	# input_to_csv(table_name)

	# ## get patch for match table from oracle elixir
	# table_name = 'match'
	# preprocess_and_input(table_name, data_name='oracle_elixir')

	# ## get ckpm, gamelength for set_match table from oracle elixir
	# table_name = 'set_match'
	# preprocess_and_input(table_name, data_name='oracle_elixir')

	# ## get all other columns for set_match_info_by_team from oracle elixir
	# table_name = 'set_match_info_by_team'
	# preprocess_and_input(table_name, data_name='oracle_elixir')

	# ## create set_match_player_performance unique table 
	# table_name = 'set_match_player_performance'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# ## get all other columns for set_match_player_performance from oracle elixir
	# table_name = 'set_match_player_performance'
	# preprocess_and_input(table_name, data_name='oracle_elixir')

	# # get set_match_url table
	# table_name = 'set_match_url'
	# preprocess_and_input(table_name)
	# input_to_csv(table_name)

	# # get player from mvp table and input mvp for set match
	# table_name = 'player'
	# preprocess_and_input(table_name, data_name='gamepedia')
	# input_to_csv(table_name)
	# table_name = 'set_match'
	# preprocess_and_input(table_name, data_name='gamepedia')

	# # get team table again from match history and input to DB
	# table_name = 'player'
	# preprocess_and_input(table_name, 'match_history')
	# input_to_csv(table_name)

	# # get champion table again from match history and input to DB
	# table_name = 'champion'
	# preprocess_and_input(table_name, 'match_history')
	# input_to_csv(table_name)

	# # get ckpm, gamelength from match history and input to DB
	# table_name = 'set_match'
	# preprocess_and_input(table_name, 'match_history')
	# input_to_csv(table_name)

	# # get set_match_info_by_team table from match history data
	# table_name = 'set_match_info_by_team'
	# preprocess_and_input(table_name, 'match_history')

	# get set_match_player_performance table from match history data
	table_name = 'set_match_player_performance'
	preprocess_and_input(table_name, 'match_history')


	# pass


def preprocess_and_input(table_name=None, data_name=None):
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
		if data_name == 'oracle_elixir':
			pas_oracleelixir(table_name)
			return
		pas_matchschedule(table_name)

	elif table_name == 'match_info_by_team':
		pas_matchschedule(table_name)

	elif table_name == 'set_match':
		if data_name == 'oracle_elixir':
			pas_oracleelixir(table_name)
			return
		elif data_name == 'gamepedia':
			pas_gamepedia(table_name)
			return
		elif data_name == 'match_history':
			pas_matchhistory(table_name, 'team')
			return
		pas_matchschedule(table_name)

	elif table_name == 'set_match_info_by_team':
		if data_name == 'oracle_elixir':
			pas_oracleelixir(table_name)
			return
		elif data_name == 'match_history':
			# pas_matchhistory(table_name, 'player')
			pas_matchhistory(table_name, 'team')
			return
		pas_matchschedule(table_name)

	elif table_name == 'player':
		if data_name == 'oracle_elixir':
			pas_oracleelixir(table_name)
		elif data_name == 'match_history':
			pas_matchhistory(table_name, 'player')
		elif data_name == 'gamepedia':
			pas_gamepedia(table_name)

	elif table_name == 'champion':
		if data_name == 'oracle_elixir':
			pas_oracleelixir(table_name)
		elif data_name == 'match_history':
			pas_matchhistory(table_name, 'player')
			pas_matchhistory(table_name, 'team')

	elif table_name == 'set_match_player_performance':
		if data_name == 'oracle_elixir':
			pas_oracleelixir(table_name)
			return
		elif data_name == 'match_history':
			pas_matchhistory(table_name, 'player')
			return
		pas_create_table(table_name)

	elif table_name == 'set_match_url':
		pas_gamepedia(table_name)


	for file in glob.glob(f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\*csv'):
		if 'unique' in file:
			db.pkInput(pd.read_csv(file), table_name)
	return

	
def input_to_csv(table_name=None):
	temp_df = db.get_table(table_name)
	temp_df = temp_df[tableUniqueKey[table_name] + [tablePK_dict[table_name]]]
	temp_df.to_csv(f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_pk.csv', index=False)
	return

if __name__ == "__main__":
	main()