import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocess import Preprocess
from utils import GameDictionary, datetime_to_strft, str_to_datetime, oddsToFloat, matchTypeToSeason


class Oddsportal(Preprocess):
	def __init__(self, original_df):
		super().__init__(original_df)

	def pp(self):
		g_dict = GameDictionary()
		temp_df = self.original_df.copy()
		temp_df['date'] = temp_df['date'].apply(str_to_datetime).apply(datetime_to_strft)
		temp_df[['team_1', 'team_2']] = temp_df[['team_1', 'team_2']].replace(g_dict.get_dict('team'))
		temp_df['win_odds_home'] = temp_df['win_odds_home'].apply(oddsToFloat)
		temp_df['win_odds_away'] = temp_df['win_odds_away'].apply(oddsToFloat)
		temp_df['season'] = temp_df['match_type'].apply(matchTypeToSeason)
		temp_df['betting_site'] = 'Oddsportal'
		temp_df['bet_type'] = 'special'
		temp_df['saved_time'] = temp_df['date']
		self.preprocessed_df = temp_df
		return self.preprocessed_df