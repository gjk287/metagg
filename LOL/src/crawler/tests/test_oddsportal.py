import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from crawler import Oddsportal
from utils import UrlOddsportal


def main():
	# instantiate url oddsportal
	url_odp = UrlOddsportal()

	# set league 
	url_odp.set_league()

	# set start and end year
	url_odp.set_startToEndYear(2017, 2020)

	# get url dict
	url_dict = url_odp.generate_url()

	# crawl
	crawl_and_save(url_dict)


	
def crawl_and_save(url_dict):
	url_list = list(url_dict.keys())
	for url in url_list:
		# instantiate oddsportal crawler
		oddsportal = Oddsportal(url, url_dict[url]['Country'], url_dict[url]['page_num'], url_dict[url]['League'], url_dict[url]['Year'])
		
		# get selenium driver and go to link
		oddsportal.get_driver()
		oddsportal.go_to_link()

		# crawl the data
		oddsportal.crawl_data()

		# save
		oddsportal.save_df()

		# close driver
		oddsportal.close_browser()

if __name__ == "__main__":
	main()