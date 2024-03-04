# -*- coding: utf-8 -*-

"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from typing import List, Dict, Tuple
import numpy as np
import xarray as xr

from .datamodels import GlobalAttributes

VALID_DATATYPES = ["Grid", "Trajectory"]
VALID_VARIABLE_TYPES = ["Standard", "Flag", "Uncertainty"]


class CFStructBaseClass(object):

    def __init__(
            self,
            datatype: str = None,
            gattrs: GlobalAttriubtes = None,
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
        super(TrajectoryCFStruct, self).__init__(datatype="Grid", **kwargs)


class GridCFStruct(CFStructBaseClass):

    def __init__(self, **kwargs):
        super(GridCFStruct, self).__init__(datatype="Grid", **kwargs)


class CFVariable(object):

    def __init__(
            self,
            variable_type: str,
            name: str,
            value: np.ndarray,
            dims: Tuple[int],
            attrs: Dict = None
    ) -> None:
        """

        :param name:
        :param value:
        :param dims:
        :param attrs:
        """

        self._variable_type = variable_type
        self._name = name
        self.value = value
        self._dims = dims
        self._attrs = attrs

    def to_xarray_var(self) -> xr.Variable:
