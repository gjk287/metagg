import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from crawler import Gamepedia
from utils import UrlGamepedia

# instantiate
gp_url = UrlGamepedia()


def main():
	# set league = default is all
	gp_url.set_league()
	
	# set start and end year
	gp_url.set_startToEndYear(2017, 2020)

	# generate url
	url_list = gp_url.generate_url()
	
	crawl_and_save(url_list)

def crawl_and_save(url_list):
	for url in url_list:
		league = gp_url.get_leagueFromUrl(url)
		year = gp_url.get_yearFromUrl(url)
		season = gp_url.get_seasonFromUrl(url)
		print(league, year, season)

		# instantiate crawler
		gamepedia = Gamepedia(league, year, season, url)

		# crawl with bs4
		gamepedia.crawl_data(mh=True, module='bs4')
		gamepedia.crawl_data(mh=False, module='bs4')

		# save
		mh_PATH = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\League_of_Legends\\datasets\\RawData\\Gamepedia\\match_history_url\\{league}-{year}-{season}.csv'
		schedule_PATH = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\League_of_Legends\\datasets\\RawData\\Gamepedia\\game_schedule\\{league}-{year}-{season}.csv'
		
		gamepedia.save_df(mh_PATH, 'mh')
		gamepedia.save_df(schedule_PATH, 'gs')


if __name__ == "__main__":
	main()