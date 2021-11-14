from typing import Optional

import pandas
import plotly.express
import plotly.graph_objects

from pictorial.utility import CategoryOrders, get_order
import pictorial.aggregate

__all__ = [
    'bar',
]


def bar(
        df: pandas.DataFrame,
        y: str,
        x: Optional[str] = None,
        color: Optional[str] = None,
        facet_col: Optional[str] = None,
        facet_row: Optional[str] = None,
        category_orders: Optional[CategoryOrders] = None,
        *args,
        **kwargs,
) -> plotly.graph_objects.Figure:

    by = []

    if x is not None:
        by.append(x)

    if color is not None:
        by.append(color)

    if facet_col is not None:
        by.append(facet_col)

    if facet_row is not None:
        by.append(facet_row)

    if category_orders is None:
        category_orders = dict()

    for column in by:
        category_orders[column] = get_order(df=df, column=column, column_value=y, prepared_orders=category_orders)

    # The following could be replaced by a generic aggregator
    df_aggregated = pictorial.aggregate.sum(df=df, column=y, by=by)

    return plotly.express.bar(
        data_frame=df_aggregated,
        x=x,
        y=y,
        color=color,
        facet_col=facet_col,
        facet_row=facet_row,
        category_orders=category_orders,
        *args,
        **kwargs,
    )
