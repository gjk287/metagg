import pandas as pd
from bs4 import BeautifulSoup
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawler import Crawler


class Oddsportal(Crawler):
	def __init__(self, url, country, page_num, league, year, wait_on_page_load=10):
		super().__init__(url, wait_on_page_load)
		self.country = country
		self.page_num = page_num
		self.df = None
		self.league = league
		self.year = year

	def crawl_data(self):
		df = pd.DataFrame()
		for i in range(self.page_num):
			# click page 2~last
			if i+1 > 1:
				self.driver.find_element_by_xpath("//div[@id='pagination']/a[@href='#/page/{}/']".format(str(i+1))).click()
			else:
				pass
			self.driver.implicitly_wait(3)
			time.sleep(3)
			html = self.driver.page_source
			soup = BeautifulSoup(html, 'html.parser')
			tournament_table = soup.find('table', attrs={'id':'tournamentTable'})
			trs = tournament_table.tbody.find_all('tr')
			trs_tuple_list = []
			for i in range(len(trs)):
				trs_tuple_list.append((trs[i], i))

			games_list = []
			game_days_list = []
			for tup in trs_tuple_list:
				if 'deactivate' in tup[0].attrs['class']:
					game_time = tup[0].td.text
					team_A = tup[0].find('td', class_='name table-participant').text.split(' - ')[0]
					team_B = tup[0].find('td', class_='name table-participant').text.split(' - ')[1]
					set_score_A = None
					set_score_B = None
					odds_A = tup[0].find_all('td')[3].text
					odds_B = tup[0].find_all('td')[4].text
					game_list = [game_time, team_A, team_B, set_score_A, set_score_B, odds_A, odds_B, tup[1]]
					games_list.append(game_list)
				elif 'nob-border' in tup[0].attrs['class']:
					game_day = tup[0].th.span.text
					game_type = tup[0].th.text[14:]
					game_day_list = [game_day, game_type, tup[1]]
					game_days_list.append(game_day_list)
				else:
					pass

			final_list = []
			for i in games_list:
				its_game_day = []
				for j in game_days_list:
					if i[7] > j[2]:
						its_game_day.append(j)
					else:
						pass
				final_list.append(i + its_game_day[-1])

			df_each = pd.DataFrame()
			for i in range(len(final_list)):
				df_each.loc[i, 'date'] = final_list[i][8]
				df_each.loc[i, 'league_name'] = self.league
				df_each.loc[i, 'year'] = self.year
				df_each.loc[i, 'match_type'] = final_list[i][9]
				df_each.loc[i, 'team_1'] = final_list[i][1]
				df_each.loc[i, 'team_2'] = final_list[i][2]
				df_each.loc[i, 'win_odds_home'] = final_list[i][5]
				df_each.loc[i, 'win_odds_away'] = final_list[i][6]
				
			df = pd.concat([df,df_each]).reset_index(drop=True)
		
		self.df = df
		return

	def save_df(self, PATH=None):
		if PATH:
			PATH = PATH
		else:
			PATH = 'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\RawData\\Oddsportal'
		self.df.to_csv(f'{PATH}\\{self.league}-{self.year}.csv', index=False)