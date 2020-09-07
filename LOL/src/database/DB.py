import psycopg2
import pandas as pd
import sys
import os
import glob
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Database, CurFromConnPool
from utils import GameDictionary
from date_utils import stringDate_to_strft
from database_utils import tableUniqueKey, tableFK_dict, tablePK_dict, func_extend_idToValue


class DB(object):
	def __init__(self, host='loldbinstance.crj9bbxpdcgf.ap-northeast-2.rds.amazonaws.com', database='meta-gg', user='postgres', password='Rlwjd132'):
		self.host = host
		self.database = database
		self.user = user
		self.__password = password
		self.tableUniqueKey = tableUniqueKey
		self.tableFK_dict = tableFK_dict
		self.tablePK_dict = tablePK_dict
		
	def initialise(self):
		Database.initialise(host=self.host, database=self.database, user=self.user, password=self.__password)
		return

	# update할 테이블에 primary key가 붙어있어야함
	def update_table(self, df, table_name, update_cols):
		# pk in DB, pk dict
		pk = self.tablePK_dict[table_name]
		pk_dict = self.get_dict(table_name)['idToValue']

		# change nan to None and drop na for pk
		df = df.where(pd.notnull(df), None)
		df = df.dropna(subset=[pk])

		with CurFromConnPool() as cur:
			for _, val in df.iterrows():
				val_list = []
				for col in update_cols:
					if type(val[col]) == str:
						val_list.append(f"{col}='{val[col]}'")
					elif val[col] is None:
						pass
					else:
						val_list.append(f"{col}={val[col]}")

				if len(val_list) == 0:
					continue

				pk_value = val[pk]
				# pk가 존재할때만 update해주기
				if pk_value in pk_dict.keys():
					cur.execute(f"UPDATE {table_name}\
						SET {', '.join(val_list)}\
							WHERE {pk}={pk_value}")
				else:
					pass
		return print(f'{table_name} update completed!')

	def get_dict(self, table_name):
		table = self.get_table(table_name)
		output_dict = dict()
		uniqueCol = self.tableUniqueKey[table_name]
		fk = self.tableFK_dict[table_name]
		pk = self.tablePK_dict[table_name]

		idValue_dict = dict()
		valueID_dict = dict()
		if table.empty:
			output_dict['idToValue'] = idValue_dict
			output_dict['valueToID'] = valueID_dict
			output_dict['uniqueColumn'] = uniqueCol
			output_dict['FK'] = fk

		else:
			for _, val in table.iterrows():
				key_val_list = []
				for col in uniqueCol:
					if col == 'date':
						key_val_list.append(stringDate_to_strft(val[col]))
					else:
						key_val_list.append(val[col])
				idValue_dict[val[pk]] = tuple(list(key_val_list))
				valueID_dict[tuple(list(key_val_list))] = val[pk]
			
			output_dict['idToValue'] = idValue_dict
			output_dict['valueToID'] = valueID_dict
			output_dict['uniqueColumn'] = uniqueCol
			output_dict['FK'] = fk
		return output_dict


	def pkInput(self, df, table_name):
		# 만약에 id가 하나라도 있어서 dictionary를 불러올 수 있을때
		df = df.dropna(subset=list(self.tableUniqueKey[table_name]), how='all').reset_index(drop=True)
		df = df.where(pd.notnull(df), None)
		try:
			pk_dict = self.get_dict(table_name)['idToValue']
			uniqueCol = self.tableUniqueKey[table_name]
			print(f'Got {table_name} dictionary!\n--------------------------------------')

			with CurFromConnPool() as cur:
				for _, val in df.iterrows():
					key_value = tuple(list(val[uniqueCol]))
					if key_value not in pk_dict.values():
						cur.execute(f"INSERT INTO {table_name}({', '.join(uniqueCol)})\
							VALUES ({'%s' + (', %s' * (len(uniqueCol) - 1))})", tuple(key_value))
					else:
						continue
		# id가 하나도 없어서 dictionary를 불러오지 못하면 그냥 있는대로 다 넣기
		except:
			print('It does not have any id yet!')
			uniqueCol = self.tableUniqueKey[table_name]
			with CurFromConnPool() as cur:
				for _, val in df.iterrows():
					key_value = tuple(list(val[uniqueCol]))
					cur.execute(f"INSERT INTO {table_name}({', '.join(uniqueCol)})\
						VALUES ({'%s' + (', %s' * (len(uniqueCol) - 1))})", tuple(key_value))
		print(f'Table: {table_name} input done!')
		return


	def get_table(self, table_name):
		if table_name == 'match_schedule':
			df = pd.read_csv('League_of_Legends\\datasets\\DerivedData\\None_DB_table\\game_schedule.csv')
			
			if df.empty:
				df = pd.read_csv(r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta-gg\League_of_Legends\datasets\DerivedData\None_DB_table\game_schedule.csv')
			return df.where(pd.notnull(df), None)

		else:
			with CurFromConnPool() as cur:
				cur.execute('SELECT * FROM {}'.format(table_name))
				column_names = [desc[0] for desc in cur.description]
				table = pd.DataFrame(cur.fetchall(), columns=column_names)
				if 'date' in column_names:
					table['date'] = table['date'].apply(stringDate_to_strft)
				return table


	def get_table_name(self, view=False):
		if not view:
			with CurFromConnPool() as cur:
				cur.execute("SELECT table_name FROM information_schema.tables\
					WHERE table_schema=%s AND table_type=%s", ('public', 'BASE TABLE', ))
				column_names = [desc[0] for desc in cur.description]
				table = pd.DataFrame(cur.fetchall(), columns=column_names)
		else:
			with CurFromConnPool() as cur:
				cur.execute("select table_name as view_name from information_schema.views \
					where table_schema not in (%s, %s) \
						order by view_name", ('information_schema', 'pg_catalog',))
				column_names = [desc[0] for desc in cur.description]
				table = pd.DataFrame(cur.fetchall(), columns=column_names)
		return table

	def get_table_columns(self, table_name):
		with CurFromConnPool() as cur:
			cur.execute('SELECT * FROM {}'.format(table_name))
			column_names = [desc[0] for desc in cur.description]
			return column_names


	def extend_idToValue(self, df, table_name, id_name=None, drop=False, rename=None):
		df_copy = df.copy()
		if id_name:
			pass
		else:
			id_name = self.tablePK_dict[table_name]
		matching_dict = self.get_dict(table_name)
		df_copy[matching_dict['uniqueColumn']] = df_copy[id_name].apply(lambda row: func_extend_idToValue(matching_dict, row))

		if rename:
			df_copy = df_copy.rename(columns=rename)

		if drop:
			return df_copy.drop(id_name, axis=1)
		return df_copy