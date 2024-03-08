# -*- coding: utf-8 -*-

"""
Software tests using pytests for the CFVariable and its children
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import pytest
import numpy as np
from typing import Dict, Tuple
from cf_data_struct.datastruct import CFVariable, BasicVarAttrs


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
        # Incorrect name
        {"name": "some name", "value": np.zeros(10), "dims": ("time",)},
        {"name": "some-name", "value": np.zeros(10), "dims": ("time",)},
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


@pytest.mark.parametrize(
    "test_input, expected_result",
    [
        ({"name": "some_name", "value": np.zeros(10), "dims": "time"}, ("time",))
    ]
)
def test_cfvariable_dims_cast_to_tuple(test_input: Dict, expected_result: Tuple[str, ...]) -> None:
    var = CFVariable(**test_input)
    assert var.dims == expected_result


@pytest.mark.parametrize(
    "test_input",
    [
        {"name": "some_name", "value": np.zeros(10), "dims": "time"},
        {"name": "some_name", "value": np.zeros(10), "dims": "time", "attributes": {"long_name": "some_name"}}
    ]
)
def test_cfvariable_varattr_cast_to_object(test_input: Dict) -> None:
    var = CFVariable(**test_input)
    assert isinstance(var.attrs, BasicVarAttrs)
