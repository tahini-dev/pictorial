from typing import Union, NoReturn, Sequence, Mapping, Any, Iterable

import numpy as np

__all__ = [
    'assert_equals',
]


def get_iterator_and_assert_str(
        expected: Union[Mapping, Sequence],
        actual: Any,
) -> Iterable:

    if isinstance(expected, str):
        assert expected == actual
        return tuple()
    else:

        if isinstance(expected, Mapping):
            iterator = expected.items()
        elif isinstance(expected, Sequence):
            iterator = enumerate(expected)
        else:
            raise TypeError("Require a dict or a list for expected")

        return iterator


def assert_equals(
        expected: Union[Mapping, Sequence],
        actual: Any,
) -> NoReturn:

    iterator = get_iterator_and_assert_str(expected, actual)

    for key_to_check, expected_value in iterator:
        actual_value = actual[key_to_check]

        if isinstance(expected_value, Mapping):
            assert_equals(expected_value, actual_value)
        elif isinstance(expected_value, Sequence):
            assert_equals(expected_value, actual_value)
        elif isinstance(expected_value, np.ndarray):
            np.testing.assert_array_equal(expected_value, actual_value)
        else:
            assert expected_value == actual_value
