import pandas as pd
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from database import DB

db = DB()
db.initialise()

def main():
	PATH = r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta.gg\LOL\datasets\DerivedData\DB_table\set_match\set_match_mvp.csv'
	df = pd.read_csv(PATH)
	#PATH2 = r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta.gg\LOL\datasets\DerivedData\DB_table\player\player_unique2.csv'
	#df2 = pd.read_csv(PATH2)
	temp_df = db.get_table('player')
	print(set(df['mvp']) - set(temp_df['player_name']))

	#print(df['mvp'].unique())


if __name__ == '__main__':
	main()




