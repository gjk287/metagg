import pandas as pd

def main():
	PATH = r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta.gg\LOL\datasets\RawData\MatchHistory\team\LCK-2020-spring-team.csv'
	df = pd.read_csv(PATH)
	#PATH2 = r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta.gg\LOL\datasets\DerivedData\DB_table\player\player_unique2.csv'
	#df2 = pd.read_csv(PATH2)

	df['game_length'] = df['game_length'].apply(time_to_sec)
	print(df[['year', 'season', 'team_1', 'team_2', 'set_number', 'total_kills', 'game_length']])
	df_groupby = df.groupby(['year', 'season', 'week', 'team_1', 'team_2', 'league_name', 'set_number']).sum()

	df = df.set_index(['year', 'season', 'week', 'team_1', 'team_2', 'league_name', 'set_number'])

	for idx, _ in df.iterrows():
		ckill = df_groupby.loc[idx, 'total_kills']
		df.loc[idx, 'ckill'] = ckill
		
	df = df.reset_index()
	df['ckpm'] = df.apply(lambda row: ckpm_feature(row['ckill'], row['game_length']), axis=1)
	print(df[['year', 'season', 'team_1', 'team_2', 'set_number', 'total_kills', 'game_length', 'ckill', 'ckpm']])
	df.to_csv('temp_ddd.csv', index=False)


def time_to_sec(string):
	try:
		min = int(string.split(':')[0])
		sec = int(string.split(':')[-1])
		return 60 * min + sec
	except:
		return None

def ckpm_feature(ckill, game_length):
	return ckill / game_length * 60

if __name__ == '__main__':
	main()




