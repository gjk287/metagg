import os
import sys
import pandas as pd
import glob
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DB
from utils import matchhistory_result, change_fb_matchhistory, GamepediaDict, tableUniqueKey, time_to_sec, ckpm_feature, matchhistory_kmil, matchhistory_int_column
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
				ref_table = ref_table.reset_index(drop=True)
				self.reference_table = ref_table

				# create top~sup player id, first_blood, total gold, earned gold, minion kills, monster kills=neutral minion
				temp_df['week'] = temp_df['week'].astype(str)
				temp_df['year'] = temp_df['year'].astype(int)
				temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
				temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
				temp_df['earned_gold'] = temp_df['earned_gold'].apply(matchhistory_kmil)
				temp_df['minion_kills'] = temp_df['minion_kills'].apply(matchhistory_int_column)
				temp_df['neutral_minions_kills'] = temp_df['neutral_minions_kills'].apply(matchhistory_int_column)
				temp_df = change_fb_matchhistory(temp_df)

				#ref_table = ref_table.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number'])
				#temp_df = temp_df.set_index(['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number'])
				for idx, val in ref_table.copy().iterrows():
					temp_df_2 = temp_df[temp_df['year']==val['year']]
					temp_df_2 = temp_df_2[temp_df_2['season']==val['season']]
					temp_df_2 = temp_df_2[temp_df_2['league_name']==val['league_name']]
					temp_df_2 = temp_df_2[temp_df_2['team_1']==val['team_1']]
					temp_df_2 = temp_df_2[temp_df_2['team_2']==val['team_2']]
					temp_df_2 = temp_df_2[temp_df_2['team']==val['team']]
					temp_df_2 = temp_df_2[temp_df_2['tiebreaker']==val['tiebreaker']]
					temp_df_2 = temp_df_2[temp_df_2['match_round']==val['match_round']]
					temp_df_2 = temp_df_2[temp_df_2['set_number']==val['set_number']]
					temp_df_2 = temp_df_2.reset_index(drop=True)
					
					if temp_df_2.shape[0] == 5:
						top_player = temp_df_2.loc[0, 'player_name']
						jg_player = temp_df_2.loc[1, 'player_name']
						mid_player = temp_df_2.loc[2, 'player_name']
						bot_player = temp_df_2.loc[3, 'player_name']
						sup_player = temp_df_2.loc[4, 'player_name']
						
					else:
						print('No 5 players')
						print(f"Year: {val['year']}, Season: {val['season']}, League: {val['league_name']}, team_1: {val['team_1']}, team_2: {val['team_2']}, team: {val['team']}, match_round: {val['match_round']}, set_number: {val['set_number']}")
						print(temp_df_2.shape)
						print(temp_df_2[['year', 'season', 'week', 'team_1', 'team_2', 'team', 'player_name']])
						print()
						continue
					

					## groupby
					temp_df_groupby = temp_df_2.groupby(['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']).sum()
					fb = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'first_blood']
					earned_gold = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'earned_gold']
					minion_kills = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'minion_kills']
					monster_kills = temp_df_groupby.loc[tuple(val[['year', 'season', 'league_name', 'team_1', 'team_2', 'team', 'tiebreaker', 'match_round', 'set_number']]), 'neutral_minions_kills']

					# input to ref_table
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
				return ref_table.reset_index()

			elif table_name == 'set_match_player_performance':
				# pk를 가지고 있는 set_match_player_performance
				ref_table = db.extend_idToValue(ref_table, 'set_match_info_by_team')
				ref_table = db.extend_idToValue(ref_table, 'player')
				ref_table = db.extend_idToValue(ref_table, 'set_match')
				ref_table = db.extend_idToValue(ref_table, 'match')
				ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
				ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
				ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
				ref_table = ref_table[(ref_table['year']==year) & (ref_table['season']==season) & (ref_table['league_name']==league)]
				ref_table['year'] = ref_table['year'].astype(int)
				ref_table['match_round'] = ref_table['match_round'].astype(str)
				ref_table['tiebreaker'] = ref_table['tiebreaker'].astype(int)
				ref_table = ref_table.reset_index(drop=True)
				self.reference_table = ref_table

				#
				temp_df['week'] = temp_df['week'].astype(str)
				temp_df['year'] = temp_df['year'].astype(int)
				temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
				temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
				col_to_kmil = ['total_damage_dealt_to_champions', 'physical_damage_dealt_to_champions', 
				'magic_damage_dealt_to_champions', 'true_damage_dealt_to_champions', 'total_damage_dealt', 'physical_damage_dealt', 'magic_damage_dealt', 
				'true_damage_dealt', 'damage_dealt_to_objectives', 'damage_dealt_to_turrets', 'total_heal', 'total_damage_taken', 'physical_damage_taken', 
				'magical_damage_taken', 'true_damage_taken', 'earned_gold', 'gold_spent']
				col_to_int = ['largest_killing_spree', 'largest_multi_kill', 'largest_critical_strike', 'wards_placed', 'wards_killed', 'vision_wards_bought_in_game', 'minion_kills', 
				'neutral_minions_kills', 'neutral_minions_kills_team_jungle', 'neutral_minions_kills_enemy_jungle']
				for kmil in col_to_kmil:
					temp_df[kmil] = temp_df[kmil].apply(matchhistory_kmil)

				for int_change in col_to_int:
					temp_df[int_change] = temp_df[int_change].apply(matchhistory_int_column)

				# 
				for idx, val in ref_table.copy().iterrows():
					temp_df_2 = temp_df[temp_df['year']==val['year']]
					temp_df_2 = temp_df_2[temp_df_2['season']==val['season']]
					temp_df_2 = temp_df_2[temp_df_2['league_name']==val['league_name']]
					temp_df_2 = temp_df_2[temp_df_2['team_1']==val['team_1']]
					temp_df_2 = temp_df_2[temp_df_2['team_2']==val['team_2']]
					temp_df_2 = temp_df_2[temp_df_2['tiebreaker']==val['tiebreaker']]
					temp_df_2 = temp_df_2[temp_df_2['match_round']==val['match_round']]
					temp_df_2 = temp_df_2[temp_df_2['set_number']==val['set_number']]
					temp_df_2 = temp_df_2[temp_df_2['player_name']==val['player_name']]
					temp_df_2 = temp_df_2.reset_index(drop=True)

					if temp_df_2.shape[0] != 1:
						print('No player!')
						continue
					else:
						pass
					
					col_all = col_to_kmil + col_to_int
					# ref_table input
					# series로 넣을 수 있는지 알아보기 **
					for col_each in col_all:
						ref_table.loc[idx, col_each] = temp_df_2.loc[0, col_each]

				ref_table = ref_table.where(pd.notnull(ref_table), None)
				return ref_table.reset_index()
					

		
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
				# pass
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
				ref_table = ref_table.reset_index(drop=True)
				self.reference_table = ref_table

				# wdl, side, ban1~5,  team_kills, team_deaths, team_kpm, baron, dragon, rift, tower, inhib, total_golds, 
				temp_df['week'] = temp_df['week'].astype(str)
				temp_df['year'] = temp_df['year'].astype(int)
				temp_df['tiebreaker'] = temp_df['week'].apply(lambda x: 1 if x == 'Tiebreakers' else 0)
				temp_df['match_round'] = temp_df['week'].replace({'Round': 'Elimination Round', 'Stage': 'Knockout Stage'})
				temp_df['wdl'] = temp_df['result'].apply(matchhistory_result)
				temp_df['game_length'] = temp_df['game_length'].apply(time_to_sec)
				temp_df['team_total_gold'] = temp_df['total_golds'].apply(matchhistory_kmil)

				for idx, val in ref_table.copy().iterrows():
					temp_df_2 = temp_df[temp_df['year']==val['year']]
					temp_df_2 = temp_df_2[temp_df_2['season']==val['season']]
					temp_df_2 = temp_df_2[temp_df_2['league_name']==val['league_name']]
					temp_df_2 = temp_df_2[temp_df_2['team_1']==val['team_1']]
					temp_df_2 = temp_df_2[temp_df_2['team_2']==val['team_2']]
					temp_df_2 = temp_df_2[temp_df_2['tiebreaker']==val['tiebreaker']]
					temp_df_2 = temp_df_2[temp_df_2['match_round']==val['match_round']]
					temp_df_2 = temp_df_2[temp_df_2['set_number']==val['set_number']]

					temp_df_home = temp_df_2[temp_df_2['team']==val['team']]
					temp_df_away = temp_df_2[~(temp_df_2['team']==val['team'])]
					temp_df_home = temp_df_home.reset_index(drop=True)
					temp_df_away = temp_df_away.reset_index(drop=True)

					if temp_df_home.shape[0] != 1:
						print(temp_df_home[['year', 'season', 'league_name', 'team_1', 'team_2', 'match_round', 'set_number']])
						continue

					wdl = temp_df_home.loc[0, 'wdl']
					side = temp_df_home.loc[0, 'side']
					team_kills = temp_df_home.loc[0, 'total_kills']
					team_deaths = temp_df_away.loc[0, 'total_kills']
					gamelength = temp_df_home.loc[0, 'game_length']
					team_kpm = team_kills / gamelength * 60
					team_baron_kills = temp_df_home.loc[0, 'baron_kills']
					team_dragon_kills = temp_df_home.loc[0, 'dragon_kills']
					team_rift_kills = temp_df_home.loc[0, 'rift_kills']
					team_tower_kills = temp_df_home.loc[0, 'tower_kills']
					team_inhib_kills = temp_df_home.loc[0, 'inhibitor_kills']
					team_total_gold = temp_df_home.loc[0, 'team_total_gold']


					# input to ref_table
					ref_table.loc[idx, 'ban1'] = temp_df_home.loc[0, 'ban1']
					ref_table.loc[idx, 'ban2'] = temp_df_home.loc[0, 'ban2']
					ref_table.loc[idx, 'ban3'] = temp_df_home.loc[0, 'ban3']
					ref_table.loc[idx, 'ban4'] = temp_df_home.loc[0, 'ban4']
					ref_table.loc[idx, 'ban5'] = temp_df_home.loc[0, 'ban5']
					ref_table.loc[idx, 'wdl'] = wdl
					ref_table.loc[idx, 'side'] = side
					ref_table.loc[idx, 'team_kills'] = team_kills
					ref_table.loc[idx, 'team_deaths'] = team_deaths
					ref_table.loc[idx, 'team_kpm'] = team_kpm
					ref_table.loc[idx, 'team_baron_kills'] = team_baron_kills
					ref_table.loc[idx, 'team_dragon_kills'] = team_dragon_kills
					ref_table.loc[idx, 'team_rift_kills'] = team_rift_kills
					ref_table.loc[idx, 'team_tower_kills'] = team_tower_kills
					ref_table.loc[idx, 'team_inhib_kills'] = team_inhib_kills
					ref_table.loc[idx, 'team_total_gold'] = team_total_gold

				ref_table[['ban1_id', 'ban2_id', 'ban3_id', 'ban4_id', 'ban5_id']] = ref_table[['ban1', 'ban2', 'ban3', 'ban4', 'ban5']].replace(db.get_dict('champion')['valueToID'])
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