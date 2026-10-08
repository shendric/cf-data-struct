
import numpy as np
import xarray as xr

from typing import Any, Dict, List, Tuple, Union, Optional, Type

class FlagVariable(xr.Variable):

    @classmethod
    def init(
        cls,
        dims: Tuple[int, ...],
        value: np.ndarray,
        attrs: Dict[str, Any],
        flag_values: List[Any],
        flag_meanings: List[str],
        to_datatype: Optional[Type] = None,
    ) -> FlagVariable:
        pass

