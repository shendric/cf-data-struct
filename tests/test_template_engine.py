# -*- coding: utf-8 -*-
"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"

import pytest


def test_template_engine_basic():
    """
    Test the TemplateEngine class.
    """
    from cf_data_struct.template import TemplateEngine

    context_attributes = {
        "product": "awi",
        "timeliness": "nrt",
        "version": "v1p0",
        "hemisphere": "nh",
    }

    t = TemplateEngine(context_attributes=context_attributes)
    rendered_template = t.render("product: {product}, timeliness: {timeliness}, version: {version}, hemisphere: {hemisphere}.")
    expected_output = "product: awi, timeliness: nrt, version: v1p0, hemisphere: nh."
    assert rendered_template == expected_output, f"Expected '{expected_output}', but got '{rendered_template}'"


