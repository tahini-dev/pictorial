from __future__ import annotations

from typing import Optional
from uuid import uuid4

import pandas as pd
import plotly.graph_objects as go


def box(
        df: pd.DataFrame,
        y: str,
        x: Optional[str] = None,
        color: Optional[str] = None,
        mean: Optional[bool] = None,
        sd: Optional[bool] = None,
        order_how: Optional[str] = None,
        order_ascending: Optional[bool] = None,
        category_orders: Optional[dict[str, list]] = None,
) -> go.Figure:
    groupby_columns = []

    if x is None:
        x = f'__x_{uuid4()}'
        df[x] = 0
        x_title = None
    else:
        x_title = x

    groupby_columns.append(x)
    x_values = get_order(
        df,
        column=x,
        column_value=y,
        order_how=order_how,
        order_ascending=order_ascending,
        category_orders=category_orders,
    )

    if color is None:
        color = f'__color_{uuid4()}'
        df[color] = 0

    groupby_columns.append(color)
    color_values = get_order(
        df,
        column=color,
        column_value=y,
        order_how=order_how,
        order_ascending=order_ascending,
        category_orders=category_orders,
    )

    df_plot = (
        df
            .groupby(groupby_columns)
        [y]
            .describe()
            .reset_index()
    )

    x_order = (
        pd.Series(x_values)
            .reset_index()
            .set_index(0)
        ['index']
    )
    df_plot = df_plot.sort_values(x, key=lambda x_value: x_order[x_value])

    fig = go.Figure()
    for color_value in color_values:
        df_color = df_plot[lambda x: x[color] == color_value]
        add_trace(
            fig,
            df_color,
            x=df_color[x],
            name=color_value,
            mean=mean,
            sd=sd,
        )

    fig = (
        fig
            .update_layout(boxmode='group')
            .update_xaxes(title=x_title)
            .update_yaxes(title=y)
    )

    return fig


def get_order(
        df: pd.DataFrame,
        column: str,
        column_value: str,
        order_how: Optional[str] = None,
        order_ascending: Optional[bool] = None,
        category_orders: Optional[dict[str, list]] = None,
) -> list:
    if order_how is None:
        order_how = 'count'

    if order_ascending is None:
        order_ascending = False

    if category_orders is None:
        category_orders = dict()

    order_how = order_how.casefold()
    if order_how == 'count':
        order_from_df = df[column].value_counts().sort_values(ascending=order_ascending).index.tolist()
    elif order_how == 'value':
        order_from_df = df.groupby(column)[column_value].sum().sort_values(ascending=order_ascending).index.tolist()
    elif order_how == 'name':
        order_from_df = df[column].drop_duplicates().sort_values(ascending=order_ascending).tolist()
    else:
        raise NotImplementedError(f"Not implemented for 'order_how': {order_how}")

    order_from_category_orders = category_orders.get(column, list())
    num_from_category_orders = len(order_from_category_orders)

    order = dict(zip(order_from_category_orders, range(num_from_category_orders)))

    rank = num_from_category_orders
    for value in order_from_df:
        order[value] = order.get(value, rank)
        rank += 1

    return sorted(order.keys(), key=lambda x: order[x])


def add_trace(
        fig: go.Figure,
        df: pd.DataFrame,
        x: Optional[list[str]] = None,
        name: Optional[str] = None,
        mean: Optional[bool] = None,
        sd: Optional[bool] = None,
) -> go.Figure:
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

    fig.add_trace(go.Box(
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
    return fig