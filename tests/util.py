from typing import Dict, Union, NoReturn, Iterable, Optional

import numpy as np
import plotly.graph_objects as go


HeatmapOrDict = Union[Dict, go.Heatmap]


def assert_heatmap_equals(
        expected: HeatmapOrDict,
        actual: HeatmapOrDict,
        keys_to_check: Optional[Iterable] = None,
) -> NoReturn:

    if keys_to_check is None:
        keys_to_check = expected.keys()

    for key in keys_to_check:

        if key not in expected:
            raise AssertionError(f"'{key}' does not exist in left")

        if key not in actual:
            raise AssertionError(f"'{key}' does not exist in right")

        expected_value = expected[key]
        actual_value = actual[key]

        if isinstance(expected_value, np.ndarray):
            np.testing.assert_array_equal(expected_value, actual_value)
        else:
            assert expected_value == actual_value
