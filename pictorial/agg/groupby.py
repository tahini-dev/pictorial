

def plotly_bar_group(df, col, *args, **kwargs):
    px.bar(df.groupby(col).count(),x=col, y=count, *args, **kwargs)