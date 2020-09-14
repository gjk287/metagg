import os
import sys
import pandas as pd
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DB
from utils import change_fb_matchhistory, GamepediaDict, tableUniqueKey, time_to_sec, ckpm_feature, matchhistory_kmil, matchhistory_int_column
from preprocess import Preprocess

# instantiate database
db = DB()
db.initialise()

def main():
	pass
"""
player, team 두개로 나눠진 matchhistory 데이터에서 player, champion, set_match, set_match_info_by_team, set_match_player performance를 만들려고함
table_type은 (player), (team)으로 나눠진 데이터 종류를 뜻함
table_name은 내가 만들고 싶은 table 이름을 뜻함.
여기에 들어가는 데이터는 매년 매시즌의 리그 경기가 들어감. (여기에서 year, season, league를 얻고 gamepedia_dict에 넣어서 거기에 맞는 team 이름으로 바꾸기)
	player table 					= (player)에서 만들기
	champion table 					= (player), (team)에서 만들기 
	set_match table 				= (team)에서 ckpm, gamelength 만들기
	set_match_info_by_team 			= table_type both를 만들어서 두개를 같이 사용해서 테이블을 생성해야됨. groupby 같은거 사용해보기. 아니면 각자에서 하나씩 생성하는걸로 하기. 내일 생각해보기
	set_match_player_performance	= (player)에서 만들기

"""
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
			elif table_name == 'champion':
				temp_df = temp_df.dropna(subset=['champion']).reset_index(drop=True)
				champion_list = list(temp_df['champion'].unique())
				return pd.DataFrame(data=champion_list, columns=['champion_name'])

			# get set_match_info_by_team table
			elif table_name == 'set_match_info_by_team':
				# pk를 가지고 있는 set_match_info_by_team
				ref_table = db.extend_idToValue(ref_table, 'set_match')
				ref_table = db.extend_idToValue(ref_table, 'match')
				ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
				ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
				ref_table = db.extend_idToValue(ref_table, 'team', 'team_id', rename={'team_name':'team'})
				ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
				ref_table = ref_table[(ref_table['year']==year) & (ref_table['season']==season) & (ref_table['league_name']==league)]
				ref_table['year'] = ref_table['year'].astype(int)
				ref_table['match_round'] = ref_table['match_round'].astype(str)
				ref_table['tiebreaker'] = ref_table['tiebreaker'].astype(int)
				self.reference_table = ref_table

				# create top~sup player id, first_blood, total gold, earned gold, minion kills, monster kills=neutral minion
				temp_df['week'] = temp_df['week'].astype(str)
				temp_df['year'] = temp_df['year'].astype(int)
				temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
				temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
				temp_df = change_fb_matchhistory(temp_df)

				#ref_table = ref_table.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number'])
				#temp_df = temp_df.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number'])
				for idx, val in ref_table.copy().iterrows():
					temp_df = temp_df[temp_df['year']==val['year']]
					temp_df = temp_df[temp_df['season']==val['season']]
					temp_df = temp_df[temp_df['league_name']==val['league_name']]
					temp_df = temp_df[temp_df['team_1']==val['team_1']]
					temp_df = temp_df[temp_df['team_2']==val['team_2']]
					temp_df = temp_df[temp_df['team']==val['team']]
					temp_df = temp_df[temp_df['tiebreaker']==val['tiebreaker']]
					temp_df = temp_df[temp_df['match_round']==val['match_round']]
					temp_df = temp_df[temp_df['set_number']==val['set_number']].reset_index(drop=True)
					
					if temp_df.shape[0] == 5:
						top_player = temp_df.loc[0, 'player_name']
						jg_player = temp_df.loc[1, 'player_name']
						mid_player = temp_df.loc[2, 'player_name']
						bot_player = temp_df.loc[3, 'player_name']
						sup_player = temp_df.loc[4, 'player_name']
						print(f"Year: {val['year']}, Season: {val['season']}, League: {val['league_name']}, team_1: {val['team_1']}, team_2: {val['team_2']}, match_round: {val['match_round']}, set_number: {val['set_number']}")
						temp_df.to_csv('tempdd.csv',index=False)
						break
					else:
						print('No 5 players')
						print(f"Year: {val['year']}, Season: {val['season']}, League: {val['league_name']}, team_1: {val['team_1']}, team_2: {val['team_2']}, match_round: {val['match_round']}, set_number: {val['set_number']}")
						continue
					
					temp_df['earned_gold'] = temp_df['earned_gold'].apply(matchhistory_kmil)
					temp_df['minion_kills'] = temp_df['minion_kills'].apply(matchhistory_int_column)
					temp_df['neutral_minions_kills'] = temp_df['neutral_minions_kills'].apply(matchhistory_int_column)

					## groupby
					temp_df_groupby = temp_df.groupby(['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']).sum()
					fb = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'first_blood']
					earned_gold = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'earned_gold']
					minion_kills = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'minion_kills']
					monster_kills = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'neutral_minions_kills']

					# input in ref_table
					ref_table.loc[idx, 'top_player'] = top_player
					ref_table.loc[idx, 'jg_player'] = jg_player
					ref_table.loc[idx, 'mid_player'] = mid_player
					ref_table.loc[idx, 'bot_player'] = bot_player
					ref_table.loc[idx, 'sup_player'] = sup_player
					ref_table.loc[idx, 'team_first_blood'] = fb
					ref_table.loc[idx, 'team_earned_gold'] = earned_gold
					ref_table.loc[idx, 'team_minion_kills'] = minion_kills
					ref_table.loc[idx, 'team_monster_kills'] = monster_kills

				ref_table[['top_player_id', 'jg_player_id', 'mid_player_id', 'bot_player_id', 'sup_player_id']] = ref_table[['top_player', 'jg_player', 'mid_player', 'bot_player', 'sup_player']].replace(db.get_dict('player')['valueToID'])
				ref_table = ref_table.where(pd.notnull(ref_table), None)
					



		
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
				# pk를 가지고 있는 set_match 테이블
				# 같은 년도, 같은 시즌에 같은 리그인것만 보기
				ref_table = db.extend_idToValue(ref_table, 'match')
				ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
				ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
				ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
				ref_table = ref_table[(ref_table['year']==year) & (ref_table['season']==season) & (ref_table['league_name']==league)]
				self.reference_table = ref_table

				# create game_length and ckpm
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
				
				# put created value to ref_table
				# year, season, league_name, team_1, team_2, tiebreaker, match_round로 게임을 특정 지을 수 있음
				ref_table = ref_table.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round', 'set_number'])

				# ckpm, game_length는 두팀다 똑같기 때문에 drop duplicates
				temp_df = temp_df.drop_duplicates(subset=['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round', 'set_number'])
				temp_df = temp_df.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'tiebreaker', 'match_round', 'set_number'])
				for idx, _ in ref_table.iterrows():
					# 없으면 None으로 넣기
					try:
						ref_table.loc[idx, 'ckpm'] = temp_df.loc[idx, 'ckpm']
						ref_table.loc[idx, 'game_length'] = temp_df.loc[idx, 'game_length']
					except:
						ref_table.loc[idx, 'ckpm'] = None
						ref_table.loc[idx, 'game_length'] = None
				ref_table = ref_table.where(pd.notnull(ref_table), None)
				return ref_table.reset_index()

			# get set_match_info_by_team table
			elif table_name == 'set_match_info_by_team':
				# pk를 가지고 있는 set_match_info_by_team
				ref_table = db.extend_idToValue(ref_table, 'set_match')
				ref_table = db.extend_idToValue(ref_table, 'match')
				ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
				ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
				ref_table = db.extend_idToValue(ref_table, 'team', 'team_id', rename={'team_name':'team'})
				ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
				ref_table = ref_table[(ref_table['year']==year) & (ref_table['season']==season) & (ref_table['league_name']==league)]
				self.reference_table = ref_table

				# wdl, side, ban1~5,  team_kills, team_deaths, team_kpm, baron, dragon, rift, tower, inhib




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