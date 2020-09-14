import glob
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from preprocess import Oddsportal


def main():
	pass

def preprocess_and_save():
	df = pd.DataFrame()
	for file in glob.glob('LOL\\datasets\\RawData\\Oddsportal\\*csv'):
		temp_df = pd.read_csv(file)
		oddsportal = Oddsportal(temp_df)
		temp_df = oddsportal.pp()
		df = pd.concat([df, temp_df]).reset_index(drop=True)

	df.to_csv('LOL\\datasets\\DerivedData\\DB_table\\odds_by_match_info\\oddsportal.csv', index=False)


if __name__ == "__main__":
	main()