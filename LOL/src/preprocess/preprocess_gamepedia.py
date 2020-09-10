import pandas as pd
import sys
import os
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import Preprocess
from utils import GamepediaDict, result_FFW


class Gamepedia(Preprocess):
	def __init__(self, original_df):
		super().__init__(original_df)
		

	def pp(self, table_name='game_schedule'):
		if table_name == 'game_schedule':
			# get original_df = 바꾸려는 gamepedia 데이터
			temp_df = self.original_df.copy()

			# get and set = year, season, league 
			year = temp_df['year'].unique()[0]
			season = temp_df['season'].unique()[0]
			league = temp_df['league_name'].unique()[0]

			# initiate Gamepedia dictionary
			gp_dict = GamepediaDict()
			gp_dict.from_year_season_league(year, season, league)
			
			# change league and team names, result
			temp_df['league_name'] = temp_df['league_name'].replace(gp_dict.get_dict('league'))
			temp_df[['team_1', 'team_2']] = temp_df[['team_1', 'team_2']].replace(gp_dict.get_dict('team'))
			temp_df['result'] = temp_df['result'].apply(result_FFW)

			self.preprocessed_df = temp_df
		
		elif table_name == 'set_match_url':
			# get original_df = 바꾸려는 gamepedia 데이터
			temp_df = self.original_df.copy()

			# fillna forward
			temp_df[['team_1', 'team_2']] = temp_df[['team_1', 'team_2']].fillna(method='ffill')

			# get and set = year, season, league 
			year = temp_df['year'].unique()[0]
			season = temp_df['season'].unique()[0]
			league = temp_df['league_name'].unique()[0]

			# instantiate Gamepedia dictionary
			gp_dict = GamepediaDict()
			gp_dict.from_year_season_league(year, season, league)
			
			# change league and team names
			temp_df['league_name'] = temp_df['league_name'].replace(gp_dict.get_dict('league'))
			temp_df[['team_1', 'team_2']] = temp_df[['team_1', 'team_2']].replace(gp_dict.get_dict('team'))

			self.preprocessed_df = temp_df

		return self.preprocessed_df