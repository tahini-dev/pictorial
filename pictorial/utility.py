from __future__ import annotations

from typing import Union, Optional

import pandas

__all__ = [
    'Index',
    'validate_index',
]

Index = Union[str, list[str], pandas.Index, pandas.Series]


def validate_index(
        value: Optional[Index] = None,
        /,
) -> list[str]:

    if value is None:
        return []
    elif isinstance(value, (pandas.Index, pandas.Series)):
        return value.tolist()
    elif isinstance(value, str):
        return [value]
    else:
        return list(value)
