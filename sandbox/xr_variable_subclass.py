
import numpy as np
import xarray as xr

from typing import Any, Dict, List, Tuple, Union, Optional, Type
from pydantic import BaseModel

from cf_data_struct.datamodels import ContentType

class Encoding(BaseModel):
    dtype: str
    scale_factor: Optional[float] = None
    add_offset: Optional[float] = None
    _FillValue:  Optional[float | int] = None
    zlib: bool = True
    complevel: int = 5,

class

class FlagVariable(xr.Variable):
    """
    Alias to xr.Variable with simpler init metho
    """

    @classmethod
    def init(
        cls,
        dims: Tuple[int, ...],
        value: np.ndarray,
        attrs: Dict[str, Any],
        flag_values: List[Any],
        flag_meanings: List[str],
        to_datatype: Optional[Type] = None,
        coverage_content_type: Optional[ContentType] = None,
        encoding: Optional[Dict[str, str]] = None,
    ) -> FlagVariable:
        """

        :param dims:
        :param value:
        :param attrs:
        :param flag_values:
        :param flag_meanings:
        :param to_datatype:
        :param coverage_content_type:
        :param encoding:

        :return: An xr.Variable
        """
        pass

