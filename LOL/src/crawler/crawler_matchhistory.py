import pandas as pd
from selenium import webdriver
import time
import sys
import os
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import io
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import mh_column_dict, mh_china_column_dict

try:
	sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
	sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
except:
	pass


class MatchHistory(object):
	def __init__(self, df_mh, wait_on_page_load=15):
		self.df_mh = df_mh
		self.wait_on_page_load = wait_on_page_load
		self.df_player = None
		self.df_team = None
		options2 = Options() 
		prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2,
			'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2,
			'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2,
			'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2,
			'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}	 
		options2.add_experimental_option('prefs', prefs) 
		options2.add_argument("start-maximized") 
		options2.add_argument("disable-infobars") 
		options2.add_argument("--disable-extensions")
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--ignore-ssl-errors')
		self.driver = None
		self.column_dict = mh_column_dict
		self.china_column_dict = mh_china_column_dict

	def close_browser(self):
		self.driver.quit()
		return

	def get_driver(self):
		self.driver = webdriver.Chrome(ChromeDriverManager().install())

	def crawl_china(self):
		temp_mh = self.df_mh.copy()
		temp_mh = temp_mh.where(pd.notnull(temp_mh), None)
		for league in self.df_mh['league_name'].unique():
			df_mh_league = temp_mh[temp_mh['league_name']==league]
			for year in df_mh_league['year'].unique():
				df_mh_league_year = df_mh_league[df_mh_league['year']==year]
				for season in df_mh_league_year['season'].unique():
					df_mh_league_year_season = df_mh_league_year[df_mh_league_year['season']==season].reset_index(drop=True)
					
					df_player = pd.DataFrame()
					df_team = pd.DataFrame()
					for row_num in range(df_mh_league_year_season.shape[0]):
						df_player_each_row = pd.DataFrame()
						df_team_each_row = pd.DataFrame()
						if df_mh_league_year_season.loc[row_num, 'MH']:
							result_try = None
							result_try_coin = 0
							while result_try is None:
								try:
									url = df_mh_league_year_season.loc[row_num, 'MH']
									self.driver.get(url)
									time.sleep(self.wait_on_page_load)

									temp_click = self.driver.find_element_by_class_name('data-mode1-seasonbox')
									temp_click.find_element_by_id(f'tab-{int(df_mh_league_year_season.loc[row_num, "set_number"]-1)}').click()

									html = self.driver.page_source
									soup = BeautifulSoup(html, 'html.parser')
									result_try = 'Success'
									print('Success!!')

								except:
									result_try_coin += 1
									if result_try_coin == 5:
										result_try = 'Success?'


							result_value_try = 0
							while result_value_try < 5:
								try:
									print(f'Start: {result_value_try+1}!')
									week = df_mh_league_year_season.loc[row_num, "week"]
									team_1 = df_mh_league_year_season.loc[row_num, "team_1"]
									team_2 = df_mh_league_year_season.loc[row_num, "team_2"]
									set_number = df_mh_league_year_season.loc[row_num, "set_number"]
									date = soup.find('span', attrs={"id":"bmatch_date"}).text

									for row in range(2):
										df_team_each_row.loc[row, "year"] = year
										df_team_each_row.loc[row, "season"] = season
										df_team_each_row.loc[row, "league_name"] = league
										df_team_each_row.loc[row, "week"] = week
										df_team_each_row.loc[row, "team_1"] = team_1
										df_team_each_row.loc[row, "team_2"] = team_2
										df_team_each_row.loc[row, "set_number"] = set_number
										df_team_each_row.loc[row, "state"] = "OK"
										df_team_each_row.loc[row, "date"] = date

										if row == 0:
											df_team_each_row.loc[row, "side"] = 'red'
											df_team_each_row.loc[row, 'team'] = soup.find('p', attrs={"id":"teama-name"}).text
											df_team_each_row.loc[row, 'total_golds'] = soup.find('span', attrs={"id":"game-gold-total-left"}).text
											df_team_each_row.loc[row, 'total_kills'] = soup.find('p',  attrs={"id":"game-kda-k-total-num-left"}).text
											df_team_each_row.loc[row, 'tower_kills'] = soup.find('span', attrs={"id":"game-tower-num-left"}).text
											df_team_each_row.loc[row, 'baron_kills'] = soup.find('span', attrs={"id":"game-b-dragon-num-left"}).text
											df_team_each_row.loc[row, 'dragon_kills'] = soup.find('span', attrs={"id":"game-s-dragon-num-left"}).text
										else:
											df_team_each_row.loc[row, 'side'] = 'blue'
											df_team_each_row.loc[row, 'team'] = soup.find('p', attrs={"id":"teamb-name"}).text
											df_team_each_row.loc[row, 'total_golds'] = soup.find('span', attrs={"id":"game-gold-total-right"}).text
											df_team_each_row.loc[row, 'total_kills'] = soup.find('p',  attrs={"id":"game-kda-k-total-num-right"}).text
											df_team_each_row.loc[row, 'tower_kills'] = soup.find('span', attrs={"id":"game-tower-num-right"}).text
											df_team_each_row.loc[row, 'baron_kills'] = soup.find('span', attrs={"id":"game-b-dragon-num-right"}).text
											df_team_each_row.loc[row, 'dragon_kills'] = soup.find('span', attrs={"id":"game-s-dragon-num-right"}).text

										bans_each = soup.find_all('div', attrs={"class":"data-main-b"})[i].find_all('img')
										for i in range(len(bans_each)):
											df_team_each_row.loc[row, "ban{}".format(i+1)] = bans_each[i].attrs['src'].split("/")[-1].split(".")[0]

									battle_items = soup.find_all('tr', attrs={"class":"nr-battle-item"})
									for i in range(len(battle_items)):
										df_player_each_row.loc[i, 'year'] = year
										df_player_each_row.loc[i, 'season'] = season
										df_player_each_row.loc[i, 'league_name'] = league
										df_player_each_row.loc[i, 'week'] = week
										df_player_each_row.loc[i, 'team_1'] = team_1
										df_player_each_row.loc[i, 'team_2'] = team_2
										df_player_each_row.loc[i, 'set_number'] = set_number
										df_player_each_row.loc[i, 'date'] = date
										df_player_each_row.loc[i, 'side'] = 'red'
										df_player_each_row.loc[i, 'team'] = soup.find('p', attrs={"id":"teama-name"}).text
										df_player_each_row.loc[i, 'player_name'] = soup.find('p', attrs={"id":"nr-game-player-name-left-{}".format(i+1)}).text
										df_player_each_row.loc[i, 'champion'] = soup.find('img', attrs={"id":"nr-game-hero-left-{}".format(i+1)}).attrs['src'].split('/')[-1].split('.')[0]
										df_player_each_row.loc[i, 'kills'] = soup.find('span', attrs={"id":"nr-game-kda-k-num-left-{}".format(i+1)}).text
										df_player_each_row.loc[i, 'deaths'] = soup.find('span', attrs={"id":"nr-game-kda-d-num-left-{}".format(i+1)}).text
										df_player_each_row.loc[i, 'assists'] = soup.find('span', attrs={"id":"nr-game-kda-a-num-left-{}".format(i+1)}).text
										df_player_each_row.loc[i, 'golds'] = soup.find('td', attrs={"id":"nr-game-gold-num-left-{}".format(i+1)}).text
										df_player_each_row.loc[i, 'minions'] = soup.find('span', attrs={"id":"nr-game-lasthit-num-left-{}".format(i+1)}).text
										df_player_each_row.loc[i, 'spell_1'] = soup.find('img', attrs={"id":"nr-game-rune-u-left-{}".format(i+1)}).attrs['src'].split('/')[-1].split('.')[0].strip('Summoner')
										df_player_each_row.loc[i, 'spell_2'] = soup.find('img', attrs={"id":"nr-game-rune-skill-d-left-{}".format(i+1)}).attrs['src'].split('/')[-1].split('.')[0].strip('Summoner')
										
									for i in range(len(battle_items)):
										df_player_each_row.loc[i+5, 'year'] = year
										df_player_each_row.loc[i+5, 'season'] = season
										df_player_each_row.loc[i+5, 'league_name'] = league
										df_player_each_row.loc[i+5, 'week'] = week
										df_player_each_row.loc[i+5, 'team_1'] = team_1
										df_player_each_row.loc[i+5, 'team_2'] = team_2
										df_player_each_row.loc[i+5, 'set_number'] = set_number
										df_player_each_row.loc[i+5, 'date'] = date
										df_player_each_row.loc[i+5, 'side'] = 'blue'
										df_player_each_row.loc[i+5, 'team'] = soup.find('p', attrs={"id":"teama-name"}).text
										df_player_each_row.loc[i+5, 'player_name'] = soup.find('p', attrs={"id":"nr-game-player-name-right-{}".format(i+1)}).text
										df_player_each_row.loc[i+5, 'champion'] = soup.find('img', attrs={"id":"nr-game-hero-right-{}".format(i+1)}).attrs['src'].split('/')[-1].split('.')[0]
										df_player_each_row.loc[i+5, 'kills'] = soup.find('span', attrs={"id":"nr-game-kda-k-num-right-{}".format(i+1)}).text
										df_player_each_row.loc[i+5, 'deaths'] = soup.find('span', attrs={"id":"nr-game-kda-d-num-right-{}".format(i+1)}).text
										df_player_each_row.loc[i+5, 'assists'] = soup.find('span', attrs={"id":"nr-game-kda-a-num-right-{}".format(i+1)}).text
										df_player_each_row.loc[i+5, 'golds'] = soup.find('td', attrs={"id":"nr-game-gold-num-right-{}".format(i+1)}).text
										df_player_each_row.loc[i+5, 'minions'] = soup.find('span', attrs={"id":"nr-game-lasthit-num-right-{}".format(i+1)}).text
										df_player_each_row.loc[i+5, 'spell_1'] = soup.find('img', attrs={"id":"nr-game-summoner-skill-u-right-{}".format(i+1)}).attrs['src'].split('/')[-1].split('.')[0].strip('Summoner')
										df_player_each_row.loc[i+5, 'spell_2'] = soup.find('img', attrs={"id":"nr-game-summoner-skill-d-right-{}".format(i+1)}).attrs['src'].split('/')[-1].split('.')[0].strip('Summoner')
										
									self.driver.find_element_by_xpath('//div[@class="n-data-mode1-data disul"]/a[2]').click()
									try:
										for sub_type in self.china_column_dict.keys():
											time.sleep(2)
											self.driver.find_element_by_xpath('//dd[@data-type="{}"]/span'.format(sub_type)).click()
											soup_sub = BeautifulSoup(self.driver.page_source, "html.parser")
											stats = soup_sub.find_all('li', attrs={"type":sub_type})
											time.sleep(1)
											self.driver.find_element_by_xpath('//dd[@data-type="{}"]/span'.format(sub_type)).click()
											for i in range(len(stats)):
												df_player_each_row.loc[i, self.china_column_dict[sub_type]] = stats[i].text
									
									except:
										pass
								
								except:
									df_player_each_row.loc[0, "year"] = year
									df_player_each_row.loc[0, "season"] = season
									df_player_each_row.loc[0, "league_name"] = league
									df_player_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
									df_player_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
									df_player_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
									df_player_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
									df_player_each_row.loc[0, "state"] = "AttributeError"

									df_team_each_row.loc[0, "year"] = year
									df_team_each_row.loc[0, "season"] = season
									df_team_each_row.loc[0, "league_name"] = league
									df_team_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
									df_team_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
									df_team_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
									df_team_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
									df_team_each_row.loc[0, "state"] = "AttributeError"
									result_value_try += 1

						else:
							df_player_each_row.loc[0, "year"] = year
							df_player_each_row.loc[0, "season"] = season
							df_player_each_row.loc[0, "league_name"] = league
							df_player_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
							df_player_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
							df_player_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
							df_player_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
							df_player_each_row.loc[0, "state"] = "this row doesn't have MH_url"

							df_team_each_row.loc[0, "year"] = year
							df_team_each_row.loc[0, "season"] = season
							df_team_each_row.loc[0, "league_name"] = league
							df_team_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
							df_team_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
							df_team_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
							df_team_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
							df_team_each_row.loc[0, "state"] = "this row doesn't have MH_url"

						df_player = pd.concat([df_player, df_player_each_row]).reset_index(drop=True)
						df_team = pd.concat([df_team, df_team_each_row]).reset_index(drop=True)

						df_player.to_csv(r'C:\Users\jjames\Desktop\temp\player.csv', index=False)
						df_team.to_csv(r'C:\Users\jjames\Desktop\temp\team.csv', index=False)

					self.df_player = df_player
					self.df_team = df_team
					#self.save_df(league, year, season, missing)


	def crawl_data(self, username, password, missing=False):
		temp_mh = self.df_mh.copy()
		temp_mh = temp_mh.where(pd.notnull(temp_mh), None)
		login_coin = False
		for league in self.df_mh['league_name'].unique():
			df_mh_league = temp_mh[temp_mh['league_name']==league]
			for year in df_mh_league['year'].unique():
				df_mh_league_year = df_mh_league[df_mh_league['year']==year]
				for season in df_mh_league_year['season'].unique():
					df_mh_league_year_season = df_mh_league_year[df_mh_league_year['season']==season].reset_index(drop=True)
					
					df_player = pd.DataFrame()
					df_team = pd.DataFrame()
					for row_num in range(df_mh_league_year_season.shape[0]):
						df_player_each_row = pd.DataFrame()
						df_team_each_row = pd.DataFrame()
						if df_mh_league_year_season.loc[row_num, 'MH']:
							result_try = None
							while result_try is None:
								try:
									url = df_mh_league_year_season.loc[row_num, "MH"].split("&tab")[0] + "&tab=stats"
									self.driver.get(url)
									time.sleep(self.wait_on_page_load)
									if not login_coin:
										#input username
										user_name_box = self.driver.find_element_by_css_selector('body > div > div > div > div.grid.grid-direction__row.grid-page-web__content > div.grid.grid-direction__column.grid-page-web__wrapper > div > div.grid.grid-align-center.grid-justify-space-between.grid-fill.grid-direction__column.grid-panel-web__content.grid-panel__content > div > div > div > div:nth-child(1) > div > input')
										user_name_box.send_keys(username)
										time.sleep(1)
										# input password
										password_box = self.driver.find_element_by_css_selector('body > div > div > div > div.grid.grid-direction__row.grid-page-web__content > div.grid.grid-direction__column.grid-page-web__wrapper > div > div.grid.grid-align-center.grid-justify-space-between.grid-fill.grid-direction__column.grid-panel-web__content.grid-panel__content > div > div > div > div.field.password-field.field--animate > div > input')
										password_box.send_keys(password)
										time.sleep(1)
										# check box remember me and submit
										self.driver.find_element_by_xpath('//*[@data-testid="checkbox-remember-me"]').click()
										time.sleep(1)
										self.driver.find_element_by_xpath('//*[@data-testid="btn-signin-submit"]').click()
										time.sleep(self.wait_on_page_load)
										login_coin = True
									
									html = self.driver.page_source
									soup = BeautifulSoup(html, "html.parser")
									result_try = 'Success'

								except:
									pass


							result_value_try = 0
							while result_value_try < 5:
								try:
									week = df_mh_league_year_season.loc[row_num, "week"]
									team_1 = df_mh_league_year_season.loc[row_num, "team_1"]
									team_2 = df_mh_league_year_season.loc[row_num, "team_2"]
									set_number = df_mh_league_year_season.loc[row_num, "set_number"]
									date = soup.find("span", attrs={"class":"map-header-date"}).get_text()
									gametime = soup.find("span", attrs={"class":"map-header-duration"}).get_text()
									#print(f'{team_1} vs {team_2}: week: {week}, set_number: {set_number}, date: {date}, game_length: {gametime}, league: {league}')
									# player_df
									champion_names_div = soup.find_all("div", attrs={"class":"champion-nameplate-name"})
									#print(champion_names_div)
									for row in range(len(champion_names_div)):
										team_player = champion_names_div[row].get_text().strip().split(' ')
										df_player_each_row.loc[row, "year"] = year
										df_player_each_row.loc[row, "season"] = season
										df_player_each_row.loc[row, "league_name"] = league
										df_player_each_row.loc[row, "week"] = week
										df_player_each_row.loc[row, "team_1"] = team_1
										df_player_each_row.loc[row, "team_2"] = team_2
										df_player_each_row.loc[row, "set_number"] = set_number
										df_player_each_row.loc[row, "state"] = "OK"
										df_player_each_row.loc[row, "date"] = date
										df_player_each_row.loc[row, "team"] = team_player[0]
										df_player_each_row.loc[row, "player_name"] = ' '.join(team_player[1:])

									# champion
									characters_blue = soup.find("tr", attrs="grid-header-row").find_all("td", attrs={"class":"team-100"})
									characters_red = soup.find("tr", attrs="grid-header-row").find_all('td', attrs={"class":"team-200"})
									for row in range(len(characters_blue)):
										df_player_each_row.loc[row, "champion"] = characters_blue[row].find("div", attrs={"class":"champion-icon binding"}).div.attrs["data-rg-id"]
										df_player_each_row.loc[row, "side"] = "blue"
									for row in range(len(characters_red)):
										df_player_each_row.loc[row+5, "champion"] = characters_red[row].find("div", attrs={"class":"champion-icon binding"}).div.attrs["data-rg-id"]
										df_player_each_row.loc[row+5, "side"] = "red"
									# rest of column
									grid_rows = soup.find_all("tr", attrs={"class":"grid-row"})
									for idx, grid in enumerate(grid_rows):
										column_name = self.column_dict[idx]
										rows_blue = grid.find_all("td", attrs={"class":"team-100"})
										rows_red = grid.find_all("td", attrs={"class":"team-200"})
										if column_name == 'first_blood':
											for row in range(len(rows_blue)):
												df_player_each_row.loc[row, column_name] = rows_blue[row].text + 'fb'
											for row in range(len(rows_red)):
												df_player_each_row.loc[row+5, column_name] = rows_red[row].text + 'fb'
										else:
											for row in range(len(rows_blue)):
												df_player_each_row.loc[row, column_name] = rows_blue[row].get_text()
											for row in range(len(rows_red)):
												df_player_each_row.loc[row+5, column_name] = rows_red[row].get_text()

									# team_df
									for row in range(2):
										df_team_each_row.loc[row, "year"] = year
										df_team_each_row.loc[row, "season"] = season
										df_team_each_row.loc[row, "league_name"] = league
										df_team_each_row.loc[row, "week"] = week
										df_team_each_row.loc[row, "team_1"] = team_1
										df_team_each_row.loc[row, "team_2"] = team_2
										df_team_each_row.loc[row, "set_number"] = set_number
										df_team_each_row.loc[row, "game_length"] = gametime
										df_team_each_row.loc[row, "state"] = "OK"
										if row == 0:
											df_team_each_row.loc[row, "side"] = "blue"
										else:
											df_team_each_row.loc[row, "side"] = "red"

									champion_names_div = soup.find_all("div", attrs={"class":"champion-nameplate-name"})
									df_team_each_row.loc[0, 'team'] = champion_names_div[0].get_text().strip().split(' ')[0]
									df_team_each_row.loc[1, 'team'] = champion_names_div[-1].get_text().strip().split(' ')[0]

									summaries = soup.find_all("div", attrs={"class":"gs-container team-summary"})
									bans = soup.find_all("div", attrs={"class":"bans-container"})
									tower_kills = soup.find_all("div", attrs={"class":"tower-kills"})
									inhibitor_kills = soup.find_all("div", attrs={"class":"inhibitor-kills"})
									baron_kills = soup.find_all("div", attrs={"class":"baron-kills"})
									dragon_kills = soup.find_all("div", attrs={"class":"dragon-kills"})
									rift_kills = soup.find_all("div", attrs={"class":"rift-herald-kills"})

									for row in range(2):
										df_team_each_row.loc[row, 'result'] = summaries[row].find("div", attrs={"class":"game-conclusion"}).get_text()
										df_team_each_row.loc[row, 'total_golds'] = summaries[row].find("div", attrs={"class":"gold"}).get_text()
										df_team_each_row.loc[row, "total_kills"] = summaries[row].find("div", attrs={"class":"kills"}).get_text()
										df_team_each_row.loc[row, "tower_kills"] = tower_kills[row].get_text()
										df_team_each_row.loc[row, "inhibitor_kills"] = inhibitor_kills[row].get_text()
										df_team_each_row.loc[row, "baron_kills"] = baron_kills[row].get_text()
										df_team_each_row.loc[row, "dragon_kills"] = dragon_kills[row].get_text()
										df_team_each_row.loc[row, "rift_kills"] = rift_kills[row].get_text()

										bans_each = bans[row].find_all("div", attrs={"class":"champion-icon binding"})
										for i in range(len(bans_each)):
											df_team_each_row.loc[row, "ban{}".format(i+1)] = bans_each[i].div.attrs["data-rg-id"]
									result_value_try += 5
									
								
								except:
									df_player_each_row.loc[0, "year"] = year
									df_player_each_row.loc[0, "season"] = season
									df_player_each_row.loc[0, "league_name"] = league
									df_player_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
									df_player_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
									df_player_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
									df_player_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
									df_player_each_row.loc[0, "state"] = "AttributeError"

									df_team_each_row.loc[0, "year"] = year
									df_team_each_row.loc[0, "season"] = season
									df_team_each_row.loc[0, "league_name"] = league
									df_team_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
									df_team_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
									df_team_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
									df_team_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
									df_team_each_row.loc[0, "state"] = "AttributeError"
									result_value_try += 1

						else:
							df_player_each_row.loc[0, "year"] = year
							df_player_each_row.loc[0, "season"] = season
							df_player_each_row.loc[0, "league_name"] = league
							df_player_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
							df_player_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
							df_player_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
							df_player_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
							df_player_each_row.loc[0, "state"] = "this row doesn't have MH_url"

							df_team_each_row.loc[0, "year"] = year
							df_team_each_row.loc[0, "season"] = season
							df_team_each_row.loc[0, "league_name"] = league
							df_team_each_row.loc[0, "week"] = df_mh_league_year_season.loc[row_num, 'week']
							df_team_each_row.loc[0, "team_1"] = df_mh_league_year_season.loc[row_num, 'team_1']
							df_team_each_row.loc[0, "team_2"] = df_mh_league_year_season.loc[row_num, 'team_2']
							df_team_each_row.loc[0, "set_number"] = df_mh_league_year_season.loc[row_num, 'set_number']
							df_team_each_row.loc[0, "state"] = "this row doesn't have MH_url"

						df_player = pd.concat([df_player, df_player_each_row]).reset_index(drop=True)
						df_team = pd.concat([df_team, df_team_each_row]).reset_index(drop=True)
					self.df_player = df_player
					self.df_team = df_team
					self.save_df(league, year, season, missing)

	def save_df(self, league, year, season, missing=False):
		if missing:
			player_PATH = f'C:\\Users\\jjames\\Dropbox\\Cloud_Data\\Projects\\Game-Data-Platform\\meta.gg\\LOL\\datasets\\RawData\\MatchHistory\\player\\{league}-{int(year)}-{season}-player-missing.csv'
			team_PATH = f'C:\\Users\\jjames\\Dropbox\\Cloud_Data\\Projects\\Game-Data-Platform\\meta.gg\\LOL\\datasets\\RawData\\MatchHistory\\team\\{league}-{int(year)}-{season}-team-missing.csv'
		else:
			player_PATH = f'C:\\Users\\jjames\\Dropbox\\Cloud_Data\\Projects\\Game-Data-Platform\\meta.gg\\LOL\\datasets\\RawData\\MatchHistory\\player\\{league}-{int(year)}-{season}-player.csv'
			team_PATH = f'C:\\Users\\jjames\\Dropbox\\Cloud_Data\\Projects\\Game-Data-Platform\\meta.gg\\LOL\\datasets\\RawData\\MatchHistory\\team\\{league}-{int(year)}-{season}-team.csv'
		
		self.df_player.to_csv(player_PATH, index=False)
		self.df_team.to_csv(team_PATH, index=False)
