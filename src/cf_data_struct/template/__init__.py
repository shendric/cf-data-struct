# -*- coding: utf-8 -*-

"""
Contains the template engine, which can fill strings from templates from context variables and
dictionary like definitions.
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import re
from typing import Dict, Any, Union, List, Callable, Optional
from pydantic import field_validator, RootModel

from enum import StrEnum

from cf_data_struct.template.extended_vars import StrExtendedFormatOptions


class TemplateFillValues(StrEnum):
    UNKNOWN = "unknown" # Tag will be replaced with "unknown" string
    TAG_REMAIN = "tag_remain"  # Tag will remain in the string and not be replaced


class ContextAttributes(RootModel[Dict[str, Any]]):

    @field_validator("root", mode="after")
    @classmethod
    def validate_root(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        extended_format_types_dict: Dict[Callable, Callable] = {
            str: StrExtendedFormatOptions
        }
        for key, value in values.items():
            value_type = type(value)
            # This will replace the value with a type with extended formatting options if one is defined
            # for the original type, otherwise it will keep the original type
            values[key] = extended_format_types_dict.get(value_type, value_type)(value)
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


class TemplateEngine:
    """
    A simple template engine that can fill strings from templates using context variables and
    dictionary-like definitions.
    """

    def __init__(
        self,
        context_attributes: Optional[Dict[str, Any]] = None,
        dynamic_variables: Optional[Dict[str, Dict[str, Any]]] = None,
        fill_value: Union[TemplateFillValues, str] = TemplateFillValues.UNKNOWN,
        raise_on_error: bool = False
    ) -> None:
        """
        Initialize the TemplateEngine with required input

        :param context_attributes: A dictionary with static context attributes that must cover the
            range of all possible template variables. These attributes will be used to fill the templates.
        :param dynamic_variables: A dictionary with dynamic variables that can be used to fill the templates
            based on the value of certain context attributes.
        :param fill_value: The value to use for missing template variables. Can either be a custom string and
            the default values is `unknown` If the value is `tag_remain`, the template variable will remain
            in the string and not be replaced.

        :param raise_on_error: Whether to raise an error if a template variable is missing.
        """

        # Store the context attributes and make sure all data types are compatible
        # with the extended formatting options (This will be done inside ContextAttributes)
        context_attributes = context_attributes or {}
        self._context = ContextAttributes.model_validate(context_attributes)

        # Store the dynamic variables and make sure it is a dictionary
        self._dynamic_variables = dynamic_variables or {}
        assert isinstance(self._dynamic_variables, dict), "dynamic_variables must be a dictionary"

        # Store the fill value and make sure it is a string or a TemplateFillValues enum
        assert isinstance(fill_value, (str, TemplateFillValues)), "fill_value must be a string or TemplateFillValues"
        self._fill_value = fill_value

        assert isinstance(raise_on_error, bool), "raise_on_error must be a boolean"
        self._raise_on_error = raise_on_error

    def render(self, template: str) -> str:
        """
        Render the given template string using the context variables.

        :param template: The template string to be rendered.
        :return: The rendered string with context variables filled in.
        """
        template = self._expand_dict_like_statements(template)
        return template.format(**self._context.root)

    def _expand_dict_like_statements(self, template: str) -> str:
        """
        Fill a dictionary-like statement in the template string using the context variables.

        A dictionary-like statement is a string in the format `{dynamic_variable[context_attribute]}`.

        TODO: Evaluate if extended formatting options should be supported while expanding dictionary-like statements.

        Example:

            context_attributes = {"hemisphere": "nh"}
            dynamic_variable = {"region_name": {"nh": "Arctic", "sh": "Antarctic"}}

            "{region_name[hemisphere]} Sea Ice Thickness Product" -> "Arctic Sea Ice Thickness Product."

        :param template: The template string to be filled.

        :return: The filled string with context variable
        """

        # Ensure that the original template remains unchanged for error handling and debugging purposes
        template_new = str(template)

        # Use a regular expression to find all instances of `{dict_name[key_name]}`
        # with an optional format specifier after the closing bracket.
        dict_pattern = re.compile(r"\{(\w+)\[(\w+)\](?::\w+)?\}")
        matches = dict_pattern.findall(template_new)

        for match in matches:
            dict_name, key_name = match
            if key_name not in self._context:
                return template_new
            if dict_name not in self._dynamic_variables:
                return template_new
            key_var = self._context[key_name]
            if dict_name in self._dynamic_variables:
                value = self._dynamic_variables[dict_name][key_var]
                template_new = template_new.replace(f"{{{dict_name}[{key_name}]}}", value)

        return template_new