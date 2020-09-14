import glob
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from preprocess import MatchHistory
from database import DB
from utils import tableUniqueKey, tablePK_dict

db = DB()
db.initialise()


def main():
	preprocess_and_save('player', 'player')
	


def preprocess_and_save(table_name=None, table_type='player', save=True):
	df = pd.DataFrame()
	for file in glob.glob(f'LOL\\datasets\\RawData\\MatchHistory\\{table_type}\\*csv'):
		temp_df = pd.read_csv(file)
		temp_df = temp_df[temp_df['state']=='OK']
		
		# skip empty df
		if temp_df.empty:
			continue

		mh = MatchHistory(temp_df)
		if table_name in ['player', 'champion']:
			temp_df = mh.pp(table_name, table_type)
		elif table_name in ['set_match', 'set_match_info_by_team']:
			ref_table = pd.read_csv(f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_pk.csv')
			temp_df = mh.pp(table_name, table_type, ref_table)

		df = pd.concat([df, temp_df]).reset_index(drop=True)

	# drop duplicates
	df = df.drop_duplicates()

	df_unique = df[tableUniqueKey[table_name]]
	df_all_columns = list(set(df.columns) & set(db.get_table_columns(table_name)))
	df_all = df[df_all_columns]
	
	if table_type == 'player':
		# path
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique2.csv'
		newPathAll = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_all2.csv'
	elif table_type == 'team':
		# path
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique3.csv'
		newPathAll = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_all3.csv'

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
		return df_all



if __name__ == '__main__':
	main()