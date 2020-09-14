import glob
import pandas as pd
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))
from database import DB
from utils import tableUniqueKey, tablePK_dict

db = DB()
db.initialise()

def main():
	update_table('set_match')

def update_table(table_name='all'):
	PATH = f'LOL\\datasets\\DerivedData\\DB_table\\{table_name}\\*csv'
	table_columns = db.get_table_columns(table_name)
	updatable_cols_set = set(table_columns) - set(tableUniqueKey[table_name]) - set([tablePK_dict[table_name]])
	pk_col = [tablePK_dict[table_name]]
	unique_cols = tableUniqueKey[table_name]

	for file in glob.glob(PATH):
		if ('_pk' not in file) and ('_unique' not in file):
			temp_df = pd.read_csv(file)
			col_to_update = list(updatable_cols_set.intersection(temp_df.columns))
			# if nothing to update continue
			if not col_to_update:
				print(f'{file} skipped\n')
				continue

			# if pk exists
			if set(pk_col) <= set(temp_df.columns):
				db.update_table(temp_df, table_name, col_to_update)

			# else use unique colu mns
			elif set(unique_cols) <= set(temp_df.columns):
				temp_df = db.extend_valueToID(temp_df, table_name)
				db.update_table(temp_df, table_name, col_to_update)
			
			# if there is not enough pk or unique columns
			else:
				print('Not enough pk or unique columns')
				


if __name__ == "__main__":
	main()