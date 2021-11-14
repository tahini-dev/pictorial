from __future__ import annotations
import sys
from typing import Union, Optional, List

import pandas

__all__ = [
    'Index',
    'validate_index',
]

if sys.version_info >= (3, 9):
    List = list

Index = Union[str, List[str], pandas.Index, pandas.Series]


def _validate_index(
        value: Optional[Index] = None,
) -> List[str]:

    if value is None:
        return []
    elif isinstance(value, (pandas.Index, pandas.Series)):
        return value.tolist()
    elif isinstance(value, str):
        return [value]
    else:
        return list(value)


# This is before python 3.7 does not support positional only arguments
if sys.version_info <= (3, 7):
    validate_index = _validate_index
else:
    def validate_index(
            value: Optional[Index] = None,
            /,
    ) -> List[str]:
        return _validate_index(value)
