import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import tableUniqueKey
from database import DB

db = DB()
db.initialise()

def main():
	pass

def preprocess_and_save(data_name=None, table_name=None, save=True):
	if data_name == 'league':
		league_value = [['LCK', 'Korea', 1], ['LPL', 'China', 1], ['LEC', 'Europe', 1],
						['LCS', 'North America', 1], ['BL', 'Belgium', 2], ['BRCC', 'Brazil', 2],
						['CBLOL', 'Brazil', 1], ['Challengers Korea', 'Korea', 2], ['CIS_CL', 'Commonwealth Independent States', 2],
						['DL', 'Dutch', 2], ['ECS', 'Taiwas', 2], ['EM', 'Europe', 2], ['LCL', 'Commonwealth Independent States', 1],
						['LCS_a', 'North America', 2], ['LDL', 'China', 2], ['LJL', 'Japan', 1],
						['LLA', 'Latin America', 1], ['LMS', 'Tawian', 1], ['LPLOL', 'Portugal', 2],
						['OCS', 'Oceania', 2], ['OPL', 'Oceania', 1], ['PCS', 'Taiwan/HongKong/Macau', 1],
						['PGN', 'Italy', 2], ['TCL', 'Turkey', 1], ['TPL_a', 'Turkey', 2], ['VCS', 'Vietnam', 1],
						['KeSPA', 'Korea', 0], ['WCS', 'Worlds', 0], ['MSI', 'Worlds', 0]]
		df = pd.DataFrame(data=league_value, columns=['league_name', 'league_country', 'league_division'])
		# path
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{data_name}\\{data_name}_unique.csv'
		
		# save rest of info
		df.to_csv(f'LOL\\datasets\\DerivedData\\DB_table\\{data_name}\\{data_name}.csv', index=False)
		
		# change for unique
		df = df[tableUniqueKey[data_name]]

	elif data_name == 'betting_site':
		betting_site_value = [['Unikrn'], ['Betjoe'], ['Oddsportal']]
		df = pd.DataFrame(data=betting_site_value, columns=['betting_site'])
		# path
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{data_name}\\{data_name}_unique.csv'

		# change for unique
		df = df[tableUniqueKey[data_name]]

	elif data_name == 'set_match_player_performance':
		temp_df = pd.read_csv(f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\DerivedData\\DB_table\\set_match_info_by_team\\set_match_info_by_team_details.csv')
		
		playerDict = db.get_dict('player')['valueToID']
		temp_df['top_player_id'] = temp_df['top_player'].replace(playerDict)
		temp_df['jg_player_id'] = temp_df['jg_player'].replace(playerDict)
		temp_df['mid_player_id'] = temp_df['mid_player'].replace(playerDict)
		temp_df['bot_player_id'] = temp_df['bot_player'].replace(playerDict)
		temp_df['sup_player_id'] = temp_df['sup_player'].replace(playerDict)
		set_match_player_performance = temp_df[['set_match_info_by_team_id', 'league_name', 'year', 'season', 'date', 'team_1', 'team_2', 'set_number', 'match_round', 'tiebreaker', 'league_id', 'match_id', 'home_team_id', 'away_team_id']]

		# iterate through players and concat all
		concat_df = pd.DataFrame()
		iter_col = ['top_player_id', 'jg_player_id', 'mid_player_id', 'bot_player_id', 'sup_player_id']
		for col in iter_col:
			temp_player_df = temp_df[['set_match_info_by_team_id', col]]
			temp_player_df.columns = ['set_match_info_by_team_id', 'player_id']
			merged_df = pd.merge(set_match_player_performance, temp_player_df, how='inner', left_on='set_match_info_by_team_id', right_on='set_match_info_by_team_id')
			concat_df = pd.concat([concat_df, merged_df]).reset_index(drop=True)

		df = concat_df
		df = df.dropna(subset=['player_id']).reset_index(drop=True)
		# drop unknown player
		df = df[df['player_id'] != 549]

		# path
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{data_name}\\{data_name}_unique.csv'

		# change for unique
		df = df[tableUniqueKey[data_name]]


	elif data_name == 'bet_type':
		if table_name == 'bet_type_special':
			bet_type_value = ['2-0', '2-1', '3-0', '3-1', '3-2', 'penta', 'quadra', 'second_dragon', 'third_dragon',
                                'first_5kill', 'first_10kill', 'first_baron', 'first_blood', 'first_dragon', 'first_inhib',
                                'first_rift', 'first_tower', 'game_win', 'set_win']
			df = pd.DataFrame(data=bet_type_value, columns = ['bet_name'])

		elif table_name == 'bet_type_ou':
			bet_type_value = [['game_time', '45:00', 'over'], ['game_time', '45:00', 'under'], 
                           ['total_baron', '1.5', 'over'], ['total_baron', '1.5', 'under'],
                           ['total_dragon', '4.5', 'over'], ['total_dragon', '4.5', 'under'],
                           ['total_inhib', '1.5', 'over'], ['total_inhib', '1.5', 'under'],
                           ['total_inhib', '2.5', 'over'], ['total_inhib', '2.5', 'under'],
                           ['total_sets', '2.5', 'over'], ['total_sets', '2.5', 'under'],
                           ['total_sets', '3.5', 'over'], ['total_sets', '3.5', 'under'],
                           ['total_sets', '4.5', 'over'], ['total_sets', '4.5', 'under'],
                           ['total_tower', '11.5', 'over'], ['total_tower', '11.5', 'under'],
                           ['total_tower', '12.5', 'over'], ['total_tower', '12.5', 'under'],
                           ['total_kill', '10.5', 'over'], ['total_kill', '10.5', 'under'],
                           ['total_kill', '11.5', 'over'], ['total_kill', '11.5', 'under'],
                           ['total_kill', '12.5', 'over'], ['total_kill', '12.5', 'under'],
                           ['total_kill', '13.5', 'over'], ['total_kill', '13.5', 'under'],
                           ['total_kill', '14.5', 'over'], ['total_kill', '14.5', 'under'],
                           ['total_kill', '15.5', 'over'], ['total_kill', '15.5', 'under'],
                           ['total_kill', '16.5', 'over'], ['total_kill', '16.5', 'under'],
                           ['total_kill', '17.5', 'over'], ['total_kill', '17.5', 'under'],
                           ['total_kill', '18.5', 'over'], ['total_kill', '18.5', 'under'],
                           ['total_kill', '19.5', 'over'], ['total_kill', '19.5', 'under'],
                           ['total_kill', '20.5', 'over'], ['total_kill', '20.5', 'under'],
                           ['total_kill', '21.5', 'over'], ['total_kill', '21.5', 'under'],
                           ['total_kill', '22.5', 'over'], ['total_kill', '22.5', 'under'],
                           ['total_kill', '23.5', 'over'], ['total_kill', '23.5', 'under'],
                           ['total_kill', '24.5', 'over'], ['total_kill', '24.5', 'under'],
                           ['total_kill', '25.5', 'over'], ['total_kill', '25.5', 'under'],
                           ['total_kill', '26.5', 'over'], ['total_kill', '26.5', 'under'],
                           ['total_kill', '27.5', 'over'], ['total_kill', '27.5', 'under'],
                           ['total_kill', '28.5', 'over'], ['total_kill', '28.5', 'under'],
                           ['total_kill', '29.5', 'over'], ['total_kill', '29.5', 'under'],
                           ['total_kill', '30.5', 'over'], ['total_kill', '30.5', 'under'],
                           ['total_kill', '31.5', 'over'], ['total_kill', '31.5', 'under'],
                           ['total_kill', '32.5', 'over'], ['total_kill', '32.5', 'under'],
                           ['total_kill', '33.5', 'over'], ['total_kill', '33.5', 'under'],
                           ['total_kill', '34.5', 'over'], ['total_kill', '34.5', 'under'],
                           ['total_kill', '35.5', 'over'], ['total_kill', '35.5', 'under'],
                           ['total_kill', '36.5', 'over'], ['total_kill', '36.5', 'under'],
                           ['total_kill', '37.5', 'over'], ['total_kill', '37.5', 'under'],
                           ['total_kill', '38.5', 'over'], ['total_kill', '38.5', 'under'],
                           ['total_kill', '39.5', 'over'], ['total_kill', '39.5', 'under'],
                           ['total_kill', '40.5', 'over'], ['total_kill', '40.5', 'under']]
			df = pd.DataFrame(data=bet_type_value, columns = ['bet_name', 'threshold', 'over_under'])
		
		elif table_name == 'bet_type_handicap':
			bet_type_value = [['set_handicap', '1.5'], ['set_handicap', '-1.5'],
                                 ['set_handicap', '2.5'], ['set_handicap', '-2.5'],
                                 ['total_kill_handicap', '0.5'], ['total_kill_handicap', '-0.5'],
                                 ['total_kill_handicap', '1.5'], ['total_kill_handicap', '-1.5'],
                                 ['total_kill_handicap', '2.5'], ['total_kill_handicap', '-2.5'],
                                 ['total_kill_handicap', '3.5'], ['total_kill_handicap', '-3.5'],
                                 ['total_kill_handicap', '4.5'], ['total_kill_handicap', '-4.5'],
                                 ['total_kill_handicap', '5.5'], ['total_kill_handicap', '-5.5'],
                                 ['total_kill_handicap', '6.5'], ['total_kill_handicap', '-6.5'],
                                 ['total_kill_handicap', '7.5'], ['total_kill_handicap', '-7.5'],
                                 ['total_kill_handicap', '8.5'], ['total_kill_handicap', '-8.5'],
                                 ['total_kill_handicap', '9.5'], ['total_kill_handicap', '-9.5'],
                                 ['total_kill_handicap', '10.5'], ['total_kill_handicap', '-10.5'],
                                 ['total_kill_handicap', '11.5'], ['total_kill_handicap', '-11.5'],
                                 ['total_kill_handicap', '12.5'], ['total_kill_handicap', '-12.5'],
                                 ['total_kill_handicap', '13.5'], ['total_kill_handicap', '-13.5'],
                                 ['total_kill_handicap', '14.5'], ['total_kill_handicap', '-14.5'],
                                 ['total_kill_handicap', '15.5'], ['total_kill_handicap', '-15.5'],
                                 ['total_kill_handicap', '16.5'], ['total_kill_handicap', '-16.5'],
                                 ['total_kill_handicap', '17.5'], ['total_kill_handicap', '-17.5'],
                                 ['total_kill_handicap', '18.5'], ['total_kill_handicap', '-18.5'],
                                 ['total_kill_handicap', '19.5'], ['total_kill_handicap', '-19.5']]
			df = pd.DataFrame(data=bet_type_value, columns = ['bet_name', 'handicap_amount'])

		elif table_name == 'bet_type_both':
			bet_type_value = [['both_team_tower', 'yes'], ['both_team_tower', 'no'],
                             ['both_team_baron', 'yes'], ['both_team_baron', 'no'],
                             ['both_team_dragon', 'yes'], ['both_team_dragon', 'no'],
                             ['both_team_inhib', 'yes'], ['both_team_inhib', 'no']]
			df = pd.DataFrame(data=bet_type_value, columns = ['bet_name', 'yes_no'])

		elif table_name == 'bet_type_correct_number':
			bet_type_value = [['total_dragon', 2], ['total_dragon', 3],
							['total_dragon', 4], ['total_dragon', 5],
							['total_dragon', 6], ['total_dragon', 7],
							['total_baron', 0], ['total_baron', 1], 
							['total_baron', 2], ['total_baron', 3], 
							['total_baron', 4], ['total_tower', 7], 
							['total_tower', 8], ['total_tower', 9], 
							['total_tower', 10], ['total_tower', 11], 
							['total_tower', 12], ['total_tower', 13], 
							['total_tower', 14], ['total_tower', 15], 
							['total_tower', 16], ['total_tower', 17], 
							['total_tower', 18], ['total_tower', 19]]

		

		# path
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique.csv'

		# change for unique
		df = df[tableUniqueKey[table_name]]

	else:
		print(f'{table_name} cannot be created. Please check again')

	
	if save:
		try:
			df.to_csv(newPath, index=False)
		except:
			newPath = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\{newPath}'
			df.to_csv(newPath, index=False)
	else:
		return df


if __name__ == "__main__":
	main()