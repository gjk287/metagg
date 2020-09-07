from datetime import datetime, timedelta, date
import time
import pandas as pd

def datetime_to_strft(date):
	try:
		return_date = date.strftime('%Y-%m-%d')
	except:
		return_date = None
	return return_date

def stringDate_to_strft(date):
	new_date = pd.to_datetime(date).strftime('%Y-%m-%d')
	return new_date

# for oddsportal date
def str_to_datetime(date):
	try:
		dateObj = datetime.strptime(date, '%d %b %Y')
	except:
		if ('Yesterday' in date) | ('Today' in date):
			new_date = date.split(', ')[-1]
			new_day = new_date.split(' ')[0]
			new_month = new_date.split(' ')[1]
			date = f'{new_day} {new_month} {2020}'
			dateObj = datetime.strptime(date, '%d %b %Y')
		else:
			dateObj = None
	return dateObj
