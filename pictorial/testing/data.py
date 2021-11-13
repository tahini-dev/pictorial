import pandas as pd
import numpy as np
import plotly.express as px


def create_test_df(dataset='stocks'):
    if dataset == 'stocks':
        return px.data.stocks().melt(id_vars=['date'], var_name='ticker', value_name='price')
    elif dataset == 'random':
        num_rows = 50
        np.random.seed(1)
        costs = np.random.randint(1, 10, num_rows)
        dates = np.random.choice(pd.date_range(start='2021.10.01', end='2021-10-31'), num_rows)
        names = np.random.choice(['abc', 'def', 'ghi', 'jkl'], num_rows)
        return pd.DataFrame(dict(date=dates, names=names, cost=costs))


if __name__ == '__main__':
    df = create_test_df()