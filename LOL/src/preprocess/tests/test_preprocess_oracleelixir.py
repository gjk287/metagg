import glob
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from preprocess import OracleElixir
from utils import get_OracleElixir


def main():
	preprocess_and_save('champion')

def preprocess_and_save(table_name=None, save=True):
	temp_df = get_OracleElixir()
	elixir = OracleElixir(temp_df)
	if table_name == 'player':
		df = elixir.pp(table_name)
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique.csv'

	elif table_name == 'champion':
		df = elixir.pp(table_name)
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_unique.csv'

	elif table_name == 'match':
		ref_table = pd.read_csv(f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_pk.csv')
		df = elixir.pp(table_name, ref_table)
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_patch.csv'

	elif table_name == 'set_match':
		ref_table = pd.read_csv(f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_pk.csv')
		df = elixir.pp(table_name, ref_table)
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_ckpm_gamelength.csv'

	elif table_name == 'set_match_info_by_team':
		ref_table = pd.read_csv(f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_pk.csv')
		df = elixir.pp(table_name, ref_table)
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_details.csv'

	elif table_name == 'set_match_player_performance':
		ref_table = pd.read_csv(f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_pk.csv')
		df = elixir.pp(table_name, ref_table)
		newPath = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\{table_name}_details.csv'

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