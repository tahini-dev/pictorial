import pandas as pd
import pytest
import pandas

import pictorial.aggregate

nan = float('nan')


@pytest.mark.parametrize('args, kwargs, expected_error, expected_message', [
    # Column does not exist
    ([], dict(df=pandas.DataFrame(), column='test', aggregator='sum'), KeyError, 'Column not found: test'),
])
def test_error_generic(args, kwargs, expected_error, expected_message):
    with pytest.raises(expected_error) as error:
        pictorial.aggregate.generic(*args, **kwargs)
    assert expected_message == error.value.args[0]


@pytest.mark.parametrize('args, kwargs, expected', [
    # Empty dataframe - count
    (
        [],
        dict(df=pandas.DataFrame(columns=['test']), column='test', aggregator='count'),
        pd.DataFrame(columns=['test'], index=range(0)).astype('int64'),
    ),
    # Empty dataframe - sum
    (
        [],
        dict(df=pandas.DataFrame(columns=['test']), column='test', aggregator='sum'),
        pd.DataFrame(columns=['test'], index=range(0)),
    ),
    # Empty dataframe - sum as function
    (
        [],
        dict(df=pandas.DataFrame(columns=['test']), column='test', aggregator=sum),
        pd.DataFrame(columns=['test'], index=range(0)),
    ),
    # Non empty dataframe - count
    (
        [],
        dict(df=pandas.DataFrame(dict(test=[0, 1, 2])), column='test', aggregator='count'),
        pd.DataFrame(dict(test=[3])),
    ),
    # Non empty dataframe with group-by columns - count
    (
        [],
        dict(
            df=pandas.DataFrame(dict(test=[0, 1, 2], test_by=[1, 2, 1])),
            column='test',
            aggregator='count',
            by='test_by',
        ),
        pd.DataFrame(dict(test_by=[1, 2], test=[2, 1])),
    ),
    # Non empty dataframe with additional columns - count
    (
        [],
        dict(
            df=pandas.DataFrame(dict(test=[0, 1, 2], test_by=[1, 2, 1])),
            column='test',
            aggregator='count',
        ),
        pd.DataFrame(dict(test=[3])),
    ),
    # Non empty dataframe with multiple group-by columns - count
    (
        [],
        dict(
            df=pandas.DataFrame(dict(test=[0, 1, 2], test_by_1=[1, 2, 1], test_by_2=['a', 'b', 'c'])),
            column='test',
            aggregator='count',
            by=['test_by_1', 'test_by_2']
        ),
        pd.DataFrame(dict(test_by_1=[1, 1, 2], test_by_2=['a', 'c', 'b'], test=[1, 1, 1])),
    ),
    # Non empty dataframe with multiple group-by columns with different order - count
    (
        [],
        dict(
            df=pandas.DataFrame(dict(test=[0, 1, 2], test_by_1=[1, 2, 1], test_by_2=['a', 'b', 'c'])),
            column='test',
            aggregator='count',
            by=['test_by_2', 'test_by_1']
        ),
        pd.DataFrame(dict(test_by_2=['a', 'b', 'c'], test_by_1=[1, 2, 1], test=[1, 1, 1])),
    ),
])
def test_generic(args, kwargs, expected):
    actual = pictorial.aggregate.generic(*args, **kwargs)
    pandas.testing.assert_frame_equal(expected, actual)


@pytest.mark.parametrize('args, kwargs, expected_error, expected_message', [
    # Empty dataframe does not work
    (
        [],
        dict(df=pandas.DataFrame(columns=['test']), column='test'),
        ValueError,
        "index must be a MultiIndex to unstack, <class 'pandas.core.indexes.numeric.Int64Index'> was passed",
    ),
])
def test_error_describe(args, kwargs, expected_error, expected_message):
    with pytest.raises(expected_error) as error:
        pictorial.aggregate.describe(*args, **kwargs)
    assert expected_message == error.value.args[0]


def make_dataframe_describe(count, mean, std, min, lower_quartile, median, upper_quartile, max, **kwargs):
    df = pandas.concat(
        [
            pandas.DataFrame(dict(**kwargs)),
            pandas.DataFrame({
                'count': count,
                'mean': mean,
                'std': std,
                'min': min,
                '25%': lower_quartile,
                '50%': median,
                '75%': upper_quartile,
                'max': max,
            }).astype(float),
        ],
        axis=1,
    )

    return df


@pytest.mark.parametrize('args, kwargs, expected', [
    # No group-by columns and only nans in column
    (
        [],
        dict(df=pandas.DataFrame(dict(test=[nan])), column='test'),
        make_dataframe_describe(
            count=[0],
            mean=[nan],
            std=[nan],
            min=[nan],
            lower_quartile=[nan],
            median=[nan],
            upper_quartile=[nan],
            max=[nan],
        ),
    ),
    # No group-by columns and zero value in column
    (
        [],
        dict(df=pandas.DataFrame(dict(test=[0])), column='test'),
        make_dataframe_describe(
            count=[1],
            mean=[0],
            std=[nan],
            min=[0],
            lower_quartile=[0],
            median=[0],
            upper_quartile=[0],
            max=[0],
        ),
    ),
    # No group-by columns but other column present and only zeros in column
    (
        [],
        dict(df=pandas.DataFrame(dict(test=[0, 0], test_by=[1, 2])), column='test'),
        make_dataframe_describe(
            count=[2],
            mean=[0],
            std=[0],
            min=[0],
            lower_quartile=[0],
            median=[0],
            upper_quartile=[0],
            max=[0],
        ),
    ),
    # Group-by columns and only zeros in column
    (
        [],
        dict(df=pandas.DataFrame(dict(test=[0, 0], test_by=[1, 2])), column='test', by='test_by'),
        make_dataframe_describe(
            count=[1, 1],
            mean=[0, 0],
            std=[nan, nan],
            min=[0, 0],
            lower_quartile=[0, 0],
            median=[0, 0],
            upper_quartile=[0, 0],
            max=[0, 0],
            test_by=[1, 2],
        ),
    ),
    # Group-by columns and nans and zeros in column
    (
        [],
        dict(df=pandas.DataFrame(dict(test=[0, nan], test_by=[1, 2])), column='test', by='test_by'),
        make_dataframe_describe(
            count=[1, 0],
            mean=[0, nan],
            std=[nan, nan],
            min=[0, nan],
            lower_quartile=[0, nan],
            median=[0, nan],
            upper_quartile=[0, nan],
            max=[0, nan],
            test_by=[1, 2],
        ),
    ),
])
def test_describe(args, kwargs, expected):
    actual = pictorial.aggregate.describe(*args, **kwargs)
    pandas.testing.assert_frame_equal(expected, actual)
