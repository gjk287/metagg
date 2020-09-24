import numpy as np

def wma(x, rolling_window):
    arr = np.arange(rolling_window, 0, -1)
    return np.exp(-arr/4.5)

def dot_wma(x, rolling_window):
    w = wma(x, rolling_window)
    return np.dot(x, w)


def opp_team(team_1, team_2, cor_team):
    if team_1 == cor_team:
        return team_2
    elif team_2 == cor_team:
        return team_1