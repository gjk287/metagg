import pandas as pd
import glob
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
from database import DB
from preprocess import GamepediaDict

db = DB()
db.initialise()

def main():
	result_list = list()
	for file in glob.glob(r'C:\Users\james\Desktop\metagg_fork\LOL\datasets\RawData\MatchHistory\team\*csv'):
		df = pd.read_csv(file)
		df = df[df['state']=='OK']
		
		if not df.empty:
			# print(file)
			result = df.loc[13, 'result']
			result_list.append(result)
	print(set(result_list))
			


if __name__ == '__main__':
	main()




