import numpy as np
import pandas as pd
import pytest

import pictorial.core.bar
import pictorial.testing


@pytest.mark.parametrize('args, kwargs, expected', [
    # Simple test with one bar and no optional arguments
    (
        (),
        dict(df=pd.DataFrame(dict(a=range(5), b=[1] * 5, c=[2] * 5)), y='a'),
        dict(data=[dict(x=np.array([0]), y=np.array([10]))]),
    ),
    # Simple test with one bar and specific x value
    (
        (),
        dict(df=pd.DataFrame(dict(a=range(5), b=[1] * 5, c=[2] * 5)), y='a', x='b'),
        dict(data=[dict(x=np.array([1]), y=np.array([10]))]),
    ),
    # Two bars
    (
        (),
        dict(df=pd.DataFrame(dict(a=range(5), b=[1] * 2 + [2] * 3, c=[2] * 5)), y='a', x='b'),
        dict(data=[dict(x=np.array([1, 2]), y=np.array([1, 9]))]),
    ),
    # Two bars with a different split
    (
        (),
        dict(df=pd.DataFrame(dict(a=range(5), b=[2] * 3 + [1] * 2, c=[2] * 5)), y='a', x='b'),
        dict(data=[dict(x=np.array([1, 2]), y=np.array([7, 3]))]),
    ),
    # Two bars and testing the ordering
    (
        (),
        dict(df=pd.DataFrame(dict(a=range(5), b=['aa'] * 3 + ['bb'] * 2, c=[2] * 5)), y='a', x='b'),
        dict(
            data=[dict(x=np.array(['aa', 'bb']), y=np.array([3, 7]))],
            layout=dict(xaxis=dict(categoryorder='array', categoryarray=['bb', 'aa'])),
        ),
    ),
    # Two bars and testing the ordering
    (
        (),
        dict(df=pd.DataFrame(dict(a=range(5), b=['bb'] * 3 + ['aa'] * 2, c=[2] * 5)), y='a', x='b'),
        dict(
            data=[dict(x=np.array(['aa', 'bb']), y=np.array([7, 3]))],
            layout=dict(xaxis=dict(categoryorder='array', categoryarray=['aa', 'bb'])),
        ),
    ),
])
def test_plot(args, kwargs, expected):
    actual = pictorial.core.bar.plot(*args, **kwargs)
    pictorial.testing.assert_equals(expected, actual)
