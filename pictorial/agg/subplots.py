from plotly.subplots import make_subplots


def create_subplot_by_function(func, cases, num_rows, num_cols, height=None, width=None):
    if height is None:
        height = max(num_rows * 300, 400)
    if width is None:
        width = 1100

    fig = make_subplots(rows=num_rows, cols=num_cols)
    fig.update_layout(width=width, height=height)

    row = 1
    col = 1

    for case in cases:
        fig_case = func(case)
        for trace in fig_case.data:
            fig.add_trace(trace, row=row, col=col)

        col += 1
        if col > num_cols:
            col = 1
            row += 1

    return fig



