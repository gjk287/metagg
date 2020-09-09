import pandas as pd
import sys
import os
import io
from datetime import datetime, timedelta, date
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import DB
from preprocess import Preprocess
from utils import GameDictionary, datetime_to_strft, str_to_datetime, stringDate_to_strft, oddsToFloat, matchTypeToSeason, set_match_info_result_to_wdl

db = DB()
db.initialise()


class OracleElixir(Preprocess):
	def __init__(self, original_df):
		super().__init__(original_df)
		self.reference_table = None

	def pp(self, table_name, ref_table=None):
		# instantiate dictionary and replace
		g_dict = GameDictionary()
		temp_df = self.original_df
		temp_df['player'] = temp_df['player'].replace(g_dict.get_dict('player'))
		temp_df[['champion', 'ban1', 'ban2', 'ban3', 'ban4', 'ban5']] = temp_df[['champion', 'ban1', 'ban2', 'ban3', 'ban4', 'ban5']].replace(g_dict.get_dict('champion'))
		temp_df['team'] = temp_df['team'].replace(g_dict.get_dict('team'))
		temp_df['league'] = temp_df['league'].replace(g_dict.get_dict('league'))
		temp_df['date'] = temp_df['date'].apply(stringDate_to_strft)

		league_list = ['LLN', 'CLS', 'IEM', 'GPL', 'DC', 'LFL']
		temp_df = temp_df[~temp_df['league'].isin(league_list)].reset_index(drop=True)
		
		if table_name == 'player':
			temp_df = temp_df.dropna(subset=['player'])
			player_list = list(temp_df['player'].unique())
			return pd.DataFrame(data=player_list, columns=['player_name'])
			
		elif table_name == 'champion':
			temp_df = temp_df.dropna(subset=['champion'])
			champ_table = pd.DataFrame(data=list(temp_df['champion'].unique()), columns=['champion_name'])
			return champ_table

		elif table_name == 'match':
			ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
			ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
			ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
			self.reference_table = ref_table

			for idx, val in ref_table.copy().iterrows():
				gameDivide = temp_df[(temp_df['date'].isin([(pd.to_datetime(val['date']) + timedelta(days=x)).strftime('%Y-%m-%d') for x in self.date_range])) & (temp_df['league']==val['league_name'])]
				for gameID in gameDivide['gameid'].unique():
					each_game = gameDivide[gameDivide['gameid']==gameID]
					if each_game.empty:
						continue
					if (val['team_1'] in each_game['team'].unique()) & (val['team_2'] in each_game['team'].unique()):
						if each_game['patch'].unique()[0]:
							patch = each_game['patch'].unique()[0]
						else:
							patch = None
						ref_table.loc[idx, 'patch'] = patch
			ref_table = ref_table.where(pd.notnull(ref_table), None)
			return ref_table.reset_index(drop=True)

		elif table_name == 'set_match':
			ref_table = db.extend_idToValue(ref_table, 'match')
			ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
			ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
			ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
			self.reference_table = ref_table

			for idx, val in ref_table.copy().iterrows():
				# 진도율 확인용
				if idx % 3000 == 0:
					print(idx)

				gameDivide = temp_df[(temp_df['date'].isin([(pd.to_datetime(val['date']) + timedelta(days=x)).strftime('%Y-%m-%d') for x in self.date_range])) & (temp_df['league']==val['league_name'])]
				for gameID in gameDivide['gameid'].unique():
					each_game = gameDivide[gameDivide['gameid']==gameID]
					if each_game.empty:
						continue
					if (val['team_1'] in each_game['team'].unique()) & (val['team_2'] in each_game['team'].unique()) & (val['set_number']==each_game['game'].unique()[0]):
						if each_game['ckpm'].unique()[0]:
							ckpm = each_game['ckpm'].unique()[0]
						else:
							ckpm = None

						if each_game['gamelength'].unique()[0]:
							gamelength = each_game['gamelength'].unique()[0]
						else:
							gamelength = None

						ref_table.loc[idx, 'ckpm'] = ckpm
						ref_table.loc[idx, 'game_length'] = gamelength
			ref_table = ref_table.where(pd.notnull(ref_table), None)
			return ref_table.reset_index(drop=True)

		elif table_name == 'set_match_info_by_team':
			ref_table = db.extend_idToValue(ref_table, 'set_match')
			ref_table = db.extend_idToValue(ref_table, 'match')
			ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
			ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
			ref_table = db.extend_idToValue(ref_table, 'team', 'team_id', rename={'team_name':'team'})
			ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
			self.reference_table = ref_table

			# db connection 열렸나 체크용
			player_dict = db.get_dict('player')['valueToID']
			
			for idx, val in ref_table.copy().iterrows():
				# 진도율 확인용
				if idx % 3000 == 0:
					print(idx)

				gameDivide = temp_df[(temp_df['date'].isin([(pd.to_datetime(val['date']) + timedelta(days=x)).strftime('%Y-%m-%d') for x in self.date_range])) & (temp_df['league']==val['league_name'])]
				for gameID in gameDivide['gameid'].unique():
					each_game = gameDivide[gameDivide['gameid']==gameID]
					if each_game.empty:
						continue
					if (val['team_1'] in each_game['team'].unique()) & (val['team_2'] in each_game['team'].unique()) & (val['set_number']==each_game['game'].unique()[0]):
						
						for eachTeam in each_game['team'].unique():
							each_team_df = each_game[each_game['team']==eachTeam]

							if each_team_df.shape[0] != 6:
								print('Shape[0] is not 6')
								print(each_team_df)
								continue
							
							if each_team_df[each_team_df['position']=='team']['team'].values[0] == val['team']:
								for _, val2 in each_team_df.iterrows():
									if val2['position'] == 'top':
										ref_table.loc[idx, 'top_player'] = val2['player']
									elif val2['position'] == 'jng':
										ref_table.loc[idx, 'jg_player'] = val2['player']
									elif val2['position'] == 'mid':
										ref_table.loc[idx, 'mid_player'] = val2['player']
									elif val2['position'] == 'bot':
										ref_table.loc[idx, 'bot_player'] = val2['player']
									elif val2['position'] == 'sup':
										ref_table.loc[idx, 'sup_player'] = val2['player']
									else:
										ref_table.loc[idx, 'result'] = val2['result']
										ref_table.loc[idx, 'side'] = val2['side']
										ref_table.loc[idx, 'ban1'] = val2['ban1']
										ref_table.loc[idx, 'ban2'] = val2['ban2']
										ref_table.loc[idx, 'ban3'] = val2['ban3']
										ref_table.loc[idx, 'ban4'] = val2['ban4']
										ref_table.loc[idx, 'ban5'] = val2['ban5']
										ref_table.loc[idx, 'team_kills'] = val2['teamkills']
										ref_table.loc[idx, 'team_deaths'] = val2['teamdeaths']
										ref_table.loc[idx, 'team_double'] = val2['doublekills']
										ref_table.loc[idx, 'team_triple'] = val2['triplekills']
										ref_table.loc[idx, 'team_quadra'] = val2['quadrakills']
										ref_table.loc[idx, 'team_penta'] = val2['pentakills']
										ref_table.loc[idx, 'team_first_blood'] = val2['firstblood']
										ref_table.loc[idx, 'team_kpm'] = val2['team kpm']
										ref_table.loc[idx, 'team_first_dragon'] = val2['firstdragon']
										ref_table.loc[idx, 'team_dragon_kills'] = val2['dragons']
										ref_table.loc[idx, 'team_elder_kills'] = val2['elders']
										ref_table.loc[idx, 'team_first_rift'] = val2['firstherald']
										ref_table.loc[idx, 'team_rift_kills'] = val2['heralds']
										ref_table.loc[idx, 'team_first_baron'] = val2['firstbaron']
										ref_table.loc[idx, 'team_baron_kills'] = val2['barons']
										ref_table.loc[idx, 'team_first_tower'] = val2['firsttower']
										ref_table.loc[idx, 'team_tower_kills'] = val2['towers']
										ref_table.loc[idx, 'team_first_midtower'] = val2['firstmidtower']
										ref_table.loc[idx, 'team_first_three_towers'] = val2['firsttothreetowers']
										ref_table.loc[idx, 'team_inhib_kills'] = val2['inhibitors']
										ref_table.loc[idx, 'team_total_gold'] = val2['totalgold']
										ref_table.loc[idx, 'team_earned_gold'] = val2['earnedgold']
										ref_table.loc[idx, 'team_minion_kills'] = val2['minionkills']
										ref_table.loc[idx, 'team_monster_kills'] = val2['monsterkills']
										ref_table.loc[idx, 'team_goldat10'] = val2['goldat10']
										ref_table.loc[idx, 'team_csat10'] = val2['csat10']
										ref_table.loc[idx, 'team_golddiffat10'] = val2['golddiffat10']
										ref_table.loc[idx, 'team_csdiffat10'] = val2['csdiffat10']
										ref_table.loc[idx, 'team_goldat15'] = val2['goldat15']
										ref_table.loc[idx, 'team_csat15'] = val2['csat15']
										ref_table.loc[idx, 'team_golddiffat15'] = val2['golddiffat15']
										ref_table.loc[idx, 'team_csdiffat15'] = val2['csdiffat15']

			ref_table = ref_table.where(pd.notnull(ref_table), None)
			player_dict = db.get_dict('player')['valueToID']
			ref_table['top_player_id'] = ref_table['top_player'].replace(player_dict)
			ref_table['jg_player_id'] = ref_table['jg_player'].replace(player_dict)
			ref_table['mid_player_id'] = ref_table['mid_player'].replace(player_dict)
			ref_table['bot_player_id'] = ref_table['bot_player'].replace(player_dict)
			ref_table['sup_player_id'] = ref_table['sup_player'].replace(player_dict)

			champion_dict = db.get_dict('champion')['valueToID']
			ref_table['ban1_id'] = ref_table['ban1'].replace(champion_dict)
			ref_table['ban2_id'] = ref_table['ban2'].replace(champion_dict)
			ref_table['ban3_id'] = ref_table['ban3'].replace(champion_dict)
			ref_table['ban4_id'] = ref_table['ban4'].replace(champion_dict)
			ref_table['ban5_id'] = ref_table['ban5'].replace(champion_dict)

			ref_table['wdl'] = ref_table['result'].apply(set_match_info_result_to_wdl)

			return ref_table.reset_index(drop=True)

		elif table_name == 'set_match_player_performance':
			ref_table = db.extend_idToValue(ref_table, 'set_match_info_by_team')
			ref_table = db.extend_idToValue(ref_table, 'player')
			ref_table = db.extend_idToValue(ref_table, 'set_match')
			ref_table = db.extend_idToValue(ref_table, 'match')
			ref_table = db.extend_idToValue(ref_table, 'team', 'home_team_id', rename={'team_name':'team_1'})
			ref_table = db.extend_idToValue(ref_table, 'team', 'away_team_id', rename={'team_name':'team_2'})
			ref_table = db.extend_idToValue(ref_table, 'team', 'team_id', rename={'team_name':'team'})
			ref_table = db.extend_idToValue(ref_table, 'league', 'league_id')
			self.reference_table = ref_table

			for idx, val in ref_table.copy().iterrows():
				gameDivide = temp_df[(temp_df['date'].isin([(pd.to_datetime(val['date']) + timedelta(days=x)).strftime('%Y-%m-%d') for x in self.date_range])) & (temp_df['league']==val['league_name'])]
				for gameID in gameDivide['gameid'].unique():
					each_game = gameDivide[gameDivide['gameid']==gameID]
					if each_game.empty:
						continue
					if (val['team_1'] in each_game['team'].unique()) & (val['team_2'] in each_game['team'].unique()) & (val['set_number']==each_game['game'].unique()[0]):
						if each_game.shape[0] != 12:
							print('Shape[0] is not 12')
							print(each_game)
							continue
						
						each_player = each_game[each_game['player']==val['player_name']]
						if each_player.empty:
							continue
						ref_table.loc[idx, 'kills'] = each_player['kills'].values[0]
						ref_table.loc[idx, 'deaths'] = each_player['deaths'].values[0]
						ref_table.loc[idx, 'assists'] = each_player['assists'].values[0]
						ref_table.loc[idx, 'champion'] = each_player['champion'].values[0]
						ref_table.loc[idx, 'double'] = each_player['doublekills'].values[0]
						ref_table.loc[idx, 'triple'] = each_player['triplekills'].values[0]
						ref_table.loc[idx, 'quadra'] = each_player['quadrakills'].values[0]
						ref_table.loc[idx, 'penta'] = each_player['pentakills'].values[0]
						ref_table.loc[idx, 'first_blood'] = each_player['firstblood'].values[0]
						ref_table.loc[idx, 'total_gold'] = each_player['totalgold'].values[0]
						ref_table.loc[idx, 'earned_gold'] = each_player['earnedgold'].values[0]
						ref_table.loc[idx, 'total_cs'] = each_player['total cs'].values[0]
						ref_table.loc[idx, 'minion_kills'] = each_player['minionkills'].values[0]
						ref_table.loc[idx, 'monster_kills'] = each_player['monsterkills'].values[0]
						ref_table.loc[idx, 'monster_kills_own_jg'] = each_player['monsterkillsownjungle'].values[0]
						ref_table.loc[idx, 'monster_kills_enemy_jg'] = each_player['monsterkillsenemyjungle'].values[0]
						ref_table.loc[idx, 'cspm'] = each_player['cspm'].values[0]
						ref_table.loc[idx, 'goldat10'] = each_player['goldat10'].values[0]
						ref_table.loc[idx, 'golddiffat10'] = each_player['golddiffat10'].values[0]
						ref_table.loc[idx, 'goldat15'] = each_player['goldat15'].values[0]
						ref_table.loc[idx, 'golddiffat15'] = each_player['golddiffat15'].values[0]
						ref_table.loc[idx, 'csat10'] = each_player['csat10'].values[0]
						ref_table.loc[idx, 'csdiffat10'] = each_player['csdiffat10'].values[0]
						ref_table.loc[idx, 'csat15'] = each_player['csat15'].values[0]
						ref_table.loc[idx, 'csdiffat15'] = each_player['csdiffat15'].values[0]
				
				if idx % 10000 == 0:
					print(idx)

			ref_table = ref_table.where(pd.notnull(ref_table), None)
			ref_table = ref_table.dropna(subset=['player_id']).reset_index(drop=True)
			ref_table = ref_table[ref_table['player_name'] != 'unknown player'].reset_index(drop=True)
			ref_table['champion_id'] = ref_table['champion'].replace(db.get_dict('champion')['valueToID'])
			return ref_table.reset_index(drop=True)