import pandas as pd
import time
from datetime import date, datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler import Crawler
from utils import GameDictionary


class Unikrn(Crawler):
	def __init__(self, url, wait_on_page_load=10):
		super().__init__(url, wait_on_page_load)
		self.href_df = None
		self.game_info_df = None
		self.special_odds_df = None

	def close_cookie_popup(self):
		try:
			# first type of cookie popup
			self.driver.find_element_by_css_selector('#cookie-notice > div.style__Content-sc-1ie7ov0-2.hpTBWh > div > button').click()
			time.sleep(self.wait_on_page_load)
		except:
			# second type of cookie popup
			self.driver.find_element_by_css_selector('#qc-cmp2-ui > div.qc-cmp2-footer.qc-cmp2-footer-overlay.qc-cmp2-footer-scrolled > div > button.sc-bwzfXH.jlyVur').click()
			time.sleep(self.wait_on_page_load)
		return

	def click_all_exotics(self):
		self.driver.find_element_by_css_selector('#body > div.page.column-page.undefined > main > div:nth-child(2) > div > div.style__TabsList-sc-15ei6sq-7.brKuTE.tabs-list > div > div > div:nth-child(2)').click()
		return 

	def open_exotics(self):
		container = self.driver.find_element_by_class_name('style__ExoticsContainer-dbdcsb-0.kEiufg').find_elements_by_class_name('style__Section-dbdcsb-14.kKTfGE')
		for category in container[1:]:
			category.find_element_by_class_name('style__SectionHeader-dbdcsb-16.Derth').click()
		return

	def get_href_for_each_game(self):
		# get all dates from this page
		now = datetime.now()
		date_list = []
		# Next To Go = today's date
		if self.driver.find_element_by_css_selector('#body > div.page.column-page.undefined > div > main').find_element_by_class_name('event-group--header').text == 'Next To Go':
			date_list.append(date.today().strftime('%Y-%m-%d'))
		# get rest of the date
		date_each_group = self.driver.find_element_by_css_selector('#body > div.page.column-page.undefined > div > main').find_elements_by_class_name('event-group-date-separator')
		for each_group in date_each_group:
			date_list.append(datetime.strptime(each_group.text.split('\n')[-1], '%B %d, %Y').strftime('%Y-%m-%d'))

		# get matches in each date
		group_of_events = self.driver.find_element_by_css_selector('#body > div.page.column-page.undefined > div > main').find_elements_by_class_name('event-group')

		"""
		event_betting 	= 	save href of each match. event_betting_TF=> T for exists, F for not exists
		temp_df 		= 	save odds_by_match_info. 
							date, league_name, year, season, team_1, team_2, corresponding_team, betting_site, bet_type, bet_name, saved_time, odds
		"""
		event_betting = pd.DataFrame()
		temp_df = pd.DataFrame()
		count = 0
		#count_temp_df = 0
		for game_date, j in zip(date_list, group_of_events):
			inside_group_event = j.find_elements_by_class_name('event')
			# each game in each date
			for event in inside_group_event:
				# get value for temp_df
				league_name = event.find_element_by_class_name('event-tournament').text
				year = now.year
				season = 'summer'
				team_list = event.find_elements_by_class_name('team')
				team1 = team_list[0].text
				team2 = team_list[-1].text
				betting_site = 'unikrn'
				bet_type = 'special'
				bet_name = 'game_win'
				if now.hour >= 12:
					saved_time = f"{now.strftime('%Y-%m-%d')} 23:00:00"
				else:
					saved_time = f"{now.strftime('%Y-%m-%d')} 11:00:00"
				odd_list = event.find_elements_by_class_name('odds-wrapper')
				odd1 = odd_list[0].text
				odd2 = odd_list[-1].text
				# insert data in temp_df
				temp_df.loc[count, 'date'] =  game_date
				temp_df.loc[count, 'league_name'] = league_name 
				temp_df.loc[count, 'year'] = year
				temp_df.loc[count, 'season'] = season
				temp_df.loc[count, 'team_1'] = team1
				temp_df.loc[count, 'team_2'] = team2
				temp_df.loc[count, 'betting_site'] = betting_site
				temp_df.loc[count, f'{bet_type}:{bet_name}:home'] = odd1
				temp_df.loc[count, f'{bet_type}:{bet_name}:away'] = odd2
				temp_df.loc[count, 'saved_time'] = saved_time
				

				# get value for event_betting
				event_betting_tf = 'F'
				event_url_href = None
				try:
					# if there is any exotic odds url change to T and get href
					if event.find_element_by_class_name('event-buttons').find_element_by_css_selector('span').text:
						event_betting_tf = 'T'
						event_url_href = event.find_element_by_class_name('event-buttons').find_element_by_css_selector('a').get_attribute('href')
				except:
					event_betting_tf = 'F'
				# insert data in event_betting
				event_betting.loc[count, 'date'] = game_date
				event_betting.loc[count, 'league_name'] = league_name
				event_betting.loc[count, 'year'] = year
				event_betting.loc[count, 'season'] = season
				event_betting.loc[count, 'team_1'] = team1
				event_betting.loc[count, 'team_2'] = team2
				event_betting.loc[count, 'betting_site'] = betting_site
				event_betting.loc[count, 'saved_time'] = saved_time
				event_betting.loc[count, 'event_betting_TF'] = event_betting_tf
				event_betting.loc[count, 'event_url_href'] = event_url_href
				count += 1
		
		g_dict = GameDictionary()
		event_betting = event_betting.replace(g_dict.get_dict())
		event_betting = event_betting.where(pd.notnull(event_betting), None)

		temp_df = temp_df.replace(g_dict.get_dict())

		self.href_df = event_betting
		self.game_info_df = temp_df

	def crawl_data(self):
		"""
		special_betting_df 	=	save special bets (over_under, handicap...etc)
								date, league_name, year, season, team_1, team_2, set_number, betting_site, 
								bet_name, 
		"""
		special_betting_df = pd.DataFrame()
		count = 0
		temp_df = self.game_info_df
		# iterate through href dataframe
		for idx, val in self.href_df.iterrows():
			bet12_class_name = 'style__Selections-dbdcsb-13.bhqKtR'
			# if url exists
			if val['event_url_href']:
				self.driver.get(val['event_url_href'])
				time.sleep(20)
				# click "all exotics"
				try:
					self.click_all_exotics()
					time.sleep(20)
				except:
					continue
				# make pre-dataframe for 3 sets
				for num in range(3):
					special_betting_df.loc[count+num, 'date'] = val['date']
					special_betting_df.loc[count+num, 'league_name'] = val['league_name']
					special_betting_df.loc[count+num, 'year'] = val['year']
					special_betting_df.loc[count+num, 'season'] = val['season']
					special_betting_df.loc[count+num, 'team_1'] = val['team_1']
					special_betting_df.loc[count+num, 'team_2'] = val['team_2']
					special_betting_df.loc[count+num, 'betting_site'] = val['betting_site']
					special_betting_df.loc[count+num, 'saved_time'] = val['saved_time']

				# open each container of exotic bets
				try:
					self.open_exotics()
					time.sleep(20)
				except:
					continue
				# container contains category of bets (over_under, special..etc)
				container = self.driver.find_element_by_class_name('style__ExoticsContainer-dbdcsb-0.kEiufg').find_elements_by_class_name('style__Section-dbdcsb-14.kKTfGE')
				for category in container:
					# all_bet contains each bet in that category
					all_bet = category.find_elements_by_class_name('style__MarketRow-dbdcsb-8.fXImmK')
					for each_bet in all_bet:
						# continue if the bet is closed
						try:
							bet_name = each_bet.find_element_by_class_name('style__MarketName-dbdcsb-10.furSgz').text.split('\n')[-1]
						except:
							continue
						map_list = ['Map 1', 'Map 2', 'Map 3']
						map_set = {'Map 1': 1, 'Map 2': 2, 'Map 3': 3}
						# If any of Map 1,2,3 in bet_name
						if any(x in bet_name for x in map_list):
							for Map in map_list:
								if Map in bet_name:
									# get set number by Map 1,2,3 in bet_name
									set_number = map_set[Map]
									# get rid of Map 1,2,3 in bet_name
									new_bet_name = bet_name.split(Map+' ')[-1]
									# get bet_type and odds for set_match related bets
									if ('Over/Under' in new_bet_name) | ('over/under' in new_bet_name):
										bet_type = 'over_under'
										bet_12 = each_bet.find_element_by_class_name(bet12_class_name).text.split('\n')
										if len(bet_12) == 4:
											# get odds for over, under. If odds are not float then go to next bet
											try:
												odd_1 = float(bet_12[1])
												odd_2 = float(bet_12[-1])
											except:
												continue
											special_betting_df.loc[count+map_set[Map]-1, 'set_number'] = set_number
											special_betting_df.loc[count+map_set[Map]-1, f'{bet_type}:{" ".join(new_bet_name.split(" ")[:-2])}:{new_bet_name.split(" ")[-1]}:over'] = odd_1
											special_betting_df.loc[count+map_set[Map]-1, f'{bet_type}:{" ".join(new_bet_name.split(" ")[:-2])}:{new_bet_name.split(" ")[-1]}:under'] = odd_2
										else:
											print(f'Something wrong in over_under bet\n{bet_12}')
											pass
									# there is no bet with Handicap for set_match_info table in unikrn
									elif ('Handicap' in new_bet_name):
										pass

									elif ('Both' in new_bet_name):
										bet_type = 'both'
										bet_12 = each_bet.find_element_by_class_name(bet12_class_name).text.split('\n')
										if len(bet_12) == 4:
											# get odds for over, under. If odds are not float then go to next bet
											try:
												odd_1 = float(bet_12[1])
												odd_2 = float(bet_12[-1])
											except:
												continue
											special_betting_df.loc[count+map_set[Map]-1, 'set_number'] = set_number
											special_betting_df.loc[count+map_set[Map]-1, f'{bet_type}:{" ".join(new_bet_name.split(" ")[1:])}:yes'] = odd_1
											special_betting_df.loc[count+map_set[Map]-1, f'{bet_type}:{" ".join(new_bet_name.split(" ")[1:])}:no'] = odd_2
									else:
										bet_type = 'special'
										bet_12 = each_bet.find_element_by_class_name(bet12_class_name).text.split('\n')
										if len(bet_12) == 4:
											# get odds for over, under. If odds are not float then go to next bet
											try:
												odd_1 = float(bet_12[1])
												odd_2 = float(bet_12[-1])
											except:
												continue
											special_betting_df.loc[count+map_set[Map]-1, 'set_number'] = set_number
											special_betting_df.loc[count+map_set[Map]-1, f'{bet_type}:{new_bet_name}:home'] = odd_1
											special_betting_df.loc[count+map_set[Map]-1, f'{bet_type}:{new_bet_name}:away'] = odd_2
						else:
							# every bet except correct score
							try:
								if 'Handicap' in bet_name:
									bet_type = 'handicap'
									bet_12 = each_bet.find_element_by_class_name(bet12_class_name).text.split('\n')
									if len(bet_12) == 4:
										# get odds for over, under. If odds are not float then go to next bet
										try:
											odd_1 = float(bet_12[1])
											odd_2 = float(bet_12[-1])
										except:
											continue
										temp_df.loc[idx, f'{bet_type}:set_handicap:{bet_12[0].split(" ")[-1]}:home'] = odd_1
										temp_df.loc[idx, f'{bet_type}:set_handicap:{bet_12[2].split(" ")[-1]}:away'] = odd_2
								elif 'Over/Under' in bet_name:
									bet_type = 'over_under'
									bet_12 = each_bet.find_element_by_class_name(bet12_class_name).text.split('\n')
									if len(bet_12) == 4:
										# get odds for over, under. If odds are not float then go to next bet
										try:
											odd_1 = float(bet_12[1])
											odd_2 = float(bet_12[-1])
										except:
											continue
										temp_df.loc[idx, f'{bet_type}:{" ".join(bet_name.split(" ")[:-2])}:{bet_name.split(" ")[-1]}:over'] = odd_1
										temp_df.loc[idx, f'{bet_type}:{" ".join(bet_name.split(" ")[:-2])}:{bet_name.split(" ")[-1]}:under'] = odd_2
								else:
									bet_type = 'special'
									bet_12 = each_bet.find_element_by_class_name(bet12_class_name).text.split('\n')
									if len(bet_12) == 4:
										# get odds for over, under. If odds are not float then go to next bet
										try:
											odd_1 = float(bet_12[1])
											odd_2 = float(bet_12[-1])
										except:
											continue
										temp_df.loc[idx, f'{bet_type}:{bet_name}:home'] = odd_1
										temp_df.loc[idx, f'{bet_type}:{bet_name}:away'] = odd_2
							# correct score
							except:
								try:
									bet_type = 'special'
									bet_12 = each_bet.find_element_by_class_name('style__Selections-dbdcsb-13.eVkDnl').text.split('\n')
									# best of 3
									if len(bet_12) == 8:
										team_2_0 = float(bet_12[1])
										team_2_1 = float(bet_12[3])
										team_0_2 = float(bet_12[5])
										team_1_2 = float(bet_12[-1])
										temp_df.loc[idx, f'{bet_type}:2-0'] = f'{bet_12[0]}:{team_2_0}'
										temp_df.loc[idx, f'{bet_type}:2-1'] = f'{bet_12[2]}:{team_2_1}'
										temp_df.loc[idx, f'{bet_type}:0-2'] = f'{bet_12[4]}:{team_0_2}'
										temp_df.loc[idx, f'{bet_type}:1-2'] = f'{bet_12[6]}:{team_1_2}'

									# best of 5
									else:
										team_3_0 = float(bet_12[1])
										team_3_1 = float(bet_12[3])
										team_3_2 = float(bet_12[5])
										team_0_3 = float(bet_12[7])
										team_1_3 = float(bet_12[9])
										team_2_3 = float(bet_12[11])
										temp_df.loc[idx, f'{bet_type}:3-0'] = f'{bet_12[0]}:{team_3_0}'
										temp_df.loc[idx, f'{bet_type}:3-1'] = f'{bet_12[2]}:{team_3_1}'
										temp_df.loc[idx, f'{bet_type}:3-2'] = f'{bet_12[4]}:{team_3_2}'
										temp_df.loc[idx, f'{bet_type}:0-3'] = f'{bet_12[6]}:{team_0_3}'
										temp_df.loc[idx, f'{bet_type}:1-3'] = f'{bet_12[8]}:{team_1_3}'
										temp_df.loc[idx, f'{bet_type}:2-3'] = f'{bet_12[10]}:{team_2_3}'
								except:
									continue
				count += 3
		self.game_info_df = temp_df
		self.special_odds_df = special_betting_df
		return

	def save_df(self):
		g_dict = GameDictionary()
		self.game_info_df = self.game_info_df.replace(g_dict.get_dict())
		self.special_odds_df = self.special_odds_df.replace(g_dict.get_dict())

		PATH = 'C:\\Users\\jjames\\Dropbox\\Cloud_Data\\Projects\\Game-Data-Platform\\meta.gg\\LOL\\datasets\\RawData\\Unikrn'
		TIME = date.today().strftime('%Y-%m-%d')
		if int(datetime.now().strftime('%Y-%m-%d_%H').split('_')[-1]) >= 12:
			self.game_info_df.to_csv(f'{PATH}\\game_info_{TIME}_PM.csv', index=False, encoding='utf-8')
			self.special_odds_df.to_csv(f'{PATH}\\special_{TIME}_PM.csv', index=False, encoding='utf-8')
		else:
			self.game_info_df.to_csv(f'{PATH}\\game_info_{TIME}_AM.csv', index=False, encoding='utf-8')
			self.special_odds_df.to_csv(f'{PATH}\\special_{TIME}_AM.csv', index=False, encoding='utf-8')