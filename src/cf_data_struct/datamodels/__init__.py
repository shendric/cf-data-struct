# -*- coding: utf-8 -*-

"""
This module contains pydantic data models for

- CF & ADDC global attributes
- CF variable attributes

with (limited) validation and templates for different data types.
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from enum import StrEnum

from typing import List, Optional, Tuple, TypeVar, Union

from pydantic import BaseModel, Extra, Field, field_validator, model_validator
from typing_extensions import Annotated


# ISO 19115-1 codes
class ContentType(StrEnum):
    """
    Valid content types (ISO 19115-1 code) according to ACCD conventions:
    https://wiki.esipfed.org/Attribute_Convention_for_Data_Discovery_1-3
    """
    IMAGE = "image"
    THEMATIC_CLASSIFICATION = "thematicClassification"
    PHYSICAL_MEASUREMENT = "physicalMeasurement"
    AUXILIARY_INFORMATION = "auxiliaryInformation"
    QUALITY_INFORMATION = "qualityInformation"
    REFERENCE_INFORMATION = "referenceInformation"
    MODEL_RESULT = "modelResult"
    COORDINATE = "coordinate"

    def entries(cls) -> List[str]:
        return [e.value for e in cls]


class Calendar(StrEnum):
    """
    Valid calendar types according to CF conventions:
    https://cfconventions.org/cf-conventions/cf-conventions.html#calendar
    """
    GREGORIAN = "gregorian"
    STANDARD = "standard"
    PROLEPTIC_GREGORIAN = "proleptic_gregorian"
    NOLEAP = "noleap"
    _365_DAY = "365_day"
    ALL_LEAP = "all_leap"
    _366_DAY = "366_day"
    _360_DAY = "360_day"
    JULIAN = "julian"
    NONE = "none"

    def entries(cls) -> List[str]:
        return [e.value for e in cls]


NUMERIC_TYPE = Union[int, float]
FLAG_DTYPES = Union[int, bytes]


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
    scale_factor: Optional[NUMERIC_TYPE] = None
    add_offset: Optional[NUMERIC_TYPE] = None
    actual_range: Optional[Tuple[NUMERIC_TYPE, NUMERIC_TYPE]] = None
    missing_value: Optional[NUMERIC_TYPE] = None
    comment: Optional[str] = None
    units: Optional[str] = None
    ancillary_variables: Optional[str] = None
    coverage_content_type: Optional[ContentType] = None
    valid_min: Optional[NUMERIC_TYPE] = None
    valid_max: Optional[NUMERIC_TYPE] = None

    # noinspection PyNestedDecorators
    @field_validator("coverage_content_type")
    @classmethod
    def valid_coverage_content_type(cls, coverage_content_type: str) -> str:
        if coverage_content_type not in ContentType.__members__:
            raise ValueError(f"{coverage_content_type=} not in {list(ContentType.entries())=}")
        return coverage_content_type


class FlagVarAttrs(BasicVarAttrs):
    flag_meanings: str
    flag_values: List[FLAG_DTYPES]
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
        if calendar not in Calendar:
            raise ValueError(f"{calendar=} not in {Calendar.entries()=}")
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
