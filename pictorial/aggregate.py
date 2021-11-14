from __future__ import annotations
from typing import Optional
from uuid import uuid4

import pandas as pd

from pictorial.utility import Index, validate_index


def describe(
        df: pd.DataFrame,
        column: str,
        by: Optional[Index] = None,
) -> pd.DataFrame:

    by = validate_index(by)
    by_empty = len(by) == 0

    if by_empty:
        column_temp = f'__temp_{uuid4()}'
        df[column_temp] = 0
        by = [column_temp]

    df_describe = (
        df
        .groupby(by=by)
        [column]
        .describe()
        .reset_index()
    )

    if by_empty:
        df_describe = df_describe.drop(columns=by)

    return df_describe
