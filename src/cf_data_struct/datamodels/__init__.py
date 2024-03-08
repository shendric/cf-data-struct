# -*- coding: utf-8 -*-

"""
This module contains pydantic data models for

- CF & ADDC global attributes
- CF variable attributes

with (limited) validation and templates for different data types.
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from typing_extensions import Annotated
from typing import Optional, Union, List, Tuple, TypeVar

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

VALID_CALENDARS = [
    "gregorian",
    "standard",
    "proleptic_gregorian",
    "noleap",
    "365_day",
    "all_leap",
    "366_day",
    "360_day",
    "julian",
    "none"
]

numeric = Union[int, float]
flag_dtypes = Union[int, bytes]


class BasicCFGlobalAttributes(BaseModel):
    """
    Minimum global attributes according to CF-Conventions
    """
    title: str = None
    institution: str = None
    source: str = None
    history: str = None
    references: str = None
    comment: str = None


class BasicVarAttrs(BaseModel, extra=Extra.allow):
    """
    Variable Attributes according to the CF Conventions:
    https://cfconventions.org/cf-conventions/cf-conventions.html#_description_of_the_data

    This is not a complete list and extra keywords are allowed. The general concept is
    that this pydantic.Basemodel holds all fields and only enforces the use of
    `long_name` as the basic common denominator of all variable types.

    Children classes should overwrite the fields whenever necessary and add their
    own validators. Combinations are also possible.
    """

    long_name: str
    standard_name: Optional[str] = None
    scale_factor: Optional[numeric] = None
    add_offset: Optional[numeric] = None
    actual_range: Optional[Tuple[numeric, numeric]] = None
    missing_value: Optional[numeric] = None
    comment: Optional[str] = None
    units: Optional[str] = None
    ancillary_variables: Optional[str] = None
    coverage_content_type: Annotated[Optional[str], Field(validate_default=False)] = None
    valid_min: Optional[numeric] = None
    valid_max: Optional[numeric] = None

    # noinspection PyNestedDecorators
    @field_validator("coverage_content_type")
    @classmethod
    def valid_coverage_content_type(cls, coverage_content_type: str) -> str:
        if coverage_content_type not in VALID_COVERAGE_CONTENT_TYPE:
            raise ValueError(f"{coverage_content_type=} not in {VALID_COVERAGE_CONTENT_TYPE=}")
        return coverage_content_type


class FlagVarAttrs(BasicVarAttrs):
    flag_meanings: str
    flag_values: List[flag_dtypes]
    unit: str = "1"

    @model_validator(mode="after")
    @classmethod
    def has_flag_attributes(cls, values):
        if len(values.flag_values) != len(values.flag_meanings.split()):
            raise ValueError(f"{values.flag_values=} and {values.flag_meanings} does not match")


class TimeVarAttrs(BaseModel):
    """
    Variable attribute model for time attributes, e.g.
    - time
    - time_bnds
    """
    long_name: str
    units: Optional[str] = None
    calendar: Annotated[Optional[str], Field(validate_default=False)] = None

    @field_validator("calendar")
    @classmethod
    def valid_calendar(cls, calendar: str) -> str:
        if calendar not in VALID_CALENDARS:
            raise ValueError(f"{calendar=} not in {VALID_CALENDARS=}")
        return calendar


class GridVarAttrs(BasicVarAttrs):
    """
    Grid variables.
    """
    grid_mapping: str
    cell_methods: Optional[str] = None


class GridFlagVarAttrs(FlagVarAttrs, GridVarAttrs):
    """
    A combination of datatype grid and flag variables.
    """
    pass


# Helper variable for typing
GlobalAttributeType = Union[BasicCFGlobalAttributes]
VariableAttributeType = TypeVar("VariableAttributeType", bound=BasicVarAttrs)
