import os
import sys
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_matchSchedule, tableUniqueKey, toWDL, result_opp, get_df_with_3set
from database import DB

db = DB()
db.initialise()


def main():
	preprocess_and_save('match_info_by_team')

def preprocess_and_save(table_name='team', data_name=None, save=True):
	# get match schedule
	temp_df = get_matchSchedule()

	if table_name == 'team':
		# get set of all teams
		teams = set(temp_df['team_1'])
		teams.update(set(temp_df['team_2']))
		# create team table
		df = pd.DataFrame(data=list(teams), columns=['team_name'])

	elif table_name == 'match':
		# preprocess
		leagueDict = db.get_dict('league')['valueToID']
		teamDict = db.get_dict('team')['valueToID']
		temp_df['league_id'] = temp_df['league_name'].replace(leagueDict)
		temp_df['home_team_id'] = temp_df['team_1'].replace(teamDict)
		temp_df['away_team_id'] = temp_df['team_2'].replace(teamDict)
		temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
		temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
		df = temp_df

	elif table_name == 'match_info_by_team':
		# preprocess match to keep the result data
		leagueDict = db.get_dict('league')['valueToID']
		teamDict = db.get_dict('team')['valueToID']
		temp_df['league_id'] = temp_df['league_name'].replace(leagueDict)
		temp_df['home_team_id'] = temp_df['team_1'].replace(teamDict)
		temp_df['away_team_id'] = temp_df['team_2'].replace(teamDict)
		temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
		temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
		
		# merge with match_pk to get match_id
		match_id_df = pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\match\\match_pk.csv')
		match_merged = pd.merge(temp_df, match_id_df, how='inner', left_on=tableUniqueKey['match'], right_on=tableUniqueKey['match'])

		# preprocess
		home_match_info = match_merged.copy()
		home_match_info['team_id'] = home_match_info['home_team_id']
		home_match_info['wdl'] = home_match_info['result'].apply(lambda x: toWDL(x, homeAway='home'))
		home_match_info = home_match_info[['match_id', 'team_id', 'result', 'wdl']]
		away_match_info = match_merged.copy()
		away_match_info['team_id'] = away_match_info['away_team_id']
		away_match_info['wdl'] = away_match_info['result'].apply(lambda x: toWDL(x, homeAway='away'))
		away_match_info['result'] = away_match_info['result'].apply(result_opp)
		away_match_info = away_match_info[['match_id', 'team_id', 'result', 'wdl']]
		df = pd.concat([home_match_info, away_match_info]).reset_index(drop=True)

	elif table_name == 'set_match':
		# preprocess match to keep the result data
		leagueDict = db.get_dict('league')['valueToID']
		teamDict = db.get_dict('team')['valueToID']
		temp_df['league_id'] = temp_df['league_name'].replace(leagueDict)
		temp_df['home_team_id'] = temp_df['team_1'].replace(teamDict)
		temp_df['away_team_id'] = temp_df['team_2'].replace(teamDict)
		temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
		temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
		
		# merge with match_pk to get match_id
		match_id_df = pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\match\\match_pk.csv')
		match_merged = pd.merge(temp_df, match_id_df, how='inner', left_on=tableUniqueKey['match'], right_on=tableUniqueKey['match'])

		# 세트로 늘리기
		set_match_df = get_df_with_3set(match_merged)
		df = set_match_df
		
		
		
	df_unique = df[tableUniqueKey[table_name]]
	df_all_columns = list(set(df.columns) & set(db.get_table_columns(table_name)))
	df_all = df[df_all_columns]
	# path
	newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique.csv'
	newPathAll = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_all.csv'
	if save:
		try:
			df_unique.to_csv(newPath, index=False)
			df_all.to_csv(newPathAll, index=False)
		except:
			newPath = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\{newPath}'
			newPathAll = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\{newPathAll}'
			df_unique.to_csv(newPath, index=False)
			df_all.to_csv(newPathAll, index=False)
	else:
		return df_unique


if __name__ == "__main__":
	main()
