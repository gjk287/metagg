import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import opp_team, dot_wma

def num_win_N_last_game(df, rolling_window=3, weighted_sum=False):
	df['date'] = pd.to_datetime(df['date'])
	concat_df = pd.DataFrame()

	for league in df['league_name'].unique():
		temp_league = df[df['league_name']==league]
		for team in temp_league['corresponding_team'].unique():
			temp_team = temp_league[temp_league['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
			for year in temp_team['year'].unique():
				temp_year = temp_team[temp_team['year']==year]
				for season in temp_year['season'].unique():
					temp_season = temp_year[temp_year['season']==season]
					if weighted_sum==False:
						temp_season[f'num_win_{rolling_window}_last_game'] = temp_season['wdl'].apply(lambda x: 1 if (x=='W') else 0).rolling(rolling_window).sum().shift(1)
					else:
						temp_season[f'win_weighted_sum_{rolling_window}_last_game'] = temp_season['wdl'].apply(lambda x: 1 if (x=='W') else 0).rolling(rolling_window).apply(lambda x: dot_wma(x, rolling_window, 4.5)).shift(1)
					concat_df = pd.concat([concat_df, temp_season]).reset_index(drop=True)
	return concat_df


def win_rate_N_last_game(df, rolling_window=3, opponent=False):
	df['date'] = pd.to_datetime(df['date'])
	concat_df = pd.DataFrame()
	if opponent==False:
		for league in df['league_name'].unique():
			temp_league = df[df['league_name']==league]
			for team in temp_league['corresponding_team'].unique():
				temp_team = temp_league[temp_league['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
				for year in temp_team['year'].unique():
					temp_year = temp_team[temp_team['year']==year]
					for season in temp_year['season'].unique():
						temp_season = temp_year[temp_year['season']==season]
						# from start of the season
						if rolling_window == 'start':
							temp_season[f'win_rate_start_of_season'] = temp_season['wdl'].apply(lambda x: 1 if (x=='W') else 0).expanding(1).mean().shift(1)
						else:
							temp_season[f'win_rate_{rolling_window}_last_game'] = temp_season['wdl'].apply(lambda x: 1 if (x=='W') else 0).rolling(rolling_window).mean().shift(1)
						concat_df = pd.concat([concat_df, temp_season]).reset_index(drop=True)
	
	elif opponent:
		for league in df['league_name'].unique():
			temp_league = df[df['league_name']==league]
			for team in temp_league['corresponding_team'].unique():
				temp_team = temp_league[temp_league['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
				temp_team['opp_team'] = temp_team.apply(lambda row: opp_team(row['team_1'], row['team_2'], row['corresponding_team']), axis=1)
				for opTeam in temp_team['opp_team'].unique():
					temp_team_opp = temp_team[(temp_team['team_1']==opTeam) | (temp_team['team_2']==opTeam)]
					temp_team_opp['win_rate_against_opp'] = temp_team_opp['wdl'].apply(lambda x: 1 if x == 'W' else 0).expanding(1).mean().shift(1)
					concat_df = pd.concat([concat_df, temp_team_opp]).reset_index(drop=True)
		concat_df = concat_df.drop(['opp_team'], axis=1)
	return concat_df
