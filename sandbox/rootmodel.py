# -*- coding: utf-8 -*-
"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from typing import Any, Dict, List, Union, Callable
from pydantic import RootModel, model_validator, field_validator


class StrExtendedFormatOptions(str):
    """
    A version of the built-in str class that supports additional formatting options.

    - Uppercase: Use the format specifier "upper" to convert the string to uppercase.
                 `"{:upper}".format(StrExtendedFormatOptions("my_string"))` will return `MY_STRING`.
    - Lowercase: Use the format specifier "lower" to convert the string to lowercase
                 `"{:lower}".format(StrExtendedFormatOptions("MY_STRING"))` will return `my_string`.
    """
    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "upper": return self.upper()
            case "lower": return self.lower()
            case _:  return f"{super().__format__(format_spec)}"


class ContextAttributes(RootModel[Dict[str, Any]]):

    @field_validator("root", mode="after")
    @classmethod
    def validate_root(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        extended_format_types_dict: Dict[Callable, Callable] = {
            str: StrExtendedFormatOptions
        }
        for key, value in values.items():
            value_type = type(value)
            new_value = extended_format_types_dict.get(type(value), value_type)(value)
            values[key] = new_value
        return values

    @property
    def items(self) -> List[str]:
        return sorted(list(self.root.keys()))

    def __getattr__(self, item):
        return self.root[item]

    def __getitem__(self, item):
        return self.root[item]

    def __contains__(self, item):
        return item in self.items


context_attributes = {
    "product": "awi",
    "timeliness": "nrt",
    "version": "v1p0",
    "hemisphere": "nh",
}

context = ContextAttributes.model_validate(context_attributes)

print("{:upper}".format(context.product))