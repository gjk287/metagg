import glob
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from preprocess import Gamepedia
from database import DB
from utils import tableUniqueKey, tablePK_dict

db = DB()
db.initialise()

def main():
	preprocess_and_save('game_schedule')
	preprocess_and_save('match_history_url')


def preprocess_and_save(data_name='game_schedule', table_name=None, save=True):
	if data_name == 'game_schedule':
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

	elif (data_name == 'set_match_url') | (data_name == 'set_match'):
		df = pd.DataFrame()
		for file in glob.glob('LOL\\datasets\\RawData\\Gamepedia\\match_history_url\\*csv'):
			# open file
			temp_df = pd.read_csv(file)
			# preprocess
			pp_obj = Gamepedia(temp_df)
			temp_df = pp_obj.pp('set_match_url')
			# concat
			df = pd.concat([df, temp_df]).reset_index(drop=True)

		# tiebreaker, match_round column 생성
		df['tiebreaker'] = df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
		df['match_round'] = df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
		df['year'] = df['year'].astype(int)
		df['set_number'] = df['set_number'].astype(int)
		df['match_round'] = df['match_round'].astype(str)

		# set_match_id 매치 시켜주기
		table_name = 'set_match'
		temp_df = db.get_table(table_name)
		temp_df = temp_df[tableUniqueKey[table_name] + [tablePK_dict[table_name]]]
		temp_df = db.extend_idToValue(temp_df, 'match')
		temp_df = db.extend_idToValue(temp_df, 'league')
		temp_df = db.extend_idToValue(temp_df, 'team', 'home_team_id', rename={'team_name':'team_1'})
		temp_df = db.extend_idToValue(temp_df, 'team', 'away_team_id', rename={'team_name':'team_2'})
		temp_df['match_round'] = temp_df['match_round'].astype(str)
		
		df = pd.merge(df, temp_df, how='left', left_on=['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round', 'set_number'], right_on=['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round', 'set_number'])
		
		if data_name == 'match_history_url':
			df = df.rename(columns={'MH':'match_history_url', 'PB':'vod_pick_ban_url', 'Start':'vod_start_url', 'HL':'vod_highlight_url', 'Vod':'vod_url', 'Post':'vod_post_url'})
			# save only unique columns
			df = df[tableUniqueKey[data_name]]
			newPath = f'LOL\\datasets\\DerivedData\\DB_table\\set_match_url\\set_match_url_unique.csv'
		
		elif data_name == 'set_match':
			df = df.rename(columns={'MVP':'mvp'})
			df = df[tableUniqueKey[data_name] + [tablePK_dict[data_name]] + ['mvp']]
			newPath = f'LOL\\datasets\\DerivedData\\DB_table\\set_match\\set_match_mvp.csv'
		
	else:
		print('wrong data')

	if save:
		try:
			df.to_csv(newPath, index=False)
		except:
			newPath = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\{newPath}'
			df.to_csv(newPath, index=False)
	else:
		return df


if __name__ == "__main__":
	main()