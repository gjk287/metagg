import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler_betjoe import Betjoe

def main():
	result = None
	while result is None:
		try:
			result = crawl_and_save()
		except:
			pass

def crawl_and_save():
	url = 'https://sports.betjoe.com/sport/esports'
	
	# instantiate
	betjoe = Betjoe(url)

	# get selenium driver and go to the link
	betjoe.get_driver()
	betjoe.go_to_link()

	# get into League of Legends section
	try:
		betjoe.go_to_LOL()
	except:
		betjoe.go_to_LOL()

	# show all games in each league
	betjoe.show_all_league()

	# get href for each game
	betjoe.get_href_for_each_game()

	# crawl data in href
	betjoe.crawl_data()

	# save
	betjoe.save_df()
	
	# close driver
	betjoe.close_browser()

	return 'success'


if __name__ == "__main__":
	main()