import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import dot_wma, opp_team

def past_feature(df, col_to_use, game_past=1):
    concat_df = pd.DataFrame()

    for league in df['league_name'].unique():
        temp_league = df[df['league_name']==league]
        for year in temp_league['year'].unique():
            temp_year = temp_league[temp_league['year']==year]
            for season in temp_year['season'].unique():
                temp_season = temp_year[temp_year['season']==season]
                for team in temp_season['corresponding_team'].unique():
                    temp_unique_team = temp_season[temp_season['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
                    
                    for i in range(game_past):
                        temp_unique_team[[f'{x}__{i+1}' for x in col_to_use]] = temp_unique_team[col_to_use].shift(i+1)
                    
                    concat_df = pd.concat([concat_df, temp_unique_team]).reset_index(drop=True)
    return concat_df


def win_sum_feature(df, rolling_window=3):
    concat_df = pd.DataFrame()

    for league in df['league_name'].unique():
        temp_league = df[df['league_name']==league]
        for team in temp_league['corresponding_team'].unique():
            temp_team = temp_league[temp_league['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
            #temp_team['cum_win_rate'] = temp_team['wdl'].apply(lambda x: 1 if x == 'W' else 0).expanding(1).mean().shift(1)
            for year in temp_team['year'].unique():
                temp_year = temp_team[temp_team['year']==year]
                for season in temp_year['season'].unique():
                    temp_season = temp_year[temp_year['season']==season]
                    temp_season[f'win_sum__{rolling_window}'] = temp_season['wdl'].apply(lambda x: 1 if x == 'W' else 0).rolling(rolling_window).sum().shift(1)
                    concat_df = pd.concat([concat_df, temp_season]).reset_index(drop=True)
    return concat_df


def cum_win_sum_feature(df):
    concat_df = pd.DataFrame()

    for league in df['league_name'].unique():
        temp_league = df[df['league_name']==league]
        for team in temp_league['corresponding_team'].unique():
            temp_team = temp_league[temp_league['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
            for year in temp_team['year'].unique():
                temp_year = temp_team[temp_team['year']==year]
                for season in temp_year['season'].unique():
                    temp_season = temp_year[temp_year['season']==season]
                    temp_season['cum_win_sum'] = temp_season['wdl'].apply(lambda x: 1 if x == 'W' else 0).expanding(1).sum().shift(1)
                    concat_df = pd.concat([concat_df, temp_season]).reset_index(drop=True)
    return concat_df


def cum_opp_win_rate_feature(df):
    concat_df = pd.DataFrame()

    for league in df['league_name'].unique():
        temp_league = df[df['league_name']==league]
        for team in temp_league['corresponding_team'].unique():
            temp_team = temp_league[temp_league['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
            temp_team['opp_team'] = temp_team.apply(lambda row: opp_team(row['team_1'], row['team_2'], row['corresponding_team']), axis=1)
            for opTeam in temp_team['opp_team'].unique():
                temp_team_opp = temp_team[(temp_team['team_1']==opTeam) | (temp_team['team_2']==opTeam)]
                temp_team_opp['cum_opp_win_rate'] = temp_team_opp['wdl'].apply(lambda x: 1 if x == 'W' else 0).expanding(1).mean().shift(1)
                concat_df = pd.concat([concat_df, temp_team_opp]).reset_index(drop=True)
                    
    return concat_df





# def weighted_ma_feature(df, col_to_use, rolling_window=3):
#     concat_df = pd.DataFrame()

#     for league in df['league_name'].unique():
#         temp_league = df[df['league_name']==league]
#         for year in temp_league['year'].unique():
#             temp_year = temp_league[temp_league['year']==year]
#             for season in temp_year['season'].unique():
#                 temp_season = temp_year[temp_year['season']==season]
#                 for team in temp_season['corresponding_team'].unique():
#                     temp_unique_team = temp_season[temp_season['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
#                     temp_unique_team[col_to_use] = temp_unique_team[col_to_use].rolling(window=rolling_window).apply(lambda x: dot_wma(x, rolling_window)).shift(1)
                    
#                     concat_df = pd.concat([concat_df, temp_unique_team]).reset_index(drop=True)

#     return concat_df


# def sum_ma_feature(df, col_to_use, rolling_window=3):
#     concat_df = pd.DataFrame()

#     for league in df['league_name'].unique():
#         temp_league = df[df['league_name']==league]
#         for year in temp_league['year'].unique():
#             temp_year = temp_league[temp_league['year']==year]
#             for season in temp_year['season'].unique():
#                 temp_season = temp_year[temp_year['season']==season]
#                 for team in temp_season['corresponding_team'].unique():
#                     temp_unique_team = temp_season[temp_season['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
#                     temp_unique_team[col_to_use] = temp_unique_team[col_to_use].rolling(window=rolling_window).sum().shift(1)
                    
#                     concat_df = pd.concat([concat_df, temp_unique_team]).reset_index(drop=True)

#     return concat_df


# def win_weighted_sum_feature(df, rolling_window=3):
#     concat_df = pd.DataFrame()

#     for league in df['league_name'].unique():
#         temp_league = df[df['league_name']==league]
#         for team in temp_league['corresponding_team'].unique():
#             temp_team = temp_league[temp_league['corresponding_team']==team].sort_values(by=['date']).reset_index(drop=True)
#             #temp_team['cum_win_rate'] = temp_team['wdl'].apply(lambda x: 1 if x == 'W' else 0).expanding(1).mean().shift(1)
#             for year in temp_team['year'].unique():
#                 temp_year = temp_team[temp_team['year']==year]
#                 for season in temp_year['season'].unique():
#                     temp_season = temp_year[temp_year['season']==season]
#                     temp_season['win_weighted_sum'] = temp_season['wdl'].apply(lambda x: 1 if x == 'W' else 0).rolling(rolling_window).apply(lambda x: dot_wma(x, rolling_window)).shift(1)
#                     concat_df = pd.concat([concat_df, temp_season]).reset_index(drop=True)

#     return concat_df


# def cum_win_mean_feature():
#     pass