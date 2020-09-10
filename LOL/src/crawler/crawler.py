from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

class Crawler(object):
	def __init__(self, url, wait_on_page_load=10):
		self.url = url
		self.wait_on_page_load = wait_on_page_load
		if wait_on_page_load == None:
			self.wait_on_page_load = 10
		self.driver = None

	def go_to_link(self):
		self.driver.get(self.url)
		time.sleep(self.wait_on_page_load)
		return

	def close_browser(self):
		self.driver.quit()
		return

	def get_driver(self):
		# self.driver = webdriver.Chrome(
		# 	r'C:\Users\jjames\iCloudDrive\Desktop\Cloud_Data\Personal_Projects\meta-gg\chromedriver\chromedriver.exe')
		self.driver = webdriver.Chrome(ChromeDriverManager().install())

	def scroll_down(self):
		SCROLL_PAUSE_TIME = 1
		# Get scroll height
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		while True:
			# Scroll down to bottom
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# Wait to load page
			time.sleep(SCROLL_PAUSE_TIME)

			# Calculate new scroll height and compare with last scroll height
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height
		time.sleep(15)
		return