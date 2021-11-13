import pandas as pd


def group_plot(df, group_col, func):
    return df.groupby(group_col).apply(func)
