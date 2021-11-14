import pytest
import pandas

import pictorial.utility


@pytest.mark.parametrize('value, expected', [
    (None, []),
    (pandas.Index([]), []),
    (pandas.Index([1, 2, 3]), [1, 2, 3]),
    (pandas.Series([]), []),
    (pandas.Series([1, 2, 3]), [1, 2, 3]),
    ('test', ['test']),
    ([], []),
    (tuple(), []),
    ([1, 2, 3], [1, 2, 3]),
    ((1, 2, 3), [1, 2, 3]),
])
def test_validate_index(value, expected):
    actual = pictorial.utility.validate_index(value)
    assert expected == actual

# TODO: add hypothesis tests
