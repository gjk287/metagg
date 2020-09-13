import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from crawler import Unikrn


def main():
	url = 'https://unikrn.com/bet/games/league-of-legends'
	# instantiate
	unikrn = Unikrn(url)

	result = None
	while result is None:
		try:
			result = crawl_and_save(unikrn)
		except:
			count += 1
		
		if count == 7:
			result = 'Failed'

def crawl_and_save(unikrn):
	# get selenium driver and go to the link
	unikrn.get_driver()
	unikrn.go_to_link()

	# close cookie popup
	try:
		unikrn.close_cookie_popup()
	except:
		pass

	# scroll down all the way
	unikrn.scroll_down()

	# get href for each game
	unikrn.get_href_for_each_game()

	# crawl data in href
	unikrn.crawl_data()

	# save
	unikrn.save_df()

	# close driver
	unikrn.close_browser()

	return 'success'

if __name__ == "__main__":
	main()