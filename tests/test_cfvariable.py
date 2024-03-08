# -*- coding: utf-8 -*-

"""
Software tests using pytests for the CFVariable and its children
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import pytest
import numpy as np
from typing import Dict
from cf_data_struct.datastruct import CFVariable


@pytest.mark.parametrize(
    "test_input",
    [
        {},
        {"name": "some_name"},
        {"name": "some_name", "dims": ("time",)},
        {"dims": ("time",)}
    ]
)
def test_cfvariable_incorrect_input(test_input: Dict) -> None:
    with pytest.raises(TypeError):
        CFVariable(**test_input)


@pytest.mark.parametrize(
    "test_input",
    [
        {"name": "some_name"},
        {"name": "some_name", "value": ("time",)},
        {"name": "some_name", "dims": ("time",)},
        {"dims": ("time",)}
    ]
)
def test_cfvariable_insufficient_input(test_input: Dict) -> None:
    with pytest.raises(TypeError):
        CFVariable(**test_input)


@pytest.mark.parametrize(
    "test_input",
    [
        # Wrong basic input type
        {"name": 1, "value": np.zeros(10), "dims": ("time",)},
        {"name": "some_name", "value": 10, "dims": ("time",)},
        {"name": "some_name", "value": np.zeros(10), "dims": 1},
        # Incorrect variable id
        {"name": "some_name", "value": np.zeros(10), "dims": ("time",), "var_id": 10},
        {"name": "some_name", "value": np.zeros(10), "dims": ("time",), "var_id": "10"},
        {"name": "some_name", "value": np.zeros(10), "dims": ("time",), "var_id": "some-var_id"},
        # Mismatch between data shape and dimension specification
        {"name": "some_name", "value": np.zeros(10), "dims": ("time", "incorrect_dim")},
        {"name": "some_name", "value": np.zeros((10, 10)), "dims": ("time",)},
        # Incorrect attributes
        {"name": "some_name", "value": np.zeros(10), "dims": ("time",), "attributes": "some_str"},
        {"name": "some_name", "value": np.zeros(10), "dims": ("time",), "attributes": 1},
    ]
)
def test_cfvariable_incorrect_input_type(test_input: Dict) -> None:
    with pytest.raises(ValueError):
        CFVariable(**test_input)
