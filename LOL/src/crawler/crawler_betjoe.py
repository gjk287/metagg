import pandas as pd
import time
from datetime import date, datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crawler import Crawler
from utils import GameDictionary, date_to_datetime_to_string


class Betjoe(Crawler):
	def __init__(self, url, wait_on_page_load=15):
		super().__init__(url, wait_on_page_load)
		self.href_df = None
		self.game_info_df = None
		self.special_odds_df = None

	def go_to_LOL(self):
		game_list = self.driver.find_elements_by_class_name('CZBvE')
		for game in game_list:
			if game.find_element_by_css_selector('span').text == 'League of Legends':
				lol_game = game
		lol_game.find_element_by_css_selector('span').click()
		time.sleep(self.wait_on_page_load)
		return

	def show_all_league(self):
		all_group = self.driver.find_elements_by_class_name('_2v2WR')
		for group in all_group[1:]:
			group.find_element_by_class_name('_2K09p').click()
			time.sleep(3)
		time.sleep(30)

	def get_href_for_each_game(self):
		now = datetime.now()
		# all_group contains each league's games
		all_group = self.driver.find_elements_by_class_name('_2v2WR')
		"""
		href_df 	=	save href of each match. 
						date, league_name, year, season, team_1, team_2, betting_site, saved_time, href_url
		"""
		href_df = pd.DataFrame()
		count = 0
		# iterate each league
		for group in all_group:
			league_name = group.find_element_by_class_name('_2K09p').text
			# iterate each game in each league
			all_game = group.find_elements_by_class_name('_1NtMe')
			for game in all_game:
				# get value for href_df
				# game_date = game.find_element_by_css_selector('a').text.split('\n')[0]
				# team_1 = game.find_element_by_css_selector('a').text.split('\n')[-2]
				# team_2 = game.find_element_by_css_selector('a').text.split('\n')[-1]
				game_date = game.find_element_by_class_name('_3tR88').text
				team_1 = game.find_element_by_class_name('OY9uM._3YXvb').text.split('\n')[0]
				team_2 = game.find_element_by_class_name('OY9uM._3YXvb').text.split('\n')[-1]
				href_url = game.find_element_by_css_selector('a').get_attribute('href')
				year = now.year
				season = 'summer'
				betting_site = 'betjoe'
				if now.hour >= 12:
					saved_time = f"{now.strftime('%Y-%m-%d')} 23:00:00"
				else:
					saved_time = f"{now.strftime('%Y-%m-%d')} 11:00:00"
				# insert data in href_df
				href_df.loc[count, 'date'] = game_date
				href_df.loc[count, 'league_name'] = league_name
				href_df.loc[count, 'year'] = year
				href_df.loc[count, 'season'] = season
				href_df.loc[count, 'team_1'] = team_1
				href_df.loc[count, 'team_2'] = team_2
				href_df.loc[count, 'betting_site'] = betting_site
				href_df.loc[count, 'saved_time'] = saved_time
				href_df.loc[count, 'href_url'] = href_url
				count += 1
		self.href_df = href_df
		return

	def crawl_data(self):
		"""
		special_betting_df 	=	save special bets (over_under, handicap...etc)
		game_info_df		=	save odds_by_match_info
		"""
		special_odds_df = pd.DataFrame()
		game_info_df = pd.DataFrame()
		
		count = 0
		count_info = 0
		for _, val in self.href_df.iterrows():
			self.driver.get(val['href_url'])
			time.sleep(self.wait_on_page_load)
			# make pre-dataframe for game_info_df
			game_info_df.loc[count_info, 'date'] = val['date']
			game_info_df.loc[count_info, 'league_name'] = val['league_name']
			game_info_df.loc[count_info, 'year'] = val['year']
			game_info_df.loc[count_info, 'season'] = val['season']
			game_info_df.loc[count_info, 'team_1'] = val['team_1']
			game_info_df.loc[count_info, 'team_2'] = val['team_2']
			game_info_df.loc[count_info, 'betting_site'] = val['betting_site']
			game_info_df.loc[count_info, 'saved_time'] = val['saved_time']
			# make pre-dataframe for 3 sets
			for num in range(3):
				special_odds_df.loc[count+num, 'date'] = val['date']
				special_odds_df.loc[count+num, 'league_name'] = val['league_name']
				special_odds_df.loc[count+num, 'year'] = val['year']
				special_odds_df.loc[count+num, 'season'] = val['season']
				special_odds_df.loc[count+num, 'team_1'] = val['team_1']
				special_odds_df.loc[count+num, 'team_2'] = val['team_2']
				special_odds_df.loc[count+num, 'set_number'] = num+1
				special_odds_df.loc[count+num, 'betting_site'] = val['betting_site']
				special_odds_df.loc[count+num, 'saved_time'] = val['saved_time']
			# get names of all betting categories
			category_name_list = []
			odds_categories = self.driver.find_elements_by_class_name('_3Zukk')
			for category in odds_categories:
				category_name_list.append(category.text)
			# get all odds in each categories (same length with category number)
			game_list_group = self.driver.find_elements_by_class_name('_2rn1X')
			# enumerate each odds categories
			for idx_category, game_list in enumerate(game_list_group):
				group_of_odds = game_list.find_elements_by_css_selector('button')
				# odds가 map 1,2,3중에 어떤건지 고르기
				if ('맵1' in category_name_list[idx_category]) or ('MAP 1' in category_name_list[idx_category]) or ('맵 1' in category_name_list[idx_category]):
					df_idx = count
				elif ('맵2' in category_name_list[idx_category]) or ('MAP 2' in category_name_list[idx_category]) or ('맵 2' in category_name_list[idx_category]):
					df_idx = count + 1
				elif ('맵3' in category_name_list[idx_category]) or ('MAP 2' in category_name_list[idx_category]) or ('맵 3' in category_name_list[idx_category]):
					df_idx = count + 2
				# odds가 세트 경기에 포함되지 않는것
				else:
					if ("경기 우승자" in category_name_list[idx_category]) | ("MATCH WINNER" in category_name_list[idx_category]):
						bet_type = 'special'
						for i, each_game_odds in enumerate(group_of_odds):
							if i % 2 == 0:
								homeaway = 'home'
							else:
								homeaway = 'away'
							game_odds = each_game_odds.text.split('\n')[-1]
							if '끄기' in game_odds:
								game_odds = None
							else:
								pass
							game_info_df.loc[count_info, f'{bet_type}:game_win:{homeaway}'] = game_odds

					elif ("매치 핸디캡" in category_name_list[idx_category]) | ("MAP ADVANTAGE" in category_name_list[idx_category]):
						bet_type = 'handicap'
						for i, each_game_odds in enumerate(group_of_odds):
							if i % 2 == 0:
								homeaway = 'home'
								handicap_amt = each_game_odds.text.split('\n')[0].split(' ')[-1]
							else:
								homeaway = 'away'
								handicap_amt = each_game_odds.text.split('\n')[0].split(' ')[-1]
							game_odds = each_game_odds.text.split('\n')[-1]
							if '끄기' in game_odds:
								game_odds = None
							else:
								pass
							game_info_df.loc[count_info, f'{bet_type}:set_handicap:{handicap_amt}:{homeaway}'] = game_odds

					elif ("정확한 스코어 맞추기" in category_name_list[idx_category]) | ("CORRECT SCORE" in category_name_list[idx_category]):
						bet_type = 'special'
						for i, each_game_odds in enumerate(group_of_odds):
							game_odds = each_game_odds.text.split('\n')[-1]
							if '끄기' in game_odds:
								game_odds = None
							else:
								pass
							column_name = each_game_odds.text.split("\n")[0]
							game_info_df.loc[count_info, f'{column_name}'] = game_odds

					elif ("전체 득점 플레이" in category_name_list[idx_category]) | ("TOTAL MAPS PLAYED" in category_name_list[idx_category]):
						bet_type = 'over_under'
						for i, each_game_odds in enumerate(group_of_odds):
							if i % 2 == 0:
								ou = 'over'
								ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
							else:
								ou = 'under'
								ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
							game_odds = each_game_odds.text.split('\n')[-1]
							if '끄기' in game_odds:
								game_odds = None
							else:
								pass
							game_info_df.loc[count_info, f'{bet_type}:total_sets:{ou_threshold}:{ou}'] = game_odds

				if ("승패" in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:set_win:{homeaway}'] = game_odds

				elif ('먼저 5점 득점' in category_name_list[idx_category]) | ('FIRST TO 5 KILLS' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_5kill:{homeaway}'] = game_odds

				elif ('처음부터 10킬까지' in category_name_list[idx_category]) | ('FIRST TO 10 KILLS' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_10kill:{homeaway}'] = game_odds

				elif ('첫킬' in category_name_list[idx_category]) | ('FIRST BLOOD' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_blood:{homeaway}'] = game_odds

				elif ('전체 득점 (' in category_name_list[idx_category]) | ('전체 득점(' in category_name_list[idx_category]):
					bet_type = 'over_under'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							ou = 'over'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
						else:
							ou = 'under'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:total_kill:{ou_threshold}:{ou}'] = game_odds

				elif ('전체 시간' in category_name_list[idx_category]) | ('TOTAL TIME' in category_name_list[idx_category]):
					bet_type = 'over_under'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							ou = 'over'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1].split(':')[0]
						else:
							ou = 'under'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1].split(':')[0]
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:game_time:{ou_threshold}:{ou}'] = game_odds

				elif ('킬수 핸디캡' in category_name_list[idx_category]) | ('KILLS ADVANTAGE' in category_name_list[idx_category]):
					bet_type = 'handicap'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
							handicap_amt = each_game_odds.text.split('\n')[0].split(' ')[-1]
						else:
							homeaway = 'away'
							handicap_amt = each_game_odds.text.split('\n')[0].split(' ')[-1]
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:total_kill_handicap:{handicap_amt}:{homeaway}'] = game_odds

				elif ('첫번째 타워 부시기' in category_name_list[idx_category]) | ('DESTROY FIRST TOWER' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_tower:{homeaway}'] = game_odds

				elif ('KILL FIRST DRAGON' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_dragon:{homeaway}'] = game_odds

				elif ('TOTAL DRAGONS SLAIN' in category_name_list[idx_category]):
					bet_type = 'over_under'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							ou = 'over'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
						else:
							ou = 'under'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:total_dragon:{ou_threshold}:{ou}'] = game_odds

				elif ('KILL FIRST BARON' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_baron:{homeaway}'] = game_odds

				elif ('TOTAL BARONS SLAIN' in category_name_list[idx_category]):
					bet_type = 'over_under'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							ou = 'over'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
						else:
							ou = 'under'
							ou_threshold = each_game_odds.text.split('\n')[0].split(' ')[-1]
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:total_baron:{ou_threshold}:{ou}'] = game_odds

				elif ('KILL FIRST RIFT HERALD' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_rift:{homeaway}'] = game_odds

				elif ('DESTROY FIRST INHIBITOR' in category_name_list[idx_category]):
					bet_type = 'special'
					for i, each_game_odds in enumerate(group_of_odds):
						if i % 2 == 0:
							homeaway = 'home'
						else:
							homeaway = 'away'
						game_odds = each_game_odds.text.split('\n')[-1]
						if '끄기' in game_odds:
							game_odds = None
						else:
							pass
						special_odds_df.loc[df_idx, f'{bet_type}:first_inhib:{homeaway}'] = game_odds

				else:
					pass
			count += 3
			count_info += 1
		self.game_info_df = game_info_df
		self.special_odds_df = special_odds_df
		return 
	
	def save_df(self):
		g_dict = GameDictionary()
		self.game_info_df = self.game_info_df.replace(g_dict.get_dict())
		self.special_odds_df = self.special_odds_df.replace(g_dict.get_dict())

		self.game_info_df['date'] = self.game_info_df['date'].apply(lambda x: '2020 ' + x)
		self.special_odds_df['date'] = self.special_odds_df['date'].apply(lambda x: '2020 ' + x)
		
		self.game_info_df['date'] = self.game_info_df['date'].apply(date_to_datetime_to_string)		
		self.special_odds_df['date'] = self.special_odds_df['date'].apply(date_to_datetime_to_string)

		self.game_info_df['date'] = self.game_info_df['date'].fillna(method='ffill')
		self.special_odds_df['date'] = self.special_odds_df['date'].fillna(method='ffill')

		PATH = 'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\RawData\\Betjoe'
		TIME = date.today().strftime('%Y-%m-%d')
		if int(datetime.now().strftime('%Y-%m-%d_%H').split('_')[-1]) >= 12:
			self.game_info_df.to_csv(f'{PATH}\\game_info_{TIME}_PM.csv', index=False, encoding='utf-8')
			self.special_odds_df.to_csv(f'{PATH}\\special_{TIME}_PM.csv', index=False, encoding='utf-8')
		else:
			self.game_info_df.to_csv(f'{PATH}\\game_info_{TIME}_AM.csv', index=False, encoding='utf-8')
			self.special_odds_df.to_csv(f'{PATH}\\special_{TIME}_AM.csv', index=False, encoding='utf-8')
