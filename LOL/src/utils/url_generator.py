import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dictionary import GameDictionary


class UrlGenerator(object):
	def __init__(self):
		#self.site = site
		self.league = None
		self.start_year = 2017
		self.end_year = 2020
		self.url = None

	def set_startToEndYear(self, start_year, end_year):
		self.start_year = start_year
		self.end_year = end_year

	def set_league(self, league=None):
		if not league:
			self.league = [
				'LCS', 'LEC', 'LCK', 'LPL', 'CBLOL', 'LCL', 'LJL', 'LLA', 'OPL', 'PCS', 'TCL', 'VCS'
			]
		else:
			self.league = league

class UrlGamepedia(UrlGenerator):
	def __init__(self):
		super().__init__()
		self.leagueSeason_dict = {
			**dict.fromkeys(['LCS', 'NA_LCS', 'LEC', 'EU_LCS', 'NA_Academy_League', 'NA_Challenger_Series', 'EU_Challenger_Series',
			'LCK', 'Challengers_Korea', 'LPL', 'LSPL', 'LDL', 'LMS', 'ECS', 'LCL', 'LJL', 'VCS_A', 'VCS', 'PCS', 'LPLOL', 
			'PG_Nationals', 'CIS_Challenger_League'], ['Spring_Season', 'Summer_Season']),
			**dict.fromkeys(['OPL', 'CBLOL', 'Brazilian_Challenger_Circuit', 'OCS'], ['Split_1', 'Split_2']),
			**dict.fromkeys(['TCL', 'Turkey_Academy_League'], ['Winter_Season', 'Summer_Season']),
			**dict.fromkeys(['Belgian_League', 'Dutch_League'], ['Spring_Split', 'Summer_Split']),
			**dict.fromkeys(['LLA'], ['Opening_Season', 'Closing_Season']),
			**dict.fromkeys(['European_Masters'], ['Spring/Play-In', 'Summer/Play-In'])
		}
		self.availableYearForEachLeague_dict = {
			**dict.fromkeys(['LCK', 'Challengers_Korea', 'LPL', 'CBLOL', 'Brazilian_Challenger_Circuit', 'LCL', 'LJL', 'OPL', 'TCL'], [2017 + x for x in range(4)]),
			**dict.fromkeys(['NA_Academy_League', 'European_Masters', 'VCS'], [2018, 2019, 2020]),
			**dict.fromkeys(['LCS', 'LEC', 'Turkey_Academy_League', 'LDL'], [2019, 2020]),
			**dict.fromkeys(['NA_LCS', 'EU_LCS'], [2017, 2018]),
			**dict.fromkeys(['NA_Challenger_Series', 'EU_Challenger_Series', 'LSPL', 'VCS_A', 'OCS'], [2017]),
			**dict.fromkeys(['LMS', 'ECS'], [2017, 2018, 2019]),
			**dict.fromkeys(['CIS_Challenger_League'], [2018]),
			**dict.fromkeys(['PCS', 'Dutch_League', 'Belgian_League', 'LPLOL', 'LLA', 'PG_Nationals'], [2020])		
		}

	def available_league(self):
		return list(set(self.leagueSeason_dict.keys()))

	def set_league(self, league=None):
		if not league:
			self.league = self.available_league()
		else:
			self.league = league
		return

	def _change_seasonValueToSpringSummer(self, url):
		check = url.split('/')[-1]
		if check == 'Play-In':
			season = url.split('/')[-2]
		else:
			season = url.split('/')[-1]

		if season.split('_')[0].lower() == 'split':
			if season.split('_')[-1] == '1':
				season_val = 'spring'
			else:
				season_val = 'summer'
		elif (season.split('_')[0].lower() == 'winter') | (season.split('_')[0].lower() == 'opening'):
			season_val = 'spring'
		elif season.split('_')[0].lower() == 'closing':
			season_val = 'summer'
		else:
			season_val = season.split('_')[0].lower()
		return season_val

	def get_seasonFromUrl(self, url):
		return self._change_seasonValueToSpringSummer(url)

	def get_leagueFromUrl(self, url):
		g_dict = GameDictionary()
		check = url.split('/')[-1]
		if check == 'Play-In':
			temp_league = url.split('/')[-4]
		else:
			temp_league = url.split('/')[-3]
		
		return g_dict.get_dict('league')[temp_league]

	def get_yearFromUrl(self, url):
		check = url.split('/')[-1]
		if check == 'Play-In':
			year = int(url.split('/')[-3].split('_')[0])
		else:
			year = int(url.split('/')[-2].split('_')[0])
		return year

	def generate_url(self):
		url_list = []
		for league in self.league:
			yr_range = self.end_year - self.start_year
			for year in [self.start_year + x for x in range(yr_range+1)]:
				if year in self.availableYearForEachLeague_dict[league]:
					if (league == 'European_Masters') & (year >= 2018):
						self.leagueSeason_dict['European_Masters'] = ['Spring_Play-In', 'Summer_Play-In']
					else:
						self.leagueSeason_dict['European_Masters'] = ['Spring/Play-In', 'Summer/Play-In']
					for season in self.leagueSeason_dict[league]:
						temp_url = f'https://lol.gamepedia.com/{league}/{year}_Season/{season}'
						url_list.append(temp_url)
				else:
					pass
		return url_list


class UrlOddsportal(UrlGenerator):
	def __init__(self):
		super().__init__()
		self.nation_dict = {
			'Korea':['south-korea', 'champions-korea'], #2020: 4, 2019: 4, 2018: 4, 2017: 4   #year: page_num
			'Australia':['australia', 'oceanic-pro-league'], #2020: 4, 2019: 4, 2018: 2, 2017: 2
			'Brazil':['brazil', 'circuito-brasileiro-de-league-of-legends'], #2020: 4, 2019: 4, 2018: 2, 2017: 1
			'China':['china', 'lol-pro-league'], #2020: 6, 2019: 6, 2018: 6, 2017: 5
			'Europe':['europe', 'european-championship'], #2020: 4, 2019: 4
			'Russia':['russia', 'lol-continental-league'], #2020: 3, 2019: 3, 2018: 3, 2017: 3
			'USA':['usa', 'championship-series']
		}
		self.availableYearForEachLeague_dict = {
			**dict.fromkeys(['Korea', 'Australia', 'Brazil', 'China', 'Russia', 'USA'], [2017 + x for x in range(4)]),
			**dict.fromkeys(['Europe'], [2019, 2020])
		}
		self.availablePageForEachLeague_dict = {
			**dict.fromkeys([('Brazil', 2017), ], 1),
			**dict.fromkeys([('Australia', 2017), ('Australia', 2018), ('Brazil', 2018), ], 2),
			**dict.fromkeys([('Russia', 2017), ('Russia', 2018), ('Russia', 2019), ('Russia', 2020), ], 3),
			**dict.fromkeys([('Korea', 2017), ('Korea', 2018), ('Korea', 2019), ('Korea', 2020), ('Australia', 2019), ('Australia', 2020), 
			('Brazil', 2019), ('Brazil', 2020), ('Europe', 2019), ('Europe', 2020), ('USA', 2019), ('USA', 2020)], 4),
			**dict.fromkeys([('China', 2017), ], 5),
			**dict.fromkeys([('China', 2018), ('China', 2019), ('China', 2020), ], 6),
			**dict.fromkeys([('USA', 2017), ], 7),
			**dict.fromkeys([('USA', 2018), ], 8),
		}
		self.leagueCountry_dict = {
			'LCK':'Korea',
			'OPL':'Australia',
			'CBLOL':'Brazil',
			'LPL':'China',
			'LEC':'Europe',
			'LCL':'Russia',
			'LCS':'USA'
		}

	def get_all_leagues(self):
		return list(self.leagueCountry_dict.keys())

	def set_league(self, league=None):
		if not league:
			self.league = self.get_all_leagues()
		else:
			self.league = league
		return

	def generate_url(self):
		url_dict = dict()
		for league in self.league:
			country = self.leagueCountry_dict[league]
			yr_range = self.end_year - self.start_year
			for year in [self.start_year + x for x in range(yr_range+1)]:
				if year in self.availableYearForEachLeague_dict[country]:
					country_url = self.nation_dict[country][0]
					league_url = self.nation_dict[country][-1]
					page_num = self.availablePageForEachLeague_dict[(country, year)]
					if year == 2020:
						temp_url = f'https://www.oddsportal.com/esports/{country_url}/league-of-legends-{league_url}/results/'
					else:
						temp_url = f'https://www.oddsportal.com/esports/{country_url}/league-of-legends-{league_url}-{int(year)}/results/'
					url_dict[temp_url] = {'Country': country, 'page_num': page_num, 'League': league, 'Year': year}
		return url_dict