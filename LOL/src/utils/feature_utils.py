import numpy as np
from sklearn.preprocessing import minmax_scale
import pandas as pd

def wma(x, rolling_window, div=4.5):
	arr = np.arange(rolling_window, 0, -1)
	return np.exp(-arr/div)

def dot_wma(x, rolling_window, div=4.5):
	w = wma(x, rolling_window, div)
	return np.dot(x, w)


def opp_team(team_1, team_2, cor_team):
	if team_1 == cor_team:
		return team_2
	elif team_2 == cor_team:
		return team_1


def normal(df, col_to_norm, method='minmax'):
	if method == 'minmax':
		return minmax_scale(df[col_to_norm])

	elif method == 'game_length':
		for col in col_to_norm:
			df[col] = (df[col] * 60 / df[method])
		return df[col_to_norm]