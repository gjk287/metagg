import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src\\preprocess\\tests'))
from test_preprocess_gamepedia import preprocess_and_save as pas_gamepedia

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src\\preprocess'))
from preprocess_create_table import preprocess_and_save as pas_create_table

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from database import DB

db = DB()
db.initialise()

def main():
	# preprocess create league, betting site, bet type table
	pas_create_table('league')
	pas_create_table('betting_site')
	pas_create_table('bet_type', 'bet_type_special')
	pas_create_table('bet_type', 'bet_type_ou')
	pas_create_table('bet_type', 'bet_type_handicap')
	pas_create_table('bet_type', 'bet_type_both')
	## input in DB
	db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\league\\league_unique.csv'), 'league')
	db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\betting_site\\betting_site_unique.csv'), 'betting_site')
	db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\bet_type_special\\bet_type_special_unique.csv'), 'bet_type_special')
	db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\bet_type_ou\\bet_type_ou_unique.csv'), 'bet_type_ou')
	db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\bet_type_handicap\\bet_type_handicap_unique.csv', dtype={'handicap_amount':str}), 'bet_type_handicap')
	db.pkInput(pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\bet_type_both\\bet_type_both_unique.csv'), 'bet_type_both')

	# # preprocess gamepedia data
	# pas_gamepedia('game_schedule')
	
	
	
	
	
	
	
	
	
	#pas_gamepedia('match_history_url')




if __name__ == "__main__":
	main()