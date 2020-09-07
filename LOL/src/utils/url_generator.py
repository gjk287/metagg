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