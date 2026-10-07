# -*- coding: utf-8 -*-

"""
Contains the template engine, which can fill strings from templates from context variables and
dictionary like definitions.
"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

from typing import Dict, Any

class TemplateEngine:
    """
    A simple template engine that can fill strings from templates using context variables and
    dictionary-like definitions.
    """

    def __init__(
        self,
        context: Dict[str, Any] = None,


    ):
        """
        Initialize the TemplateEngine with an optional context.

        :param context: A dictionary containing context variables for template rendering.
        """
        self.context = context or {}

    def render(self, template: str) -> str:
        """
        Render the given template string using the context variables.

        :param template: The template string to be rendered.
        :return: The rendered string with context variables filled in.
        """
        return template.format(**self.context)