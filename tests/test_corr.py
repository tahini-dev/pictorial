import numpy as np
import pandas as pd
import pytest

import pictorial.core.corr
import tests.util

NAN = float('nan')


@pytest.mark.parametrize('args, kwargs, expected', [
    (
        (pd.DataFrame([range(10)] * 2).T,),
        dict(),
        {
            'x': np.array([0, 1], dtype=np.int64),
            'y': np.array([0, 1], dtype=np.int64),
            'z': np.array([[np.nan, np.nan], [1., np.nan]])
        },
    ),
])
def test_get_corr_fig(args, kwargs, expected):
    actual = pictorial.core.corr.plot(*args, **kwargs)
    tests.util.assert_heatmap_equals(expected, actual.data[0])


@pytest.mark.parametrize('args, kwargs, expected', [
    ((pd.DataFrame([range(10)] * 2).T,), dict(), pd.DataFrame([[NAN, NAN], [1, NAN]])),
    ((pd.DataFrame([range(10)] * 3).T,), dict(), pd.DataFrame([[NAN, NAN, NAN], [1, NAN, NAN], [1, 1, NAN]])),
])
def test_get_lower_correlation_matrix(args, kwargs, expected):
    actual = pictorial.core.corr.get_lower_correlation_matrix(*args, **kwargs)
    pd.testing.assert_frame_equal(expected, actual)