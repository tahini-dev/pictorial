from typing import Callable, Optional

import plotly.graph_objects
from plotly.subplots import make_subplots

__all__ = ['make']


def make(
        func: Callable,
        cases,
        num_rows: Optional[int] = None,
        num_cols: Optional[int] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
) -> plotly.graph_objects.Figure:

    if num_rows is None:
        num_rows = 1

    if num_cols is None:
        num_cols = 1

    if height is None:
        height = max(num_rows * 300, 400)

    if width is None:
        width = 1100

    figure = (
        make_subplots(rows=num_rows, cols=num_cols)
        .update_layout(width=width, height=height)
    )

    row = 1
    col = 1

    for case in cases:
        figure_case = func(case)
        for trace in figure_case.data:
            figure.add_trace(trace, row=row, col=col)

        col += 1
        if col > num_cols:
            col = 1
            row += 1

    return figure
