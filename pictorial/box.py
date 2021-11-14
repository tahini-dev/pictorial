from typing import Optional
from uuid import uuid4

import pandas
import plotly.graph_objects

from pictorial.utility import get_order, CategoryOrders
import pictorial.aggregate

__all__ = [
    'plot',
]


def plot(
        df: pandas.DataFrame,
        y: str,
        x: Optional[str] = None,
        color: Optional[str] = None,
        mean: Optional[bool] = None,
        sd: Optional[bool] = None,
        order_how: Optional[str] = None,
        order_ascending: Optional[bool] = None,
        category_orders: Optional[CategoryOrders] = None,
) -> plotly.graph_objects.Figure:

    by = []

    if x is None:
        x = f'__x_{uuid4()}'
        df[x] = 0
        x_title = None
    else:
        x_title = x
    by.append(x)

    x_values = get_order(
        df,
        column=x,
        column_value=y,
        how=order_how,
        ascending=order_ascending,
        prepared_orders=category_orders,
    )

    if color is None:
        color = f'__color_{uuid4()}'
        df[color] = 0

    by.append(color)
    color_values = get_order(
        df,
        column=color,
        column_value=y,
        how=order_how,
        ascending=order_ascending,
        prepared_orders=category_orders,
    )

    df_aggregated = pictorial.aggregate.describe(df=df, column=y, by=by)

    x_order = (
        pandas.Series(x_values)
        .reset_index()
        .set_index(0)
        ['index']
    )
    df_aggregated = df_aggregated.sort_values(x, key=lambda x_value: x_order[x_value])

    figure = plotly.graph_objects.Figure()
    for color_value in color_values:
        df_color = df_aggregated[lambda d: d[color] == color_value]
        add_trace(
            figure,
            df_color,
            x=df_color[x],
            name=color_value,
            mean=mean,
            sd=sd,
        )

    figure = (
        figure
        .update_layout(boxmode='group')
        .update_xaxes(title=x_title)
        .update_yaxes(title=y)
    )

    return figure


def add_trace(
        figure: plotly.graph_objects.Figure,
        df: pandas.DataFrame,
        x: Optional[list[str]] = None,
        name: Optional[str] = None,
        mean: Optional[bool] = None,
        sd: Optional[bool] = None,
) -> plotly.graph_objects.Figure:

    if mean is None:
        mean = True

    if sd is None:
        sd = True

    if mean:
        mean_values = df['mean']
    else:
        mean_values = None

    if sd:
        sd_values = df['std']
    else:
        sd_values = None

    figure = figure.add_trace(plotly.graph_objects.Box(
        x=x,
        lowerfence=df['min'],
        q1=df['25%'],
        median=df['50%'],
        q3=df['75%'],
        upperfence=df['max'],
        mean=mean_values,
        sd=sd_values,
        name=name,
    ))

    return figure
