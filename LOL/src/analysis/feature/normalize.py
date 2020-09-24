from sklearn.preprocessing import minmax_scale
import pandas as pd


def normal(df, col_to_norm, method='minmax'):
    if method == 'minmax':
        return minmax_scale(df[col_to_norm])

    elif method == 'game_length':
        for col in col_to_norm:
            df[col] = (df[col] * 60 / df[method])
        return df[col_to_norm]