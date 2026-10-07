# -*- coding: utf-8 -*-
"""

"""

__author__ = "Stefan Hendricks <stefan.hendricks@awi.de>"


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


def test_template_engine_dynamic_attributes():
    """
    Test the TemplateEngine class with dynamic attributes.
    """
    from cf_data_struct.template import TemplateEngine

    context_attributes = {"hemisphere": "nh"}
    dynamic_variables = {"region_name": {"nh": "Arctic", "sh": "Antarctic"}}

    t = TemplateEngine(context_attributes=context_attributes, dynamic_variables=dynamic_variables)
    rendered_template = t.render("Product for {region_name[hemisphere]}")
    expected_output = "Product for Arctic"
    assert rendered_template == expected_output, f"Expected '{expected_output}', but got '{rendered_template}'"


def test_template_engine_extended_str_formats():
    """
    Test the TemplateEngine class with dynamic attributes.
    """
    from cf_data_struct.template import TemplateEngine

    context_attributes = {"latency_lower": "nrt", "latency_upper": "NRT"}
    t = TemplateEngine(context_attributes=context_attributes)
    rendered_template = t.render("{latency_lower:upper} {latency_upper:lower}")
    expected_output = "NRT nrt"
    assert rendered_template == expected_output, f"Expected '{expected_output}', but got '{rendered_template}'"