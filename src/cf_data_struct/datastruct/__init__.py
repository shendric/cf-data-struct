# -*- coding: utf-8 -*-

"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import re
import collections
import numpy as np
import pydantic
import xarray as xr
from typing import List, Dict, Tuple, Union, Type, Any
from pydantic import BaseModel

from cf_data_struct.datamodels import (
    GlobalAttributeType, VariableAttributeType, BasicCFGlobalAttributes, BasicVarAttrs
)

VALID_DATATYPES = ["Grid", "Trajectory"]
VALID_VARIABLE_TYPES = ["Standard", "Flag", "Uncertainty"]


class CFVariable(object):
    """
    """

    def __init__(
            self,
            name: str,
            value: np.ndarray,
            dims: Union[str, Tuple[str]],
            var_id: str = None,
            attributes: Union[VariableAttributeType, Dict] = None,
    ) -> None:

        # Save attributes
        self._name = self._validate_name(name)
        self.value = self._validate_value(value)
        self._dims = self._validate_dims(dims, value)
        self._attrs = self._validate_attrs(attributes, self._name)
        self._var_id = self._validate_var_id(var_id, name)

    @staticmethod
    def _validate_name(name: Any) -> str:
        if not isinstance(name, str):
            raise ValueError(f"`name` must be of type str: {name} [{type(name)}]")
        return name

    @staticmethod
    def _validate_value(value: Any) -> np.ndarray:
        if not isinstance(value, collections.abc.Iterable):
            raise ValueError(f"`name` must be of type Iterable: {value} [{type(value)}]")
        return np.array(value)

    @staticmethod
    def _validate_dims(dims: Any, value: np.ndarray) -> Tuple:
        dims = tuple(dims) if isinstance(dims, collections.abc.Iterable) and not isinstance(dims, str) else (dims, )
        if not all(isinstance(dim, str) for dim in dims):
            raise ValueError(f"all dimensions entries must be of type str: f{dims}")
        if len(value.shape) != len(dims):
            raise ValueError(f"Dimension mismatch: Data shape: {value.shape}, dimensions: {dims}")
        return dims

    @staticmethod
    def _validate_attrs(attributes: Any, name: str) -> VariableAttributeType:
        if isinstance(attributes, dict):
            try:
                attributes = BasicVarAttrs(**attributes)
            except pydantic.ValidationError as error:
                raise ValueError(f"Invalid CF variable attributes: {attributes}") from error
        elif attributes is None:
            attributes = BasicVarAttrs(long_name=name)
        elif not issubclass(type(attributes), BasicVarAttrs): 
            raise ValueError(
                f"attribute type is neither dict nor known variable attribute object: "
                f"{attributes} [{type(attributes)}]"
            )
        return attributes

    @staticmethod
    def _validate_var_id(var_id: Any, name: str) -> str:
        if var_id is None:
            if "_" in name:
                var_id = ''.join(x[0] for x in name.split("_")).lower()
            else:
                var_id = re.sub(r'[AEIOU]', '', name, flags=re.IGNORECASE).lower()
        elif not isinstance(var_id, str):
            raise ValueError(f"{var_id=} not of type str: {type(var_id)}")
        if not var_id.isidentifier():
            raise ValueError(f"{var_id=} cannot be safely used as object attribute")
        return var_id.lower()

    def to_xarray_var(
            self,
            ignore_attributes: Union[List[str], Tuple[str, ...]] = None
    ) -> xr.Variable:
        """
        Convert to xarray.Variable for export

        :return:
        """
        pass

    @property
    def dim_dict(self) -> Dict:
        return dict(zip(self._dims, self.value.shape))

    @property
    def name(self) -> str:
        return str(self._name)

    @property
    def id(self) -> str:
        return str(self._var_id)

    @property
    def dims(self) -> Tuple[str, ...]:
        return tuple(self._dims)

    @property
    def attrs(self) -> VariableAttributeType:
        return self._attrs.model_copy()

    @property
    def datatype(self):
        return self.value.dtype

    def __str__(self) -> str:
        """"""
        return (
            f"{self.__class__.__name__} - {self._name}:\n"
            f"var_id             : {self._var_id}\n"
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
