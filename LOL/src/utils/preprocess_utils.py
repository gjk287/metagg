import pandas as pd
from collections import Counter
import glob

def get_df_with_3set(base_df):
	# get number of sets from result value. ex: 2-1 = 3 sets
	base_df['num_of_set'] = base_df['result'].apply(numOfSet)
	# using num_of_set column, 세트 경기만큼 row가 늘어난 테이블 생성
	df = pd.DataFrame([base_df.loc[idx] for idx in base_df.index for _ in range(base_df.loc[idx]['num_of_set'])]).reset_index(drop=True)
	# 기본값으로 일단 set_number = 1을 주고, iterate하는데 idx-1의 row에서 set_number를 제외한 모든게 같은 경우 set_number를 1 올려줌
	# 값이 달라지면 다시 set_number = 1로 시작
	set_number = 1
	df['set_number'] = set_number
	for idx, val in df.copy().iterrows():
		if idx != 0:
			if val[df.columns != 'set_number'].equals(df.loc[idx-1, df.columns != 'set_number']):
				set_number += 1
				df.loc[idx, 'set_number'] = set_number
			else:
				set_number = 1
				df.loc[idx, 'set_number'] = set_number

	df = df.drop('num_of_set', axis=1)
	return df

def numOfSet(string):
	if string:
		num1 = int(string.split('-')[0])
		num2 = int(string.split('-')[-1])
		return num1 + num2
	else:
		return 3

def oddsToFloat(string):
	try:
		return float(string)
	except:
		return None

def matchTypeToSeason(string):
	if 'Season' in string:
		season = string.split(' Season')[0].lower()
	elif ('Play Offs' in string) | ('Play offs' in string):
		season = 'playoffs'
	else:
		season = None
	return season

def check_duplicate_player(player_list):
	player_list = [player.lower() for player in player_list]
	return [k for k,v in Counter(player_list).items() if v>1]

def get_OracleElixir():
	oe_df = pd.DataFrame()
	for file in glob.glob(r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta.gg\LOL\datasets\RawData\OracleElixir\*csv'):
		temp_df = pd.read_csv(file)
		oe_df = pd.concat([oe_df, temp_df])
	return oe_df.reset_index(drop=True)

def get_matchSchedule():
	try:
		df = pd.read_csv(r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta.gg\LOL\datasets\DerivedData\None_DB_table\game_schedule.csv')
	except:
		df = pd.read_csv('LOL\\datasets\\DerivedData\\None_DB_table\\game_schedule.csv')
	return df

def toWDL(string, homeAway='home'):
	try:
		num1 = int(string.split('-')[0])
		num2 = int(string.split('-')[-1])
		if homeAway=='home':
			if num1 > num2:
				return 'W'
			elif num1 < num2:
				return 'L'
			else:
				return 'D'
		else:
			if num1 > num2:
				return 'L'
			elif num1 < num2:
				return 'W'
			else:
				return 'D'
	except:
		return None

def result_opp(string):
	try:
		num1 = string.split('-')[0]
		num2 = string.split('-')[-1]
		return f'{num2}-{num1}'
	except:
		return None

def result_FFW(string):
	if string == 'W-F':
		result = '1-0'
	elif string == 'F-F':
		result = '0-1'
	else:
		result = string
	return result

def set_match_info_result_to_wdl(string):
	try:
		if int(string) == 1:
			return 'W'
		elif int(string) == 0:
			return 'L'
	except:
		return None

def change_fb_matchhistory(df):
	first_blood_t = df['first_blood'].value_counts().idxmin()
	df['first_blood'] = df['first_blood'].apply(lambda x: 1 if x==first_blood_t else 0)
	return df

def time_to_sec(string):
	try:
		min = int(string.split(':')[0])
		sec = int(string.split(':')[-1])
		return 60 * min + sec
	except:
		return None

def ckpm_feature(ckill, game_length):
	return ckill / game_length * 60

def matchhistory_kmil(string):
	if 'k' in string:
		num = float(string.split('k')[0]) * 1000
	
	elif 'mil' in string:
		num = float(string.split('mil')[0]) * 1000

	else:
		num = None
	return num

def matchhistory_int_column(string):
	try:
		num = int(string)
	except:
		num = None
	return num

set_match_url_column_dict = {
	'MH': 'match_history_url',
	'PB': 'vod_pick_ban_url',
	'Start': 'vod_start_url',
	'HL': 'vod_highlight_url',
	'Vod': 'vod_url',
	'MVP': 'mvp',
	'Post': 'vod_post_url'
}