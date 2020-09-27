import pandas as pd

def win_percent(team, df):
	team_match_df = df[(df['team_1']==team) | (df['team_2']==team)]

	team_home = team_match_df[team_match_df['team_1']==team]
	team_away = team_match_df[team_match_df['team_2']==team]

	val_count_home = team_home.groupby(['league_name', 'year', 'season'])['wdl_1'].value_counts()
	val_count_away = team_away.groupby(['league_name', 'year', 'season'])['wdl_2'].value_counts()

	for league in team_match_df['league_name'].unique():
		for year in team_match_df['year'].unique():
			for season in team_match_df['season'].unique():
				season_win = 0
				season_loss = 0
				if 'W' in val_count_home[(league, year, season)].index:
					win_home = val_count_home[(league, year, season, 'W')]
					season_win += win_home
					
				if 'L' in val_count_home[(league, year, season)].index:
					loss_home = val_count_home[(league, year, season, 'L')]
					season_loss += loss_home
					
				if 'W' in val_count_away[(league, year, season)].index:
					win_away = val_count_away[(league, year, season, 'W')]
					season_win += win_away
					
				if 'L' in val_count_away[(league, year, season)].index:
					loss_away = val_count_away[(league, year, season, 'L')]
					season_loss += loss_away
					
				print(f'Year: {year}, Season: {season}, Win: {season_win}, Loss: {season_loss}, Win%: {season_win/(season_win+season_loss)*100:.2f}%')