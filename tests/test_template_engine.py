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
    rendered_template = t.render("{latency_lower:^} {latency_upper:v}")
    expected_output = "NRT nrt"
    assert rendered_template == expected_output, f"Expected '{expected_output}', but got '{rendered_template}'"

def test_template_engine_string_identifier():
    """
    Test the TemplateEngine class with string identifier conversion
    """
    from cf_data_struct.template import TemplateEngine
    non_identifier_string = "My String - 1"
    assert not non_identifier_string.isidentifier(), f"{non_identifier_string} is not an identifier"
    context_attributes = {"title": non_identifier_string}
    t = TemplateEngine(context_attributes=context_attributes)
    rendered_template = t.render("{title:i}_{title:i^}_{title:iv}")
    expected_output = "My_String___1_MY_STRING___1_my_string__1"
    assert expected_output.isidentifier(), f"{expected_output} is not an identifier"
    assert rendered_template == rendered_template, f"Expected '{expected_output}', but got '{rendered_template}'"


def test_template_engine_datetime_formats():
    """
    Test the TemplateEngine class with datetime attributes.
    """
    from datetime import datetime
    from cf_data_struct.template import TemplateEngine

    context_attributes = {"time_coverage_start": datetime(2020, 1, 1, 12, 10, 30)}
    t = TemplateEngine(context_attributes=context_attributes)
    rendered_template = t.render("{time_coverage_start:%Y-%m-%d %H:%M:%S}")
    expected_output = "2020-01-01 12:10:30"
    assert rendered_template == expected_output, f"Expected '{expected_output}', but got '{rendered_template}'"