import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import date, datetime
import requests
import re
from crawler import Crawler


class Gamepedia(Crawler):
	def __init__(self, league, year, season, url, wait_on_page_load=5):
		super().__init__(url, wait_on_page_load)
		self.league = league
		self.season = season
		self.year = year
		self.df = None
		self.df_mh = None

	def show_match_schedule(self):
		weekly_schedule = self.driver.find_element_by_class_name('ml-normal-pred-and-results').find_elements_by_class_name('matchlist-tab-wrapper')

		for each_week in weekly_schedule:
			if each_week.find_element_by_class_name('table-header-showhide').text == '[show]':
				each_week.find_element_by_class_name('table-header-showhide').click()
			else:
				pass

		time.sleep(self.wait_on_page_load)
		return

	def crawl_data(self, mh=False, module='bs4'):
		if module == 'bs4':
			res = requests.get(self.url)
			res.raise_for_status()
			soup = BeautifulSoup(res.text, "lxml")

			if not mh:
				weekly_schedule = soup.find("div", attrs={"id":"matchlist-content-wrapper"}).find_all("div", attrs={"class":"matchlist-tab-wrapper"})
				df_game_schedule = pd.DataFrame()
				for each_week in weekly_schedule:
					trs = each_week.find_all('tr', attrs={"class":re.compile("^ml-allw ml-w[0-9]")})
					week = each_week.find("th").text.split(']')[-1].split(' ')[-1]
					df_each_week = pd.DataFrame()
					row_num = 0
					for tr in trs:
						if len(tr.text.split(" ")) == 2:
							date = tr.text.split(" ")[-1]
						elif "ml-row" in tr.attrs["class"]:
							#row_num = int(tr.attrs["data-initial-order"])-1
							df_each_week.loc[row_num, "year"] = self.year
							df_each_week.loc[row_num, "season"] = self.season
							df_each_week.loc[row_num, "league_name"] = self.league
							df_each_week.loc[row_num, "week"] = week
							df_each_week.loc[row_num, "date"] = date
							for td in tr.find_all("td"):
								if "matchlist-team1" in td.attrs["class"]:
									df_each_week.loc[row_num, "team_1"] = td.find("span", attrs={"class":"teamname"}).get_text()
								elif "matchlist-team2" in td.attrs["class"]:
									df_each_week.loc[row_num, "team_2"] = td.find("span", attrs={"class":"teamname"}).get_text()
								else:
									pass
							result = ""
							for td in tr.find_all("td", attrs={"class":re.compile("^matchlist-score")}):
								result = result + td.get_text()
							if len(result) >= 2:
								df_each_week.loc[row_num, "result"] = result[0] + "-" + result[1]
							else:
								df_each_week.loc[row_num, "result"] = result    
						
						else:
							# print(f'Tiebreaker in Year: {self.year}, League: {self.league}, Season: {self.season}')
							week_num = 'Tiebreakers'
						row_num += 1
					df_game_schedule = pd.concat([df_game_schedule, df_each_week]).reset_index(drop=True)
					
				self.df = df_game_schedule
			else:
				try:
					vods_match_links_trs = soup.find("table", attrs={"id":"md-table"}).find_all("tr")

					column_list = []
					for th in vods_match_links_trs[2].find_all("th"):
						column_list.append(th.text)

					tr_list = []
					for tr in vods_match_links_trs:
						try:
							if ('mdv-allweeks' in tr.attrs["class"]) and ('column-label-small' not in tr.attrs["class"]):
								tr_list.append(tr)
							elif ('mdv-allweeks' in tr.attrs["class"]) and ('column-label-small' in tr.attrs["class"]):
								tr_list.append(tr.previous_sibling.get_text().split(']')[-1].split(" ")[-1])
							else:
								pass
						except KeyError:
							pass

					row_dict = {}
					row_week = []
					for tr in tr_list:
						if len(str(tr)) <= 15:
							row_week.append(tr)
					for i in range(len(row_week)):
						row_dict[row_week[i]] = []
						for j in range(len(tr_list)):
							if row_week[i] == tr_list[j]:
								try:
									while len(str(tr_list[j+1])) > 15:
										row_dict[row_week[i]].append(tr_list[j+1])
										j += 1
								except:
									pass
						
					df_match_history = pd.DataFrame()
					for key in row_dict.keys():
						vods_match_links_dict = {}
						for rowkey in range(len(row_dict[key])):
							vods_match_links_dict[rowkey] = {}
							td_list = row_dict[key][rowkey].find_all("td")
							vods_match_links_dict[rowkey]['week'] = key
							for colkey in range(len(td_list)):
								vods_match_links_dict[rowkey][column_list[colkey-len(td_list)]] = td_list[colkey-len(td_list)]
							

						df = pd.DataFrame()
						for rowkey in vods_match_links_dict.keys():
							df.loc[rowkey, 'year'] = self.year
							df.loc[rowkey, 'season'] = self.season
							df.loc[rowkey, 'league_name'] = self.league
							df.loc[rowkey, 'week'] = vods_match_links_dict[rowkey]['week']
							
							for col in vods_match_links_dict[rowkey].keys():
								try:
									if col == "Team 1":
										df.loc[rowkey, "team_1"] = vods_match_links_dict[rowkey][col].find("span", attrs={"class":"teamname"}).text
									elif col == "Team 2":
										df.loc[rowkey, "team_2"] = vods_match_links_dict[rowkey][col].find("span", attrs={"class":"teamname"}).text
									elif col == "Blue":
										df.loc[rowkey, col] = vods_match_links_dict[rowkey][col].text
									elif col == "Red":
										df.loc[rowkey, col] = vods_match_links_dict[rowkey][col].text
									elif col == "MH":
										df.loc[rowkey, col] = vods_match_links_dict[rowkey][col].a.attrs["href"]
									elif col == "VODs":
										vods_a_list = vods_match_links_dict[rowkey][col].find_all("a")
										for vod_a in vods_a_list:
											df.loc[rowkey, vod_a.text] = vod_a.attrs["href"]
									elif col == "MVP":
										df.loc[rowkey, col] = vods_match_links_dict[rowkey][col].text
									else:
										pass
								except KeyError:
									pass

								except AttributeError:
									pass
						df_match_history = pd.concat([df_match_history, df]).reset_index(drop=True)

					for i in range(df_match_history.shape[0]):
						if (type(df_match_history.loc[i, "team_1"]) != float):
							set_number = 1
						elif (type(df_match_history.loc[i, "team_1"]) == float) and (type(df_match_history.loc[i-1, "team_1"]) != float):
							set_number = 2
						elif (type(df_match_history.loc[i, "team_1"]) == float) and (type(df_match_history.loc[i-1, "team_1"]) == float) and (type(df_match_history.loc[i-2, "team_1"]) != float):
							set_number = 3
						else:
							set_number = 0
						df_match_history.loc[i, "set_number"] = set_number
					self.df_mh = df_match_history
				except:
					self.df_mh = None
		
		elif module == 'selenium':
			if not mh:
				weekly_schedule = self.driver.find_element_by_class_name('ml-normal-pred-and-results').find_elements_by_class_name('matchlist-tab-wrapper')
				df_game_schedule = pd.DataFrame()
				count = 0

				for each_week in weekly_schedule:
					for txt in each_week.find_elements_by_tag_name('tr'):
						if txt.text != '':
							text_split = txt.text.split(' ')

							if len(text_split) == 2:
								if ('Week' in text_split[0]) | ('Round' in text_split[0]):
									week_num = text_split[-1]
								else:
									game_date = text_split[-1]
							
							elif len(text_split) == 3:
								team_1 = text_split[0]
								team_2 = text_split[-1]

								df_game_schedule.loc[count, 'year'] = self.year
								df_game_schedule.loc[count, 'season'] = self.season
								df_game_schedule.loc[count, 'league_name'] = self.league
								df_game_schedule.loc[count, 'week'] = week_num
								df_game_schedule.loc[count, 'date'] = game_date
								df_game_schedule.loc[count, 'team_1'] = team_1[:-2]
								df_game_schedule.loc[count, 'team_2'] = team_2[2:]
								count += 1



							elif len(text_split) == 4:
								team_1 = text_split[0]
								team_2 = text_split[-1]

								df_game_schedule.loc[count, 'year'] = self.year
								df_game_schedule.loc[count, 'season'] = self.season
								df_game_schedule.loc[count, 'league_name'] = self.league
								df_game_schedule.loc[count, 'week'] = week_num
								df_game_schedule.loc[count, 'date'] = game_date
								df_game_schedule.loc[count, 'team_1'] = team_1[:-2]
								df_game_schedule.loc[count, 'team_2'] = team_2[2:]
								df_game_schedule.loc[count, 'result'] = text_split[1] + '-' + text_split[2]
								count += 1

							else:
								print(f'Tiebreaker in Year: {self.year}, League: {self.league}, Season: {self.season}')
								week_num = 'Tiebreakers'
				self.df = df_game_schedule
			else:
				soup = BeautifulSoup(self.driver.page_source)
				vods_match_links_trs = soup.find("table", attrs={"id":"md-table"}).find_all("tr")
			
				column_list = []
				for th in vods_match_links_trs[2].find_all("th"):
					column_list.append(th.text)

				row_list = []
				for tr in vods_match_links_trs:
					try:
						if ('mdv-allweeks' in tr.attrs["class"]) and ('column-label-small' not in tr.attrs["class"]):
							row_list.append(tr)
						else:
							pass
					except KeyError:
						pass

				vods_match_links_dict = {}
				for rowkey in range(len(row_list)):
					vods_match_links_dict[rowkey] = {}
					td_list = row_list[rowkey].find_all("td")	
					for colkey in range(len(td_list)):
						vods_match_links_dict[rowkey][column_list[colkey-len(td_list)]] = td_list[colkey-len(td_list)]

					
				df_match_history = pd.DataFrame()


				for rowkey in vods_match_links_dict.keys():
					df_match_history.loc[rowkey, 'year'] = self.year
					df_match_history.loc[rowkey, 'season'] = self.season
					df_match_history.loc[rowkey, 'league_name'] = self.league
					
					for col in vods_match_links_dict[rowkey].keys():
						try:
							if col == "Team 1":
								df_match_history.loc[rowkey, col] = vods_match_links_dict[rowkey][col].find("span", attrs={"class":"teamname"}).text
							elif col == "Team 2":
								df_match_history.loc[rowkey, col] = vods_match_links_dict[rowkey][col].find("span", attrs={"class":"teamname"}).text
							elif col == "Blue":
								df_match_history.loc[rowkey, col] = vods_match_links_dict[rowkey][col].text
							elif col == "Red":
								df_match_history.loc[rowkey, col] = vods_match_links_dict[rowkey][col].text
							elif col == "MH":
								df_match_history.loc[rowkey, col] = vods_match_links_dict[rowkey][col].a.attrs["href"]
							elif col == "VODs":
								vods_a_list = vods_match_links_dict[rowkey][col].find_all("a")
								for vod_a in vods_a_list:
									df_match_history.loc[rowkey, vod_a.text] = vod_a.attrs["href"]
							elif col == "MVP":
								df_match_history.loc[rowkey, col] = vods_match_links_dict[rowkey][col].text
							else:
								pass

						except KeyError:
							pass
						except AttributeError:
							pass
				self.df_mh = df_match_history
		return

	def save_df(self, PATH, df='mh'):
		if df == 'mh':
			if self.df_mh is not None:
				self.df_mh.to_csv(PATH, index=False)
			else:
				pass
		else:
			if self.df is not None:
				self.df.to_csv(PATH, index=False)
			else:
				pass