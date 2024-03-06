# -*- coding: utf-8 -*-

"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import re
import collections
from typing import List, Dict, Tuple, Union, Type, Any
import numpy as np
import xarray as xr
from pydantic import BaseModel

from cf_data_struct.datamodels import GlobalAttributeType, BasicCFGlobalAttributes

VALID_DATATYPES = ["Grid", "Trajectory"]
VALID_VARIABLE_TYPES = ["Standard", "Flag", "Uncertainty"]


class CFVariable(object):
    """
    Represents a CF variable.

    This class provides functionality to create and manipulate CF variables.

    Args:
        name (str): The name of the variable.
        value (np.ndarray): The value of the variable.
        dims (Union[str, Tuple[str], None]): The dimensions of the variable.
        var_id (str, optional): The ID of the variable. If not provided, it is automatically generated.
        attrs (Type[BaseModel], optional): The attributes of the variable.

    Methods:
        to_xarray_var: Converts the CFVariable to a xarray Variable.

    """

    def __init__(
            self,
            name: str,
            value: np.ndarray,
            dims: Union[str, Tuple[str], None],
            var_id: str = None,
            time_dim_unlimited: bool = False,
            attributes: Type[BaseModel] = None,
    ) -> None:

        # TODO: Add name validation
        self._name = name
        self.value = value
        self._dims = list(dims) if isinstance(dims, collections.abc.Iterable) else [dims]
        self._time_dim_unlimited = time_dim_unlimited
        self._attrs = attributes
        self._var_id = var_id if var_id is not None else self._get_auto_id()

    def _get_auto_id(self) -> str:
        """
        Guess a variable id from the variable name,

        :return:
        """
        if "_" in self._name:
            return ''.join(x[0] for x in self._name.split("_"))
        return re.sub(r'[AEIOU]', '', self._name, flags=re.IGNORECASE)

    def to_xarray_var(self) -> xr.Variable:
        """
        Convert to xarray.Variable for export

        :return:
        """
        pass

    @property
    def name(self) -> str:
        return str(self._name)

    @property
    def id(self) -> str:
        return str(self._var_id)

    @property
    def dims(self) -> List[str]:
        return list(self._dims)

    def __str__(self) -> str:
        """"""
        return (
            f"{self.__class__.__name__} - {self._name}:\n"
            f"var_id             : {self._var_id}\n"
            f"time_dim_unlimited : {self._time_dim_unlimited}\n"
            f"dimensions         : {self._dims} [{self.value.shape}]\n"
            f"attributes         : {self._attrs}"
        )


class CFStructBaseClass(object):

    def __init__(
            self,
            datatype: str = None,
            attributes: GlobalAttributeType = None,
            dims: Union[Tuple[CFVariable], CFVariable] = None,
            variables: Union[Tuple[CFVariable], CFVariable] = None
    ) -> None:
        """

        :param datatype:
        :param attributes:
        :param dims:
        :param variables:
        """

        # Validate input
        if datatype not in VALID_DATATYPES:
            raise ValueError(f"{datatype} not valid cf_data_struct data type [{VALID_DATATYPES}]")

        dims = _is_iterable(dims)
        variables = _is_iterable(variables)

        # Set Class Properties
        self._datatype = datatype
        self.gattrs = attributes if attributes is not None else BasicCFGlobalAttributes()
        self._dims = {}
        self._dim_shape = {}
        self._vars = {}
        self._var_id_dict = {}

        # Add dimensions and variables (if any)
        for dimension in dims:
            self.add_dimension(dimension)

        for variable in variables:
            self.add_dimension(variable)

    def add_dimension(self, dimension: CFVariable) -> None:
        """
        Add a dimension to the data structure.

        :param dimension:
        :return:
        """
        if not isinstance(dimension, CFVariable):
            raise ValueError(f"{dimension=} [type={type(dimension)}] is not of type CFVariable")
        self._dims[dimension.name] = dimension
        self._dim_shape[dimension.name] = dimension.value.shape[0]

    def add_variable(
            self,
            var: CFVariable,
            overwrite: bool = False,
    ) -> None:
        """
        Add a variable to the data structure. Requirements are that the dimensions are already
        known to the data structure.

        :param var: The variable to be added. Must be of type cf_data_struct.CFVariable
        :param overwrite: Overwrite existing variables checked by variable name (default=False)

        :raises: ValueError:

        :return: None
        """

        # Variable input validation
        if not isinstance(var, CFVariable):
            raise ValueError(f"{var=} [type={type(var)}] is not of type CFVariable")

        # Check if dimensions are known
        if not set(var.dims).issubset(self._dims):
            raise ValueError(f"Not all variable dimensions {var.dims=} present in {self.dims=}")

        # Check if dimensions are correct
        expected_dims = self.get_dimensions(var.dims)
        if var.value.shape != expected_dims:
            raise ValueError(f"Dimension of {var.name} not correct: {var.value.shape} != {expected_dims}")

        # Check if variable already exists
        if variable_exists := var.name in self._vars and not overwrite:
            raise ValueError(f"{var.name} already in dataset [{self.variable_names}]")
        overwrite_ok = variable_exists and overwrite

        # Check if variable id exists
        if var.id in self.variable_ids and not overwrite_ok:
            raise ValueError(f"{var.id=} already exists in dataset [{self.variable_ids}]")

        self._vars[var.name] = var
        self._var_id_dict[var.id] = var.name

    def get_dimensions(self, dim_names: List[str]) -> List[int]:
        """
        Return the dimenions as shape list

        :param dim_names: A list of dim names

        :return:
        """
        return []



    @property
    def datatype(self) -> str:
        return str(self._datatype)

    @property
    def dims(self) -> List[str]:
        return list(self._dims.keys())

    @property
    def variable_names(self) -> List[str]:
        return list(self._vars.keys())

    @property
    def variable_id_dict(self) -> Dict:
        return self._var_id_dict.copy()
    @property
    def variable_ids(self) -> List[str]:
        return list(self._var_id_dict.keys())

class TrajectoryCFStruct(CFStructBaseClass):

    def __init__(self, **kwargs):
        super(TrajectoryCFStruct, self).__init__(datatype="Trajectory", **kwargs)


class GridCFStruct(CFStructBaseClass):

    def __init__(self, **kwargs):
        super(GridCFStruct, self).__init__(datatype="Grid", **kwargs)
        self.grid_mapping = None


def _is_iterable(value: Union[List, Tuple, Any, None]) -> List[Any]:
    """
    Ensure a variable is always a list. If None it should be an empty list

    :param value:

    :return: "listified value"
    """
    if value is None:
        return []
    return value if isinstance(value, collections.abc.Iterable) else [value]
