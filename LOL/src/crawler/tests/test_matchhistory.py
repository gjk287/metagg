import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from crawler import MatchHistory


def main():
	df_mh = pd.read_csv(r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta.gg\LOL\datasets\DerivedData\DB_table\set_match_url\match_history_url.csv')
	df_mh = df_mh.where(pd.notnull(df_mh), None)

	# set league to crawl
	df_mh = set_league(df_mh)

	# instantiate
	matchhistory = MatchHistory(df_mh)
	matchhistory.crawl_data("pooh10051", "sf05241328!")


def set_league(df_mh, league_list=None, include=True):
	if not league_list:
		return df_mh
	else:
		if include:
			df_mh = df_mh[df_mh['league_name'].isin(league_list)].reset_index(drop=True)
		else:
			df_mh = df_mh[~df_mh['league_name'].isin(league_list)].reset_index(drop=True)
		return df_mh



if __name__ == "__main__":
	main()