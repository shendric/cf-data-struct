# -*- coding: utf-8 -*-

"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import re
from typing import List, Dict, Tuple, Union, Type
import numpy as np
import xarray as xr
from pydantic import BaseModel

from cf_data_struct.datamodels import GlobalAttributes

VALID_DATATYPES = ["Grid", "Trajectory"]
VALID_VARIABLE_TYPES = ["Standard", "Flag", "Uncertainty"]


class CFStructDataSet(object):

    def __init__(self) -> None:
        pass


class CFStructBaseClass(object):

    def __init__(
            self,
            datatype: str = None,
            gattrs: GlobalAttributes = None,
            dataset: CFStructDataSet = None
    ) -> None:
        """

        :param datatype:
        :param gattrs:
        :param dataset:
        """

        if datatype not in VALID_DATATYPES:
            raise ValueError(f"{datatype} not valid cf_data_struct data type [{VALID_DATATYPES}]")
        self._datatype = datatype
        self.gattrs = gattrs
        self.dataset = dataset

    @property
    def datatype(self) -> str:
        return str(self._datatype)


class TrajectoryCFStruct(CFStructBaseClass):

    def __init__(self, **kwargs):
        super(TrajectoryCFStruct, self).__init__(datatype="Trajectory", **kwargs)


class GridCFStruct(CFStructBaseClass):

    def __init__(self, **kwargs):
        super(GridCFStruct, self).__init__(datatype="Grid", **kwargs)
        self.grid_mapping = None


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
            attrs: Type[BaseModel] = None,
    ) -> None:

        # TODO: Add name validation
        self._name = name
        self.value = value
        self._dims = dims
        self._time_dim_unlimited = time_dim_unlimited
        self._attrs = attrs
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

    def __str__(self) -> str:
        """"""
        return (
            f"{self.__class__.__name__} - {self._name}:\n"
            f"var_id             : {self._var_id}\n"
            f"time_dim_unlimited : {self._time_dim_unlimited}\n"
            f"dimensions         : {self._dims} [{self._value.shape}]\n"
            f"attributes         : {self._attrs}"
        )
