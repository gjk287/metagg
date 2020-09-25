import pandas as pd
import time
from bs4 import BeautifulSoup
import requests
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from crawler import Crawler


class QWER(Crawler):
	def __init__(self, league, year, season, url, wait_on_page_load=5):
		super().__init__(url, wait_on_page_load)
		self.league = league
		self.season = season
		self.year = year
		self.df = None

	def get_href_for_each_game(self):
		pass