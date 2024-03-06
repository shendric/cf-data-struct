# -*- coding: utf-8 -*-

"""
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from typing_extensions import Annotated
from typing import Optional, Iterable, Tuple, Union, List

import numpy as np
from pydantic import BaseModel, Field, field_validator, model_validator, Extra

# ISO 19115-1 codes
VALID_COVERAGE_CONTENT_TYPE = [
    "image",
    "thematicClassification",
    "physicalMeasurement",
    "auxiliaryInformation",
    "qualityInformation",
    "referenceInformation",
    "modelResult",
    "coordinate"
]

numeric = Union[int, float]


class GlobalAttributes(object):

    def __init__(self):
        pass


class CFVarAttrs(BaseModel, extra=Extra.allow):
    """
    Variable Attributes according to the CF Conventions:
    https://cfconventions.org/cf-conventions/cf-conventions.html#_description_of_the_data

    This is not a complete list and extra keywords are allowed. The general concept is
    that this pydantic.Basemodel holds all fields and only enforces the use of
    `long_name` as the basic common denominator of all variable types.

    Children classes can and should be used to add custom validtors for specific
    variable types, e.g. flags, gridded variables etc. Combinations are possible,
    e.g. gridded flags.
    """

    long_name: str
    standard_name: Optional[str] = None
    comment: Optional[str] = None
    units: Optional[str] = None
    ancillary_variables: Optional[str] = None
    coverage_content_type: Annotated[Optional[str], Field(validate_default=False)] = None
    flag_meanings: Optional[str] = None
    flag_values: Optional[List[numeric]] = None
    valid_min: Optional[numeric] = None
    valid_max: Optional[numeric] = None
    grid_mapping: Optional[str] = None

    # noinspection PyNestedDecorators
    @field_validator("coverage_content_type")
    @classmethod
    def valid_coverage_content_type(cls, coverage_content_type: str) -> str:
        if coverage_content_type not in VALID_COVERAGE_CONTENT_TYPE:
            raise ValueError(f"{coverage_content_type=} not in {VALID_COVERAGE_CONTENT_TYPE=}")
        return coverage_content_type


class FlagVarAttrs(CFVarAttrs):

    @model_validator(mode="after")
    def has_flag_attributes(self):
        if self.flag_values is None:
            raise ValueError(f"{self.__class__.__name__} requires attribute `flag_values`")
        if self.flag_meanings is None:
            raise ValueError(f"{self.__class__.__name__} requires attribute `flag_meanings`")
        if len(self.flag_values) != len(self.flag_meanings.split()):
            raise ValueError(f"{self.flag_values=} and {self.flag_meanings} does not match")


class GridVarAttrs(CFVarAttrs):

    @model_validator(mode="after")
    def has_grid_attributes(self):
        if self.grid_mapping is None:
            raise ValueError(f"{self.__class__.__name__} requires attribute `grid_mapping`")


class GridFlagAttrs(FlagVarAttrs, GridVarAttrs):
    pass
