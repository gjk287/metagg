import pandas as pd
from selenium import webdriver
import time
import sys
import os
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import io
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import mh_column_dict

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')


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
		self.driver = webdriver.Chrome(r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta-gg\chromedriver\chromedriver.exe', chrome_options=options)
		self.column_dict = mh_column_dict

	def crawl_data(self, username, password):
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
					self.save_df(league, year, season)

	def save_df(self, league, year, season):
		player_PATH = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\RawData\\MatchHistory\\player\\{league}-{int(year)}-{season}-player.csv'
		team_PATH = f'C:\\Users\\jjames\\iCloudDrive\\Desktop\\Cloud_Data\\Personal_Projects\\meta.gg\\LOL\\datasets\\RawData\\MatchHistory\\team\\{league}-{int(year)}-{season}-team.csv'
		
		self.df_player.to_csv(player_PATH, index=False)
		self.df_team.to_csv(team_PATH, index=False)
