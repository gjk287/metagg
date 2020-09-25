import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler_betjoe import Betjoe

def main():
	url = 'https://sports.betjoe.com/sport/esports'
	
	# instantiate
	betjoe = Betjoe(url)
	betjoe.get_driver()

	result = None
	count = 0
	while result is None:
		try:
			result = crawl_and_save(betjoe)
		except:
			count += 1
		
		if count == 7:
			result = crawl_and_save(betjoe)

def crawl_and_save(betjoe):
	# get selenium driver and go to the link
	
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