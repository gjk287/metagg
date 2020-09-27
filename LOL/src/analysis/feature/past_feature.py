import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def expand_N_last_game(df, col_to_use, N_last=1):
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
					for i in range(N_last):
						temp_season[[f'{x}__{i+1}' for x in col_to_use]] = temp_season[col_to_use].shift(i+1)

					concat_df = pd.concat([concat_df, temp_season]).reset_index(drop=True)
	return concat_df