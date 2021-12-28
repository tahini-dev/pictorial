from typing import Optional
from numbers import Number

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

__all__ = [
    'plot',
]


def plot(
        df: pd.DataFrame,
        *args,
        zmin: Optional[Number] = None,
        zmax: Optional[Number] = None,
        **kwargs,
) -> go.Figure:

    if zmin is None:
        zmin = -1
    if zmax is None:
        zmax = 1

    return px.imshow(get_lower_correlation_matrix(df), *args, zmin=zmin, zmax=zmax, **kwargs)


def get_lower_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    correlation = df.corr()
    return correlation.where(np.tril(np.ones(correlation.shape), k=-1).astype(bool))
