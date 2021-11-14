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


@pytest.mark.parametrize('args, kwargs, expected_error, expected_message', [
    (
        [],
        dict(df=pandas.DataFrame(), column='test', how='test'),
        NotImplementedError,
        "Not implemented for ordering 'how': test",
    )
])
def test_error_get_order(args, kwargs, expected_error, expected_message):
    with pytest.raises(expected_error) as error:
        pictorial.utility.get_order(*args, **kwargs)
    assert expected_message == error.value.args[0]


@pytest.mark.parametrize('args, kwargs, expected', [
    ([], dict(df=pandas.DataFrame(columns=['test']), column='test', how='count'), []),
    ([], dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count'), ['a']),
    ([], dict(df=pandas.DataFrame(dict(test=['a', 'b'])), column='test', how='count', ascending=True), ['a', 'b']),
    ([], dict(df=pandas.DataFrame(dict(test=['a', 'b'])), column='test', how='count', ascending=False), ['a', 'b']),
    ([], dict(df=pandas.DataFrame(dict(test=['a', 'b'])), column='test', how='name', ascending=True), ['a', 'b']),
    ([], dict(df=pandas.DataFrame(dict(test=['a', 'b'])), column='test', how='name', ascending=False), ['b', 'a']),
    ([], dict(df=pandas.DataFrame(dict(test=['a', 'b', 'b'])), column='test', how='count', ascending=True), ['a', 'b']),
    (
        [],
        dict(df=pandas.DataFrame(dict(test=['a', 'b', 'b'])), column='test', how='count', ascending=False),
        ['b', 'a'],
    ),
    ([], dict(df=pandas.DataFrame(dict(test=['a', 'b', 'b'])), column='test', how='name', ascending=True), ['a', 'b']),
    (
        [],
        dict(df=pandas.DataFrame(dict(test=['a', 'b', 'b'])), column='test', how='name', ascending=False),
        ['b', 'a'],
    ),
    (
        [],
        dict(
            df=pandas.DataFrame(dict(test=['a', 'b', 'b'], test_value=[1, 2, 3])),
            column='test',
            how='value',
            column_value='test_value',
            aggregator_value='sum',
            ascending=False,
        ),
        ['b', 'a'],
    ),
    (
        [],
        dict(
            df=pandas.DataFrame(dict(test=['a', 'b', 'b'], test_value=[1, 2, 3])),
            column='test',
            how='value',
            column_value='test_value',
            aggregator_value='sum',
            ascending=True,
        ),
        ['a', 'b'],
    ),
    (
        [],
        dict(
            df=pandas.DataFrame(dict(test=['a', 'b', 'b'], test_value=[4, 2, 3])),
            column='test',
            how='value',
            column_value='test_value',
            aggregator_value='max',
            ascending=False,
        ),
        ['a', 'b'],
    ),
    ([], dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count', prepared_orders=None), ['a']),
    ([], dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count', prepared_orders=dict()), ['a']),
    ([], dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count', prepared_orders=dict(test=[])), ['a']),
    (
        [],
        dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count', prepared_orders=dict(not_test=[])),
        ['a'],
    ),
    (
        [],
        dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count', prepared_orders=dict(test=['a'])),
        ['a'],
    ),
    (
        [],
        dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count', prepared_orders=dict(test=['b', 'a'])),
        ['b', 'a'],
    ),
    (
        [],
        dict(df=pandas.DataFrame(dict(test=['a'])), column='test', how='count', prepared_orders=dict(test=['a', 'b'])),
        ['a', 'b'],
    ),
])
def test_get_order(args, kwargs, expected):
    actual = pictorial.utility.get_order(*args, **kwargs)
    assert expected == actual


# TODO: add hypothesis tests
