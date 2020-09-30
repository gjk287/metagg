import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from crawler import MatchHistory
from utils import GamepediaDict


def main():
	
	file = r'C:\Users\jjames\Dropbox\Cloud_Data\Projects\Game-Data-Platform\meta.gg\LOL\datasets\RawData\Gamepedia\match_history_url\LDL-2019-summer.csv'
	df_mh = pd.read_csv(file)
	df_mh = df_mh.where(pd.notnull(df_mh), None)

	league = file.split('\\')[-1].split('-')[0]
    year = file.split('\\')[-1].split('-')[1]
    season = file.split('\\')[-1].split('-')[2].split('.csv')[0]
    gp_dict = GamepediaDict()
	gp_dict.from_year_season_league(year, season, league)

	df_mh[['team_1', 'team_2']] = df_mh[['team_1', 'team_2']].replace(gp_dict.get_dict('team'))
    df_mh[['team_1', 'team_2']] = df_mh[['team_1', 'team_2']].fillna(method='ffill')

	# set league to crawl
	df_mh = set_league(df_mh)

	# instantiate
	matchhistory = MatchHistory(df_mh)
	matchhistory.get_driver()
	#matchhistory.crawl_data("pooh10051", "sf05241328!", missing=True)
	matchhistory.crawl_china()
	matchhistory.close_browser()
	# matchhistory.save_df('Missing', 'Data', 'v1')


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