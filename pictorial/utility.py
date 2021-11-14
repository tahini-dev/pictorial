import sys
from typing import Union, Optional, List, Dict, Callable

import pandas

__all__ = [
    'get_order',
    'validate_index',
    'Index',
    'Aggregator',
    'CategoryOrders',
    'List',
]

if sys.version_info >= (3, 9):
    List = list
    Dict = dict

Index = Union[str, List[str], pandas.Index, pandas.Series]
Aggregator = Union[Callable, str, List, Dict]
CategoryOrders = Dict[str, List]


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


def get_order(
        df: pandas.DataFrame,
        column: str,
        how: Optional[str] = None,
        ascending: Optional[bool] = None,
        column_value: Optional[str] = None,
        aggregator_value: Optional[Aggregator] = None,
        prepared_orders: Optional[CategoryOrders] = None,
) -> List:

    if how is None:
        how = 'value'
    how = how.casefold()

    if ascending is None:
        if how == 'name':
            ascending = True
        else:
            ascending = False

    if aggregator_value is None:
        aggregator_value = 'sum'

    if prepared_orders is None:
        prepared_orders = dict()

    if how == 'count':
        order_from_df = df[column].value_counts().sort_values(ascending=ascending).index.tolist()
    elif how == 'name':
        order_from_df = df[column].drop_duplicates().sort_values(ascending=ascending).tolist()
    elif how == 'value':
        order_from_df = (
            df
            .groupby(column)
            [column_value]
            .aggregate(aggregator_value)
            .sort_values(ascending=ascending)
            .index
            .tolist()
        )
    else:
        raise NotImplementedError(f"Not implemented for ordering 'how': {how}")

    order_from_category_orders = prepared_orders.get(column, list())
    num_from_category_orders = len(order_from_category_orders)

    order = dict(zip(order_from_category_orders, range(num_from_category_orders)))
    for rank, value in enumerate(order_from_df, start=num_from_category_orders):
        order[value] = order.get(value, rank)

    return sorted(order.keys(), key=lambda x: order[x])
