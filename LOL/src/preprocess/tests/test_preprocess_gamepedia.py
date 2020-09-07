import glob
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from preprocess import Gamepedia


def main():
	preprocess_and_save('game_schedule')
	preprocess_and_save('match_history_url')


def preprocess_and_save(data_type='game_schedule'):
	if data_type == 'game_schedule':
		df = pd.DataFrame()
		for file in glob.glob('LOL\\datasets\\RawData\\Gamepedia\\game_schedule\\*csv'):
			# open file
			temp_df = pd.read_csv(file)

			# preprocess
			pp_obj = Gamepedia(temp_df)
			temp_df = pp_obj.pp('game_schedule')

			# concat
			df = pd.concat([df, temp_df]).reset_index(drop=True)
		# save
		newPath = f'LOL\\datasets\\DerivedData\\None_DB_table\\game_schedule.csv'

	elif data_type == 'match_history_url':
		df = pd.DataFrame()
		for file in glob.glob('LOL\\datasets\\RawData\\Gamepedia\\match_history_url\\*csv'):
			# open file
			temp_df = pd.read_csv(file)
			# preprocess
			pp_obj = Gamepedia(temp_df)
			temp_df = pp_obj.pp('match_history_url')
			# concat
			df = pd.concat([df, temp_df]).reset_index(drop=True)
		# save
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\set_match_url\\match_history_url.csv'
		
	else:
		print('wrong data')

	df.to_csv(newPath, index=False)


if __name__ == "__main__":
	main()