from typing import Optional
from uuid import uuid4

import pandas

from pictorial.utility import validate_index, Index, Aggregator

__all__ = [
    'describe',
    'sum',
]


def generic(
        df: pandas.DataFrame,
        column: str,
        aggregator: Aggregator,
        by: Optional[Index] = None,
) -> pandas.DataFrame:

    by = validate_index(by)
    by_empty = len(by) == 0

    # If by is empty then we will add a temporary column with one value to group by then drop the column after
    # This saves having to describe a single column then to turn to a dataframe then to transpose
    if by_empty:
        column_temp = f'__temp_{uuid4()}'
        df[column_temp] = 0
        by = [column_temp]

    df_aggregated = (
        df
        .groupby(by=by)
        [column]
        .aggregate(aggregator)
        .reset_index()
    )

    if by_empty:
        df_aggregated = df_aggregated.drop(columns=by)

    return df_aggregated


def describe(
        df: pandas.DataFrame,
        column: str,
        by: Optional[Index] = None,
) -> pandas.DataFrame:
    return generic(df=df, column=column, aggregator='describe', by=by)


def sum(
        df: pandas.DataFrame,
        column: str,
        by: Optional[Index] = None,
) -> pandas.DataFrame:
    return generic(df=df, column=column, aggregator='sum', by=by)
