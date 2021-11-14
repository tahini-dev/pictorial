import sys
from typing import Union, Optional, List, Dict, Callable

import pandas

__all__ = [
    'validate_index',
    'Index',
    'Aggregator',
]

if sys.version_info >= (3, 9):
    List = list
    Dict = dict

Index = Union[str, List[str], pandas.Index, pandas.Series]
Aggregator = Union[Callable, str, List, Dict]


def validate_index(
        value: Optional[Index] = None,
        # Add next line in once we do not support python 3.7 which makes this function only take in positional arguments
        # /,
) -> List[str]:

    if value is None:
        return []
    elif isinstance(value, (pandas.Index, pandas.Series)):
        return value.tolist()
    elif isinstance(value, str):
        return [value]
    else:
        return list(value)
