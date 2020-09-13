import os
import sys
import pandas as pd
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DB
from utils import change_fb_matchhistory, GamepediaDict, tableUniqueKey, time_to_sec, ckpm_feature
from preprocess import Preprocess

# instantiate database
db = DB()
db.initialise()

def main():
	pass



class MatchHistory(Preprocess):
	def __init__(self, original_df):
		super().__init__(original_df)
		self.reference_table = None

	def pp(self, table_name=None, table_type='player', ref_table=None):
		temp_df = self.original_df.copy()

		# get and set = year, season, league 
		year = temp_df['year'].unique()[0]
		season = temp_df['season'].unique()[0]
		league = temp_df['league_name'].unique()[0]

		# initiate Gamepedia dictionary
		gp_dict = GamepediaDict()
		gp_dict.from_year_season_league(year, season, league)

		# change league and team names, champion
		temp_df['league_name'] = temp_df['league_name'].replace(gp_dict.get_dict('league'))
		temp_df[['team_1', 'team_2', 'team']] = temp_df[['team_1', 'team_2', 'team']].replace(gp_dict.get_dict('team'))
		
		if table_type == 'player':
			temp_df['champion'] = temp_df['champion'].replace(gp_dict.get_dict('champion'))
			temp_df['player_name'] = temp_df['player_name'].replace(gp_dict.get_dict('player'))

			# get player table
			if table_name == 'player':
				temp_df = temp_df.dropna(subset=['player_name']).reset_index(drop=True)
				player_list = list(temp_df['player_name'].unique())
				return pd.DataFrame(data=player_list, columns=['player_name'])

			# get champion table
			if table_name == 'champion':
				temp_df = temp_df.dropna(subset=['champion']).reset_index(drop=True)
				champion_list = list(temp_df['champion'].unique())
				return pd.DataFrame(data=champion_list, columns=['champion_name'])

		
		elif table_type == 'team':
			temp_df[['ban1', 'ban2', 'ban3', 'ban4', 'ban5']] = temp_df[['ban1', 'ban2', 'ban3', 'ban4', 'ban5']].replace(gp_dict.get_dict('champion'))

			# get champion table
			if table_name == 'champion':
				temp_df = temp_df.dropna(subset=['ban1', 'ban2', 'ban3', 'ban4', 'ban5']).reset_index(drop=True)
				champ_set = set(temp_df['ban1'])
				champ_set.update(set(temp_df['ban2']))
				champ_set.update(set(temp_df['ban3']))
				champ_set.update(set(temp_df['ban4']))
				champ_set.update(set(temp_df['ban5']))
				champion_list = list(champ_set)
				return pd.DataFrame(data=champion_list, columns=['champion_name'])

			# get set_match table
			elif table_name == 'set_match':
				ref_table = db.extend_idToValue(ref_table, 'match')
				ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
				ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
				ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
				self.reference_table = ref_table

				# get game_length and ckpm
				temp_df['game_length'] = temp_df['game_length'].apply(time_to_sec)
				temp_df['week'] = temp_df['week'].astype(str)
				temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
				temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
				temp_df_groupby = temp_df.groupby(['year', 'season', 'week', 'team_1', 'team_2', 'league_name', 'set_number']).sum()
				temp_df = temp_df.set_index(['year', 'season', 'week', 'team_1', 'team_2', 'league_name', 'set_number'])
				for idx, _ in temp_df.iterrows():
					ckill = temp_df_groupby.loc[idx, 'total_kills']
					temp_df.loc[idx, 'ckill'] = ckill
				temp_df = temp_df.reset_index()
				temp_df['ckpm'] = temp_df.apply(lambda row: ckpm_feature(row['ckill'], row['game_length']), axis=1)
				
				# put value to ref_table
				ref_table = ref_table.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round'])
				temp_df = temp_df.drop_duplicates(subset=['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round'])
				temp_df = temp_df.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round'])
				for idx, _ in ref_table.iterrows():
					try:
						ref_table.loc[idx, 'ckpm'] = temp_df.loc[idx, 'ckpm']
						ref_table.loc[idx, 'game_length'] = temp_df.loc[idx, 'game_length']
					except:
						ref_table.loc[idx, 'ckpm'] = None
						ref_table.loc[idx, 'game_length'] = None
				ref_table = ref_table.where(pd.notnull(ref_table), None)
				return ref_table.reset_index()




# temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
		# elif table_name == 'set_match':
		# 	pass

		# elif table_name == 'set_match_info_by_team':
		# 	pass

		# elif table_name == 'set_match_player_performance':
		# 	pass

		
		

		# player, champion, 


		# if table_type == 'player':
		# 	# change first blood
		# 	temp_df = change_fb_matchhistory(temp_df)

		# ## matchschedule보다 데이터가 적으므로 쓰지않기
		# if table_name == 'team':
		# 	# get set of all teams
		# 	teams = set(temp_df['team_1'])
		# 	teams.update(set(temp_df['team_2']))
		# 	teams.update(set(temp_df['team']))
		# 	# create team table
		# 	df = pd.DataFrame(data=list(teams), columns=['team_name'])

		# return df


if __name__ == '__main__':
	main()